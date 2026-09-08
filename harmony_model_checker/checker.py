#!/usr/bin/env python3
"""Semantic identifier checking for Harmony programs, built on top of the
syntax parser in harmony_parser.py.

This is a genuinely different kind of check than anything in
harmony_parser.py: harmony_parser.py only ever looks at one parse tree
in isolation and asks "is
this syntax legal on its own terms?". This module asks a whole-program
question - "do these names, taken together, mean something coherent?" -
which needs a symbol table, not just a grammar.

The work is split into two phases (agreed on with the language's
designer):

  Phase 1 (implemented here): whole-program GLOBAL namespace uniqueness
  - purely a NAMING check, independent of Phase 2's scoping/reachability
  rules below. `import`, `from x import ...`, `const`, and `def` all
  share one flat, whole-program namespace in Harmony, regardless of how
  deeply any particular `const`/`def` happens to be nested textually
  (even one written inside a function body is still global BY NAME) -
  Harmony does not support shadowing, so no two of these may collide
  anywhere in a program. `from x import *` additionally requires
  knowing what module `x` actually exports (only its own non-underscore
  `const`/`def` names), which this module resolves by parsing `x`'s
  source, found by trying (in order) an externally-supplied
  `module_map: dict[module_name, file_path]`, then `<name>.hny` next to
  the file actually being checked, then `<name>.hny` in
  DEFAULT_MODULE_DIR (Harmony's own bundled modules) - recursively,
  since `x` may itself wildcard-import something. One deliberate
  exception to "no two may collide": a `def` and a `builtin` sharing
  the same name (in either order) is a common Harmony idiom - the `def`
  is a reference implementation the model checker can reason about, and
  the `builtin` a native implementation of the exact same function for
  efficiency - so that specific pairing is allowed once per name,
  though a third declaration of it (another def or builtin) is still a
  real duplicate.

  Phase 2 (implemented here too): per-function local-namespace
  uniqueness AND scoping - this is what actually decides where a name
  can be USED, on top of Phase 1's naming check. Every name used
  anywhere in a program must be declared somewhere reachable, before
  its use, in the scope where it's used - Harmony has no implicit-
  global fallback, and being part of Phase 1's flat namespace does NOT
  by itself make a name usable everywhere. var/let/param/for/lambda/
  exists-bound names, a function's own "returns NAME", and any name
  declared by a `global`/`sequential`/`const`/`import`/`from` statement
  all share ONE flat per-function pool - no shadowing within it (a name
  already open in an enclosing construct can't be redeclared by a
  nested one), and (since Harmony has no closures) each function's pool
  is completely independent of every other's, including its own
  enclosing function's. Only TWO kinds are exempt from all of this:

    - `def`/`builtin` are fully HOISTED - usable from literally
      anywhere in the program, including before their own declaration,
      so that mutual recursion between functions works regardless of
      which one is written first. A `def` nested inside another
      function is a partial exception even to this: it's still part of
      Phase 1's flat namespace (can't collide with any other def/const/
      import/builtin by name), but only actually CALLABLE from the
      function it's lexically nested directly inside, or from another
      def nested (to any depth) inside that same function - never from
      its caller, a sibling function, or the top level (see
      _scope_reachable/program.def_scopes).

  Every OTHER kind - param/returns (persistent, visible for a
  function's whole body regardless of position, since they're bound at
  the signature before the body even starts) and var/for/let/lambda/
  exists/global/sequential/const/import/from (block-scoped, visible
  only from their own point of declaration to the end of their own
  enclosing block, exactly the way an ordinary `var` already is) -
  needs its own declaration reachable from where it's used. A
  `global`/`sequential`/`const`/`import`/`from` declared inside a
  function, or inside any nested block, needs its own such declaration
  in every OTHER function that also wants to touch it - declaring it in
  one function does not, on its own, make it usable in another. The one
  exception: one of these written directly, unnested, in the program's
  own top-level statement list (not inside any if/while/for/let, and
  not inside any function) is PROMOTED into a second, genuinely
  program-wide namespace (program.promoted) - since Harmony has no
  closures to make a top-level name function-local otherwise, and this
  is the one case where that would make an ordinarily-shared name
  needlessly hard to actually use. It gets a declared-before-use
  ordering instead of def's full hoisting, so a function may use it
  (with no declaration of its own) exactly when its own top-level
  statement appears earlier in the program's text than the use,
  function bodies included. A local may also never shadow a whole-
  program global - an import/const/def name (Phase 1's namespace,
  regardless of nesting or promotion), or one of these promoted top-
  level global/sequential names specifically (a function's OWN matching
  `global`/`sequential` restatement of one is exempt, as the harmless
  no-op it's always been). The one thing that's still separately
  program-wide about every `global`/`sequential` declaration, promoted
  or not, is that the same name can't be claimed 'global' in one place
  and 'sequential' in another, anywhere in the program.

  On top of that namespace, two lvalue-kind restrictions fall out of
  the identifier taxonomy (module / shared-variable / local / constant
  / function): `?x` is legal only when x resolves to a function or a
  shared/global variable - never a local, a constant, a module, or an
  imported name (imports bring in values, not live addresses, so they
  behave like constants here); an assignment target is illegal when it
  resolves to a module, constant, function, or imported name, or to a
  *read-only* local (let/param/for/lambda/exists - only
  var/returns/global/sequential are mutable).

Nothing here raises on a found problem; a parse failure and every
namespace collision, scoping violation, or lvalue-kind violation are
reported as CheckError entries - `.errors` for both phases combined,
`.warnings` for anything merely advisory - so a caller sees every
problem in one pass rather than only the first.
"""

import os

# harmony_parser.py is this module's own sibling - inside the
# harmony_model_checker package when installed there (the normal case),
# or right next to this file when it's run as a standalone script
# (`python3 checker.py ...`, see main() below) - either way this finds
# it, since a relative import only works in the former case (it needs a
# real enclosing package) and falls back to a plain one for the latter
# (Python already puts a directly-run script's own directory on
# sys.path, so a bare `import harmony_parser` finds the sibling file
# there). Named harmony_parser.py, not parser.py, because
# harmony_model_checker already has its own 'parser' - the ANTLR-
# generated parser/ package (HarmonyParser.py etc.) - and a same-named
# sibling module would collide with (and lose to) that package.
try:
    from . import harmony_parser
except ImportError:
    import harmony_parser


# When `import x` (or `from x import ...`) has no entry for `x` in the
# caller-supplied module_map, this is the last place searched for
# `x.hny` - after module_map itself, and after the directory of the
# file actually being checked (see ModuleResolver._find_module_path).
# Computed relative to this file's own location (harmony_model_checker/
# modules/ is this module's own sibling directory) rather than a fixed
# personal path, so it's correct wherever the package itself lives.
DEFAULT_MODULE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modules")


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------

class CheckError:
    """One problem found by the checker, anchored at a character range in
    whatever source produced it (mirrors harmony_parser.py's own ParseResult
    start/end convention, so the same line/col-reporting code can be
    reused for either)."""

    def __init__(self, message, start, end, source_label=None):
        self.message = message
        self.start = start
        self.end = end
        self.source_label = source_label

    def __repr__(self):
        where = self.source_label + ": " if self.source_label else ""
        return "%s%s (%d:%d)" % (where, self.message, self.start, self.end)


# ---------------------------------------------------------------------------
# The global namespace
# ---------------------------------------------------------------------------

class Declaration:
    """One name bound into a whole-program global namespace."""
    __slots__ = ("name", "kind", "start", "end", "module")

    # kind is one of:
    #   "module" - `import m` - m itself now names the imported module
    #   "import" - `from m import n` (or a name resolved out of `from m
    #              import *`) - n now names whatever m exports as n
    #   "const"   - a `const` binding (at any nesting depth)
    #   "def"     - a function declaration (also at any nesting depth;
    #               a function name is a constant, so it competes with
    #               "const" for the same name too)
    #   "builtin" - a `builtin NAME "..."` declaration - behaves exactly
    #               like a function for every restriction below (it's
    #               a name for a callable), just described differently
    def __init__(self, name, kind, start, end, module=None):
        self.name = name
        self.kind = kind
        self.start = start
        self.end = end
        self.module = module


def _describe(decl):
    if decl.kind == "module":
        return "an imported module"
    if decl.kind == "import":
        return "a name imported from '%s'" % decl.module
    if decl.kind == "const":
        return "a constant"
    if decl.kind == "def":
        return "a function"
    if decl.kind == "builtin":
        return "a builtin function"
    if decl.kind == "global":
        return "a shared 'global' variable"
    if decl.kind == "sequential":
        return "a shared 'sequential' variable"
    return decl.kind


# Kinds resolved via the "global_ns" origin (see _resolve_identifier)
# that name something callable-or-shared by address (legal for '?'):
# def/builtin (functions), and global/sequential once promoted (see
# _collect_top_level_shared) - a promoted shared variable is exactly as
# addressable as a block-scoped one, which resolves the same way as a
# local (see _check_question_target's "local" branch). Everything else
# reached via "global_ns" (const/module/import, promoted or not) is not
# - see the module docstring's lvalue-kind taxonomy.
_GLOBAL_NS_ADDRESSABLE_KINDS = {"def", "builtin", "global", "sequential"}

# Kinds resolved via the "global_ns" origin that are mutable (legal as
# an assignment target) - a promoted global/sequential, exactly like a
# block-scoped one. const/module/import/def/builtin are never
# assignable, promoted or not.
_GLOBAL_NS_MUTABLE_KINDS = {"global", "sequential"}


class GlobalNamespace:
    """Accumulates Declarations for one program (or one module being
    resolved on behalf of a wildcard import), flagging any collision as
    soon as it's seen."""

    def __init__(self, source_label="<program>"):
        self.source_label = source_label
        self.declared = {}   # name -> Declaration (the first one seen)
        self.errors = []
        self._native_paired = set()   # names whose one builtin+def pairing
                                       # (see declare below) has already
                                       # been used up - a further def or
                                       # builtin of the same name after
                                       # that is a real duplicate again

    def declare(self, name, kind, start, end, module=None):
        existing = self.declared.get(name)
        if existing is None:
            self.declared[name] = Declaration(name, kind, start, end, module)
            return
        # Re-importing the very same thing a second time is a harmless,
        # idempotent no-op - not a shadowing violation - so it's the one
        # exception to "every second declaration of a name is an error".
        # This covers `import x` twice, `from x import a` twice, and a
        # repeated `from x import *` (which, once resolved, re-declares
        # the same name/kind/module triple as the first time) - but only
        # for the two import-derived kinds, keyed on the same name coming
        # from the same module; a repeated `const`/`def` of the same name
        # is a real duplicate declaration regardless of module (they have
        # none), so it must still fall through to the error below.
        if kind in ("module", "import") and existing.kind == kind and existing.module == module:
            return
        # A `def` paired with a `builtin` of the same name (in either
        # order) is a common, intentional Harmony idiom: the `def` gives
        # a reference implementation the model checker can reason about,
        # and the `builtin` gives a native implementation of the exact
        # same function for efficiency - not a collision. Allowed exactly
        # once each way per name; a THIRD declaration of that name (a
        # second def, or a second builtin) is still a real duplicate.
        if ({existing.kind, kind} == {"def", "builtin"}
                and name not in self._native_paired):
            self._native_paired.add(name)
            return
        self.errors.append(CheckError(
            "'%s' is declared more than once in the global namespace "
            "(first as %s, here as %s) - Harmony does not allow shadowing"
            % (name, _describe(existing), _describe(Declaration(name, kind, start, end, module))),
            start, end, self.source_label))

    def exportable_names(self):
        """The subset of this namespace usable by someone else's
        `from <this module> import *`: non-underscore const/def names.
        Imported names and module names are never re-exported this way,
        matching "only functions and constants can be exported from a
        module, and only if they don't start with _"."""
        return {
            name for name, decl in self.declared.items()
            if decl.kind in ("const", "def") and not name.startswith('_')
        }


# ---------------------------------------------------------------------------
# Pulling identifier leaves out of a `bound` / `tuple_bound` pattern
# (`const (a, b) = (1, 2)`, `def f(a, (b, c)):`, etc.)
# ---------------------------------------------------------------------------

def _bound_names(bound):
    """Every identifier ParseResult at a leaf of a bound/tuple_bound
    pattern, left to right. An empty '()' or '[]' contributes nothing."""
    if bound.type == "identifier":
        return [bound]
    if bound.type == "tuple_bound":
        if isinstance(bound.value, list):   # the empty '()'/'[]' case
            return []
        return _bound_names(bound.value)
    if bound.type == "bound":
        names = []
        for part in bound.value:
            names.extend(_bound_names(part))
        return names
    return []


def _flatten_one_line(stmt):
    """one_line_stmt's value is a right-leaning (stmt,) / (stmt, rest)
    tuple (the tail itself a nested one_line_stmt); flatten it into the
    list of simple_stmt results it chains together, left to right."""
    if len(stmt.value) == 1:
        return [stmt.value[0]]
    head, rest = stmt.value
    return [head] + _flatten_one_line(rest)


# ---------------------------------------------------------------------------
# The walker. This descends into *every* statement of a program,
# including every nested block of every compound statement (if/elif/else,
# while, for, let/when, def, atomically) - because a `const` or `def` is
# global no matter how deep it's textually nested. It only ever collects
# import/const/def declarations; var/let/param/for/lambda-bound names are
# local and belong to Phase 2.
# ---------------------------------------------------------------------------

def _walk_simple_stmt(s, ns):
    if s.type == "simple_stmt":
        # An 'atomically'-prefixed simple statement: unwrap and recurse.
        _, inner = s.value
        _walk_simple_stmt(inner, ns)
        return
    if s.type == "const_assign_stmt":
        bound, rhs = s.value
        for name in _bound_names(bound):
            ns.declare(name.value, "const", name.start, name.end)
        return
    if s.type == "builtin_stmt":
        # `builtin NAME "..."` names a callable exactly like `def` does -
        # global, and competes with const/def/import/module for the name.
        name, impl = s.value
        ns.declare(name.value, "builtin", name.start, name.end)
        return
    # var_stmt, global_stmt, assign_stmt, aug_assign_stmt, expr_stmt, and
    # everything else are local/runtime concerns, out of scope for Phase 1.


def _walk_import(imp, ns, resolver):
    stmt = imp.value   # an "import_name" or "import_from" ParseResult
    if stmt.type == "import_name":
        for name in stmt.value.value:   # import_names_seq's list of identifiers
            ns.declare(name.value, "module", name.start, name.end, module=name.value)
        return
    # import_from
    mod, names = stmt.value
    if names == "*":
        exported, sub_errors = resolver.resolve_wildcard(mod.value, mod.start, mod.end)
        ns.errors.extend(sub_errors)
        for name in sorted(exported):
            ns.declare(name, "import", mod.start, mod.end, module=mod.value)
    else:
        for name in names.value:
            sub_errors = resolver.resolve_named_import(mod.value, name.value, name.start, name.end)
            ns.errors.extend(sub_errors)
            # Still declare the name even when it failed to resolve -
            # namespace-collision checking and downstream Phase 2
            # resolution should stay sane rather than treating a
            # reported-bad import as though it never happened.
            ns.declare(name.value, "import", name.start, name.end, module=mod.value)


def _walk_compound(compound, ns, resolver):
    if compound.type == "compound_stmt":
        # An 'atomically'-prefixed compound statement: unwrap and recurse.
        _, inner = compound.value
        _walk_compound(inner, ns, resolver)
        return
    if compound.type == "if_block":
        cond, body, elifs, else_block = compound.value
        _walk_block(body, ns, resolver)
        for e in elifs:
            _, ebody = e.value
            _walk_block(ebody, ns, resolver)
        if else_block is not None:
            _walk_block(else_block.value, ns, resolver)
        return
    if compound.type == "while_block":
        cond, body = compound.value
        _walk_block(body, ns, resolver)
        return
    if compound.type == "for_block":
        it, body = compound.value
        _walk_block(body, ns, resolver)
        return
    if compound.type == "let_when_block":
        decls, body = compound.value
        # `let` is a *local* immutable binding (const's local counterpart)
        # and `when` binds nothing at global scope either - neither
        # belongs in the global namespace, so decls itself is skipped.
        _walk_block(body, ns, resolver)
        return
    if compound.type == "method_decl":
        name, params, returns, body = compound.value
        ns.declare(name.value, "def", name.start, name.end)
        _walk_block(body, ns, resolver)
        return
    if compound.type == "atomic_block":
        _walk_block(compound.value, ns, resolver)
        return


def _walk_block(block, ns, resolver):
    if block.type == "one_line_stmt":
        for s in _flatten_one_line(block):
            _walk_simple_stmt(s, ns)
    elif block.type == "normal_block":
        for stmt in block.value:
            _walk_stmt(stmt, ns, resolver)


def _walk_stmt(stmt, ns, resolver):
    kind = stmt.value[0]
    if kind == "blank":
        return
    if kind == "simple":
        _, prefix, one_line = stmt.value
        for s in _flatten_one_line(one_line):
            _walk_simple_stmt(s, ns)
        return
    if kind == "compound":
        _, prefix, compound = stmt.value
        _walk_compound(compound, ns, resolver)
        return
    if kind == "import":
        _, prefix, imp = stmt.value
        _walk_import(imp, ns, resolver)
        return
    if kind == "labeled_block":
        _, prefix, block = stmt.value
        _walk_block(block, ns, resolver)
        return


# ---------------------------------------------------------------------------
# Resolving `from x import *` by parsing x's own source.
# ---------------------------------------------------------------------------

class ModuleResolver:
    """Resolves wildcard imports against an externally-supplied
    module-name -> file-path map, fully recursively: a module reached
    only through someone else's `import *` may itself `import *`
    something else, and its own global namespace needs to be valid (and
    fully expanded) before we can know what it exports. Results are
    cached per module name; a module reached again via another cycle in
    the wildcard-import graph is not re-parsed.

    A module name not found in module_map isn't immediately an error:
    two further, fixed locations are tried, in order - `<name>.hny`
    next to the file actually being checked (`source_dir`), then
    `<name>.hny` in DEFAULT_MODULE_DIR (Harmony's own bundled modules,
    overridable via `default_module_dir` mainly so tests don't have to
    depend on a real path on one particular machine) - so an ordinary
    `import synch` just works without a caller needing to spell out a
    module_map entry for every standard module."""

    def __init__(self, module_map, source_dir=None, default_module_dir=DEFAULT_MODULE_DIR):
        self.module_map = module_map or {}
        self.source_dir = source_dir
        self.default_module_dir = default_module_dir
        self._cache = {}       # module name -> GlobalNamespace
        self._in_progress = set()

    def _find_module_path(self, module_name):
        """Where module_name's source actually lives, trying module_map
        first (an explicit override always wins), then source_dir, then
        default_module_dir - the first candidate that exists on disk as
        a file wins. Returns None if none of them do."""
        if module_name in self.module_map:
            return self.module_map[module_name]
        for directory in (self.source_dir, self.default_module_dir):
            if directory is None:
                continue
            candidate = os.path.join(directory, module_name + ".hny")
            if os.path.isfile(candidate):
                return candidate
        return None

    def resolve_wildcard(self, module_name, start, end):
        """Returns (exported_names, errors) - errors found while parsing
        and checking that module's own global namespace, if any; a
        problem here doesn't stop the caller's own check, it's just
        folded into the same flat error list."""
        context = "from %s import *" % module_name
        ns, errors = self._resolve_module(module_name, start, end, context)
        if ns is None:
            return set(), errors
        return ns.exportable_names(), errors

    def resolve_named_import(self, module_name, imported_name, start, end):
        """Resolve `from module_name import imported_name` (one specific
        name, not '*'): confirm module_name is itself resolvable via
        module_map, AND that imported_name is actually one of its
        exportable const/def names (only non-underscore const/def names
        are exportable at all - see GlobalNamespace.exportable_names).
        Returns a list of errors, empty if the import checks out."""
        context = "from %s import %s" % (module_name, imported_name)
        ns, errors = self._resolve_module(module_name, start, end, context)
        if ns is None:
            return errors
        if imported_name not in ns.exportable_names():
            return errors + [CheckError(
                "cannot resolve '%s': module '%s' has no exported constant "
                "or function named '%s' (only non-underscore const/def "
                "names are exportable)" % (context, module_name, imported_name),
                start, end)]
        return errors

    def _resolve_module(self, module_name, start, end, context):
        if module_name in self._cache:
            return self._cache[module_name], []
        if module_name in self._in_progress:
            # A cycle in the wildcard-import graph (A imports * from B,
            # B (transitively) imports * from A). Whatever A exports
            # isn't known yet at this point in resolving B, so this link
            # simply contributes nothing new; A's own errors, if any,
            # are still reported once, from A's own top-level resolution.
            return None, []

        path = self._find_module_path(module_name)
        if path is None:
            tried = []
            if self.source_dir is not None:
                tried.append("no '%s.hny' next to the file being checked (%s)"
                              % (module_name, self.source_dir))
            if self.default_module_dir is not None:
                tried.append("no '%s.hny' in %s"
                              % (module_name, self.default_module_dir))
            detail = "; ".join(["module_map has no entry for it"] + tried)
            return None, [CheckError(
                "cannot resolve '%s': no file is known for module '%s' (%s)"
                % (context, module_name, detail),
                start, end)]

        try:
            with open(path, 'r') as f:
                source = f.read()
        except OSError as e:
            return None, [CheckError(
                "cannot resolve '%s': could not read '%s' (%s)"
                % (context, path, e.strerror or e), start, end)]

        program = harmony_parser.parse_program(source)
        if not program.success:
            return None, [CheckError(
                "module '%s' (%s) does not parse: %s"
                % (module_name, path, program.value), start, end)]

        self._in_progress.add(module_name)
        try:
            ns = GlobalNamespace(path)
            for stmt in program.value:
                _walk_stmt(stmt, ns, self)
        finally:
            self._in_progress.discard(module_name)

        self._cache[module_name] = ns
        return ns, list(ns.errors)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def check_global_namespace(document, module_map=None, source_label="<program>", source_dir=None,
                            default_module_dir=DEFAULT_MODULE_DIR, extra_consts=None):
    """Phase 1: parse `document` as a whole Harmony program and check
    whole-program global-namespace uniqueness across import/from-import/
    const/def, at any nesting depth, including full recursive resolution
    of any `from x import *`/`from x import name` - via `module_map`
    (module name -> source file path) first, then falling back to
    `source_dir` (the directory of the file actually being checked) and
    finally DEFAULT_MODULE_DIR, in that order (see ModuleResolver).
    `source_dir` defaults to the directory of `source_label` itself
    (every real caller already passes the file's own path as
    source_label) whenever that's been given its own real value rather
    than left at its own placeholder default.

    `extra_consts` (optional) is an iterable of names a CALLER has
    already bound as constants before this document was ever read - the
    harmony CLI's own `-c NAME=VALUE` flag is exactly this. Real
    Harmony's `-c` does NOT create a new global binding: it only
    *overrides the value* of a `const NAME = ...` statement the program
    already writes (see ConstAST.set in harmony/ast.py - the
    command-line value is substituted in only when compiling a `const`
    statement whose own lexeme matches; a `-c` name with no matching
    `const` in the source is simply never consulted, and the real
    compiler rejects it as unused). So a `-c` name that matches an
    existing `const NAME = ...` in the program is not a collision at
    all - it's the ordinary, single, in-source declaration, just with
    its value overridden - and must NOT be pre-declared here (doing so
    would make the program's own real `const` statement look like a
    second, duplicate declaration of the same name, which is exactly
    wrong). Each name is instead only added, as a fallback, once the
    document has been fully walked and turns out to have no `const` of
    that name anywhere at the top level - permissive rather than
    flagging a "not declared" error checker.py can't fully verify
    (module resolution may simply have missed it), matching the rest of
    this checker's stance of never blocking on something it isn't sure
    the real compiler would also reject.

    Always returns a GlobalNamespace; check `.errors` for problems
    rather than expecting an exception - a parse failure is reported as
    the (only) error, with nothing further to check."""
    ns = GlobalNamespace(source_label)
    program = harmony_parser.parse_program(document)
    if not program.success:
        ns.errors.append(CheckError(
            "program does not parse: %s" % (program.value,),
            program.start, program.end, source_label))
        return ns
    if source_dir is None and source_label != "<program>":
        source_dir = os.path.dirname(os.path.abspath(source_label))
    resolver = ModuleResolver(module_map, source_dir=source_dir, default_module_dir=default_module_dir)
    for stmt in program.value:
        _walk_stmt(stmt, ns, resolver)
    for name in (extra_consts or ()):
        if name not in ns.declared:
            ns.declare(name, "const", -1, -1)
    return ns


# ===========================================================================
# Phase 2: per-function local namespaces, and the '?'/assignment-target
# lvalue-kind restrictions that resolve against them (see the module
# docstring for the full rules).
#
# Every name used anywhere in a Harmony program must be declared
# somewhere reachable from that use, before that use, in the scope where
# it's used - there is no implicit-global fallback any more. Three
# different declaration lifetimes give that "reachable, before use" its
# actual shape:
#   - param/returns are "persistent": bound at the function's own
#     signature, before its body even starts, so trivially in scope for
#     the body's entire extent.
#   - var/for/let/lambda/exists/global/sequential are "block"-scoped:
#     live only from their own point of declaration to the end of their
#     own enclosing construct (var's/global's/sequential's own
#     "construct" being simply whatever block directly contains them -
#     an if/elif/else/while/atomically body, a let/for's own body, or
#     the function's own top-level body - since EVERY block gets its
#     own frame here, not just for/let/lambda/comprehension's bespoke
#     ones). So two SIBLING (non-nested) block declarations may freely
#     reuse a name - two 'var x' in an if's two branches, say - and it's
#     illegal shadowing only when one is textually NESTED inside another
#     still-open block scope (or inside a persistent declaration's
#     whole-function scope) - see FunctionScope for the one further
#     exception this gives global/sequential (repeating the exact same
#     declaration is a harmless restatement, not a shadow).
#   - a `global`/`sequential`/`const`/`import`/`from` statement written
#     directly, unnested, in the program's own top-level statement list
#     is instead promoted into a second whole-program namespace
#     (program.promoted) - see _collect_top_level_shared. It gets the
#     same declared-before-use ordering as an ordinary block-scoped
#     declaration (never def/builtin's full hoisting), since Harmony has
#     no closures to make a top-level name function-local otherwise, and
#     this is the one case where that would make an ordinarily-shared
#     name needlessly hard to actually use.
#
# This runs as four passes over the whole program, in order, because
# def/builtin (Phase 1's global namespace, restricted to those two
# kinds) and program.promoted both allow forward references - a name may
# be used before the statement that declares it, PROVIDED it's a
# 'def'/'builtin' (fully hoisted, so mutual recursion between functions
# works regardless of order); a promoted global/sequential/const/import/
# module still needs its own declared-before-use check, just a program-
# wide one instead of a per-scope one, since Harmony has no closures to
# make it scope-local (see _resolve_identifier) - so no single top-to-
# bottom walk can safely resolve it against a name until every such
# declaration, from anywhere in the program, is already known:
#
#   Pass 1 (_collect_top_level_shared) makes one shallow scan of just the
#     program's own top-level statement list (not descending into any
#     nested block or function body) to promote each direct, unnested
#     `global`/`sequential`/`const`/`import`/`from` statement it finds
#     there into program.promoted, before anything else runs - mirroring
#     why Phase 1 (const/import/def) already has to be fully known
#     before any of this starts.
#
#   Pass 2 (_process_top_level / _process_function, via _collect_locals_*)
#     builds one FunctionScope per function (the implicit top-level one,
#     plus one per `def`, found at any nesting depth), declaring
#     param/returns as persistent and var/for/let/lambda/exists/global/
#     sequential as block declarations in a real lexical scope stack
#     (`block_stack`, threaded through the recursive descent) - this
#     still happens for EVERY global/sequential statement, promoted or
#     not, so a promoted one's own immediately-following top-level code
#     (and any function that chooses to restate it) resolves exactly as
#     it would if it hadn't been promoted at all. const/import are
#     deliberately NOT registered here (see _collect_locals_simple/
#     _collect_locals_stmt) - Phase 1's own uniqueness check plus Pass
#     3 below already catch every conflict they could have; only Pass 4
#     actually needs them in a scope's block_stack, to resolve reads.
#     Either way, `scope.locals` ends up holding one flat, representative
#     declaration per distinct name - Pass 3 only ever needs that flat
#     view, not the scope stack itself. As a side effect, this pass
#     also tracks the one thing that's still genuinely program-wide
#     about EVERY global/sequential declaration, promoted or not: which
#     of the two kinds a name was first claimed as anywhere
#     (program.global_kinds), so the same name can't be 'global' in one
#     place and 'sequential' in another.
#
#   Pass 3 (_check_shadowing) now that every scope's pool is complete,
#     checks each local against the two program-wide things it must
#     never collide with: the Phase 1 global namespace (const/import/
#     def/builtin/module), and program.promoted (a local of any OTHER
#     kind than global/sequential can't reuse a promoted global/
#     sequential name; a matching global/sequential restatement is
#     exempt, as always - a promoted const/import/module is already
#     covered by the first check, since it's always also in Phase 1's
#     own namespace).
#
#   Pass 4 (_check_occ_in_scope, via _check_occ_* / _check_expr) walks
#     every expression in every scope's own body, resolving each name it
#     reads there against block_stack/persistent/promoted/global_ns, in
#     that order (see _resolve_identifier) - anything left unexplained
#     is now an unconditional error, not a warning - and applying the
#     '?' / assignment-target restrictions at every '?' and every
#     assignment/aug-assignment target found. This is also where
#     const/import/from finally join block_stack (see
#     _check_occ_simple's const_assign_stmt case and _check_occ_stmt's
#     "import" case), reusing Phase 1's own already-resolved Declaration
#     objects directly rather than building new ones.
# ===========================================================================

_MUTABLE_LOCAL_KINDS = {"var", "returns", "global", "sequential"}

_LOCAL_KIND_DESCRIPTIONS = {
    "var": "a local variable",
    "let": "a local constant",
    "param": "a parameter",
    "for": "a for-loop-bound name",
    "lambda": "a lambda parameter",
    "exists": "an existential-bound name (from 'when exists')",
    "returns": "a named return variable",
    "global": "this function's own 'global' declaration",
    "sequential": "this function's own 'sequential' declaration",
}


class LocalDeclaration:
    """One name bound into a single function's own flat local pool."""
    __slots__ = ("name", "kind", "start", "end")

    def __init__(self, name, kind, start, end):
        self.name = name
        self.kind = kind
        self.start = start
        self.end = end

    @property
    def mutable(self):
        return self.kind in _MUTABLE_LOCAL_KINDS


def _describe_local(decl):
    return _LOCAL_KIND_DESCRIPTIONS.get(decl.kind, decl.kind)


class FunctionScope:
    """One function's (or the implicit top-level program's) own local
    namespace, plus enough of its own AST to be walked again in Pass 4
    once every scope's pool is known. `body` is a tagged tuple:
    ("block", block_result) for a real `def`, ("stmts", [stmt, ...]) for
    the top-level program (which has no enclosing block syntax).

    Two different lifetimes share this one namespace:
      - "persistent" declarations (param/returns only) are live for the
        WHOLE function, wherever they're textually written - they're
        bound at the function's signature, before its body (the block)
        even starts, so trivially visible for the body's entire extent;
        Harmony has no way to write one anywhere else, so there's no
        notion of "before its declaration" for these to violate.
      - "block" declarations (var/for/let/lambda/exists/global/
        sequential) are live only from their own point of declaration
        to the end of their own enclosing construct - which, for
        for/let/lambda/exists, is their own body/expression, but for
        `var`/`global`/`sequential` is simply whatever block directly
        contains them (an if/elif/else/while/atomically body, a
        let/for's own body, or the function's own top-level body).
        EVERY block gets its own frame (see
        _collect_locals_block/_check_occ_block), so all of these behave
        alike: visible for the rest of their own enclosing block
        (including any blocks nested inside the remainder of it, but
        NOT to a sibling block - the other branch of an if/else, say -
        and NOT beyond the enclosing block's own end, and NOT to
        anything textually before the declaration in that same block).
        Two sibling, non-nested block declarations (two 'var x' in an
        if's two branches, two separate 'for' loops, a 'for' next to an
        unrelated 'let', etc.) may freely reuse the same name, and it's
        only illegal when one is textually NESTED inside another
        still-open block scope (or inside a persistent declaration's
        whole-function scope) - real shadowing, not mere reuse.
        'global'/'sequential' get one further exception to this, in
        declare_shared below: repeating the SAME name with the SAME
        kind anywhere in the currently-open chain of frames is a
        harmless restatement, not a shadow - see declare_shared.

    `locals` ends up holding ONE flat, representative entry per
    distinct name seen anywhere (used only to describe a name's *kind*
    once Pass 4 already knows it's in scope at some occurrence - since
    for/let/lambda/exists/var are all equally read-only except var,
    it's the MUTABILITY check, not this dict, that ultimately decides
    what's legal - see _MUTABLE_LOCAL_KINDS). `persistent` holds only
    the param/returns ones, which - unlike a block declaration - are
    genuinely visible from anywhere in the function. Actually
    determining whether a given *occurrence* of a block-declared name
    is in scope at all is Pass 4's job, via its own block_stack built
    while walking the body (see _resolve_identifier) - `locals` alone
    can't answer that, since it has no notion of textual extent."""

    def __init__(self, label, start, body, parent=None):
        self.label = label
        self.start = start
        self.body = body
        self.parent = parent   # the enclosing FunctionScope this one was
                                 # found nested inside (None for the
                                 # top-level program) - see
                                 # program.def_scopes/_scope_reachable,
                                 # which walk this chain to decide where a
                                 # nested def can be called from
        self.locals = {}       # every declared name -> a representative LocalDeclaration
        self.persistent = {}   # param/returns only -> LocalDeclaration

    def _shadow_error(self, name, existing, kind, start, end, program):
        program.errors.append(CheckError(
            "'%s' is declared more than once in %s "
            "(first as %s, here as %s) - Harmony does not allow shadowing"
            % (name, self.label, _describe_local(existing),
               _describe_local(LocalDeclaration(name, kind, start, end))),
            start, end))

    def declare_persistent(self, name, kind, start, end, program):
        """param/returns: whole-function lifetime."""
        if name == "_":
            return   # '_' is a throwaway placeholder - see declare_block
        existing = self.locals.get(name)
        if existing is not None:
            self._shadow_error(name, existing, kind, start, end, program)
            return
        decl = LocalDeclaration(name, kind, start, end)
        self.locals[name] = decl
        self.persistent[name] = decl

    def declare_block(self, block_stack, name, kind, start, end, program):
        """var/for/let/lambda/exists: lives only in block_stack[-1] (the
        frame for this construct's own extent - for `var`, simply
        whatever block directly contains it, since every block pushes
        its own frame), and conflicts only with a persistent (whole-
        function) declaration, or with the same name already open in an
        ANCESTOR frame (block_stack includes the current, still-being-
        filled frame, so two names introduced together by the same
        construct - e.g. 'for i:i in ...' - are caught too) - never
        with an already-closed sibling's.

        '_' is exempt from all of this: it's Harmony's conventional
        throwaway/placeholder name (a bound position whose value is
        never meant to be used), so it never actually declares
        anything here - it can be bound as many times, in as many
        nested or sibling positions, as a program likes, and is never
        added to any frame or to `locals` (see _resolve_identifier for
        its matching exemption from every occurrence-side rule too)."""
        if name == "_":
            return
        existing = self.persistent.get(name)
        if existing is not None:
            self._shadow_error(name, existing, kind, start, end, program)
            return
        for frame in block_stack:
            existing = frame.get(name)
            if existing is not None:
                self._shadow_error(name, existing, kind, start, end, program)
                return
        decl = LocalDeclaration(name, kind, start, end)
        block_stack[-1][name] = decl
        self.locals.setdefault(name, decl)

    def declare_shared(self, block_stack, name, kind, start, end, program):
        """global/sequential: block-scoped exactly like declare_block
        (visible from here to the end of THIS block, including anything
        nested inside the remainder of it - see the class docstring) -
        but, unlike var/for/let/lambda/exists, restating the SAME
        global/sequential declaration again (same name, same kind)
        anywhere in the currently-open chain of frames is a harmless
        no-op, not a shadow error: it's simply reasserting the same fact
        about the one shared variable (Python's own 'global x' can be
        repeated freely for the same reason). Declaring the SAME name
        with the OTHER kind anywhere in that same chain, though, is a
        real contradiction - they're two different, mutually exclusive
        claims about the one shared variable - and gets its own,
        specific message rather than the generic shadow one. Any other
        kind found in the chain (a persistent param/returns, or a
        var/for/let/lambda/exists block declaration) is still ordinary
        shadowing."""
        if name == "_":
            return
        existing = self.persistent.get(name)
        if existing is not None:
            self._shadow_error(name, existing, kind, start, end, program)
            return
        for frame in block_stack:
            existing = frame.get(name)
            if existing is not None:
                if existing.kind == kind:
                    return   # harmless restatement
                if {existing.kind, kind} == {"global", "sequential"}:
                    program.errors.append(CheckError(
                        "'%s' in %s is declared both 'global' and "
                        "'sequential' (first as %s, here as %s) - a "
                        "shared variable must pick one"
                        % (name, self.label, _describe_local(existing),
                           _describe_local(LocalDeclaration(name, kind, start, end))),
                        start, end))
                    return
                self._shadow_error(name, existing, kind, start, end, program)
                return
        decl = LocalDeclaration(name, kind, start, end)
        block_stack[-1][name] = decl
        self.locals.setdefault(name, decl)


class Phase2State:
    """Accumulates everything Phase 2 needs across the whole program: the
    Phase 1 GlobalNamespace (a pure NAMING check - see the module
    docstring), a second, genuinely-program-wide namespace for every
    PROMOTED top-level declaration (promoted - see declare_promoted and
    _collect_top_level_shared), the one program-wide fact still tracked
    about EVERY global/sequential declaration, promoted or not (which
    kind a name was first claimed as - see note_shared_kind), every
    function's own FunctionScope, and the errors/warnings found along
    the way.

    A `global`/`sequential`/`const`/`import`/`from` statement is, by
    default, NOT hoisted into any program-wide namespace of USABLE
    names - each function/scope that wants to touch it must declare it
    itself (see FunctionScope.declare_block/declare_shared, and
    _check_occ_simple/_check_occ_stmt's block-scoped registration of
    const/import), in scope, before its own use, exactly like var/for/
    let. (const/import/module still can't COLLIDE by name outside their
    own scope either way - that's Phase 1's job, unconditional,
    unaffected by any of this.) The one exception is `promoted`: one of
    these written directly, unnested, in the program's OWN top-level
    statement list is promoted there instead, genuinely usable from
    anywhere (with the same declared-before-use ordering, never def's
    full hoisting) precisely because Harmony has no closures to make a
    top-level name function-local otherwise. Either way, the one thing
    that's still separately program-wide about every global/sequential
    declaration is which underlying shared variable it names, so
    global_kinds exists purely to catch the one contradiction that
    implies: the same name claimed 'global' somewhere and 'sequential'
    somewhere else, promoted or not."""

    def __init__(self, global_ns):
        self.global_ns = global_ns
        self.promoted = {}   # name -> Declaration - every declaration
                               # (global/sequential/const/import/module)
                               # written directly, unnested, in the top-
                               # level statement list; see declare_promoted/
                               # _collect_top_level_shared
        self.global_kinds = {}   # name -> "global" or "sequential", whichever
                                   # kind FIRST claimed it anywhere in the program
        self.def_scopes = {}   # def name -> the FunctionScope it's lexically
                                 # nested directly inside (the top-level
                                 # scope, for one written at the top level) -
                                 # see _collect_locals_compound's method_decl
                                 # case and _resolve_identifier's def-
                                 # reachability check
        self.errors = []
        self.warnings = []
        self.scopes = []

    def declare_promoted(self, name, kind, start, end, module=None):
        """Record one declaration written directly, unnested, in the
        program's own top-level statement list (see
        _collect_top_level_shared) - promoted, genuinely usable from
        anywhere in the program (subject to declared-before-use
        ordering - see _resolve_identifier), unlike an ordinary block-
        scoped one. The FIRST such statement for a given name is what
        its declared-before-use ordering is measured against; restating
        the same name with the SAME kind again, elsewhere at the top
        level, is a harmless no-op (matching FunctionScope.declare_shared's
        own tolerance for global/sequential; for const/import/module,
        a genuinely conflicting restatement is Phase 1's own job to
        reject, unconditionally, so nothing further is needed here
        either way). A global/sequential restatement with the OTHER
        kind is a real contradiction, but it's note_shared_kind (called
        alongside this, by _collect_top_level_shared_simple) that
        reports it - this method just leaves the first-seen kind in
        place rather than also reporting its own, second copy of the
        same complaint."""
        if name == "_":
            return
        existing = self.promoted.get(name)
        if existing is None or existing.kind == kind:
            self.promoted.setdefault(name, Declaration(name, kind, start, end, module))

    def note_shared_kind(self, name, kind, start, end):
        """Record that some 'global x'/'sequential x' statement,
        anywhere in the program (promoted to program.promoted or not),
        claims x as a shared variable of this kind - the first call for
        a given name just records it; every later call for that SAME
        name is checked against it, flagging the name being claimed as
        both 'global' somewhere and 'sequential' somewhere else. (A
        same-function conflict is also caught, more specifically and
        with its own message, by FunctionScope.declare_shared - this
        covers the cross-scope case that check can't see;
        _already_reported keeps the two from double-reporting the very
        same occurrence.)"""
        existing = self.global_kinds.get(name)
        if existing is None:
            self.global_kinds[name] = kind
        elif existing != kind and not _already_reported(self, start, end):
            self.errors.append(CheckError(
                "'%s' is declared '%s' here, but '%s' elsewhere in the "
                "program - a shared variable must pick one, program-wide"
                % (name, kind, existing), start, end))


# ---------------------------------------------------------------------------
# Resolving a name used somewhere inside one function, and the two
# lvalue-kind restrictions built on top of that resolution.
# ---------------------------------------------------------------------------

# global_ns kinds that are genuinely hoisted - usable anywhere in the
# program regardless of textual position or any declaration of their
# own, since Harmony needs mutual recursion between functions to work
# no matter which is defined first. Every OTHER global_ns kind
# (const/import/module) is, by default, block-scoped exactly like var/
# global/sequential - reachable only via block_stack or program.promoted
# - see _resolve_identifier.
_HOISTED_GLOBAL_NS_KINDS = {"def", "builtin"}


def _scope_reachable(from_scope, declaring_scope):
    """True if `declaring_scope` is `from_scope` itself, or a (lexical)
    ancestor of it - i.e. `from_scope` is the very function a nested def
    was found directly inside, or is itself nested (to any depth, and
    however many further defs deep) inside that same function. Walks
    `from_scope`'s own `parent` chain (see FunctionScope/
    _collect_locals_compound's method_decl case) looking for
    `declaring_scope`; the top-level program's own scope has no parent,
    so a def declared there is found by every scope's chain eventually -
    unaffected, still fully hoisted program-wide."""
    s = from_scope
    while s is not None:
        if s is declaring_scope:
            return True
        s = s.parent
    return False


def _resolve_identifier(name, start, end, scope, block_stack, program):
    """Classify one identifier occurrence inside `scope`'s function, at
    the point in its body reached by `block_stack` (the same shape Pass
    1 built: the list of currently-open block frames, innermost last -
    see FunctionScope). Returns (origin, info):
      ("wildcard", None)           - the name is '_', Harmony's
                                      conventional throwaway/placeholder
                                      - exempt from every rule below,
                                      whatever bound position it came
                                      from (see declare_block)
      ("local", LocalDeclaration or Declaration)
                                    - a persistent (param/returns)
                                      declaration, or a block (var/for/
                                      let/lambda/exists/global/
                                      sequential/const/import/module) one
                                      whose construct is still open here -
                                      the ACTUAL declaration in effect at
                                      this occurrence, taken from
                                      whichever frame matched (never
                                      scope.locals's arbitrary "first
                                      seen anywhere" representative,
                                      which could be a different, only
                                      textually-sibling declaration with
                                      a different - possibly less
                                      mutable - kind). A block-scoped
                                      const/import/module is stored here
                                      as a raw Declaration (Phase 1's own
                                      object for that name, reused as-is
                                      - see _check_occ_simple/
                                      _check_occ_stmt) rather than a
                                      LocalDeclaration, since it carries
                                      `.module` and has no `.mutable`
                                      property - callers must check
                                      `info.kind` before ever touching
                                      `.mutable`.
      ("global_ns", Declaration)   - either program.promoted (a
                                      global/sequential/const/import/
                                      module written directly, unnested,
                                      in the program's own top-level
                                      statement list - see
                                      _collect_top_level_shared) or
                                      Phase 1's own global namespace
                                      restricted to "def"/"builtin"
                                      (_HOISTED_GLOBAL_NS_KINDS) - the
                                      only two kinds genuinely usable
                                      from anywhere in the program with
                                      no declaration of their own at all:
                                      "builtin" unconditionally (fully
                                      hoisted, so mutual recursion works
                                      regardless of order), and "def"
                                      too PROVIDED it's actually reachable
                                      from here - a `def` written at the
                                      top level is just as unconditionally
                                      hoisted as a builtin, but one
                                      nested inside some function F is
                                      only callable from F itself, or
                                      from another def nested (to any
                                      depth) inside F - never from
                                      outside F, even though it shares
                                      Phase 1's one flat whole-program
                                      namespace for NAMING purposes (see
                                      _scope_reachable/program.def_scopes).
                                      A promoted entry (of any kind) gets
                                      the ordinary declared-before-use
                                      check instead of def's full
                                      hoisting: an occurrence textually
                                      before that name's own top-level
                                      statement is an error program-wide,
                                      function bodies included - Harmony
                                      has no closures to make a top-level
                                      name function-local otherwise, but
                                      it still has to be declared
                                      somewhere before it's read.
      ("undeclared", None)         - nothing above explains this
                                      occurrence, reported right here,
                                      unconditionally. This is also what
                                      a const/import/module found in
                                      Phase 1's namespace, but neither
                                      promoted nor declared anywhere in
                                      this scope's own block_stack,
                                      resolves to - being part of Phase
                                      1's flat NAMING namespace does NOT,
                                      by itself, make a name usable here;
                                      only def/builtin get that for free.

    Every name must be declared somewhere reachable from this point -
    Harmony has no implicit-global fallback: an identifier matching
    none of the above (including a block declaration whose construct
    has already closed by this point, a global/sequential/const/import/
    module declared only in some OTHER function or block and never
    promoted, or a `def` nested in some function this occurrence isn't
    inside) is an unconditional error, reported right here."""
    if name == "_":
        return "wildcard", None
    for frame in block_stack:
        if name in frame:
            return "local", frame[name]
    if name in scope.persistent:
        return "local", scope.persistent[name]
    if name in program.promoted:
        info = program.promoted[name]
        if start < info.start and not _already_reported(program, start, end):
            # _already_reported guards against double-reporting the same
            # occurrence when it's visited twice for two different
            # reasons - e.g. a '?'-operand's head is resolved once by
            # _check_question_target and then again when _check_expr
            # re-walks the same node (see _already_reported's docstring).
            program.errors.append(CheckError(
                "'%s' is used here before its declaration (it's %s) - it "
                "must be declared before its first use, anywhere in the "
                "program" % (name, _describe(info)), start, end))
        return "global_ns", info
    if name in program.global_ns.declared:
        info = program.global_ns.declared[name]
        if info.kind in _HOISTED_GLOBAL_NS_KINDS:
            if info.kind == "def" and name not in program.global_ns._native_paired:
                # A def+builtin pairing (see GlobalNamespace.declare) is
                # exempt - that idiom means the name is usable as one
                # unified, fully global callable, whichever of the pair
                # happens to be the one Phase 1 kept as the representative.
                declaring_scope = program.def_scopes.get(name)
                if declaring_scope is not None and not _scope_reachable(scope, declaring_scope):
                    if not _already_reported(program, start, end):
                        program.errors.append(CheckError(
                            "'%s' is not declared in %s - it's a function "
                            "local to %s" % (name, scope.label, declaring_scope.label),
                            start, end))
                    return "undeclared", None
            return "global_ns", info
        # A const/import/module found in Phase 1's flat namespace, but
        # neither promoted nor declared anywhere in this scope's own
        # block_stack - being part of Phase 1's namespace doesn't, on
        # its own, make it usable here (see the module docstring): falls
        # through to the ordinary "not declared" error below, exactly as
        # if it weren't in any namespace at all.
    if not _already_reported(program, start, end):
        program.errors.append(CheckError(
            "'%s' is not declared in %s" % (name, scope.label),
            start, end))
    return "undeclared", None


def _check_question_target(head, scope, block_stack, program):
    """`head` is the identifier at the root of a '?'-operand's
    identifier-headed chain (harmony_parser.py's parse_question_operand already
    guarantees the operand has this shape) - confirm it names a
    function/builtin or a shared variable, per "you can only take the
    address of functions or shared variables"."""
    origin, info = _resolve_identifier(head.value, head.start, head.end, scope, block_stack, program)
    if origin == "wildcard":
        return
    if origin == "local":
        if info.kind in ("global", "sequential"):
            return   # this function's own 'global x'/'sequential x' - a real shared variable
        # A block-scoped const/import/module (info is a raw Declaration
        # here, not a LocalDeclaration - see _resolve_identifier) is
        # described the same way Phase 1 would describe it.
        desc = _describe(info) if info.kind in ("const", "import", "module") else _describe_local(info)
        program.errors.append(CheckError(
            "'?%s' is illegal: %s is %s, not a function or a shared variable - "
            "only functions and shared (global) variables can have their "
            "address taken" % (head.value, head.value, desc),
            head.start, head.end))
        return
    if origin == "global_ns":
        if info.kind in _GLOBAL_NS_ADDRESSABLE_KINDS:
            return
        program.errors.append(CheckError(
            "'?%s' is illegal: %s is %s, not a function or a shared variable - "
            "only functions and shared (global) variables can have their "
            "address taken" % (head.value, head.value, _describe(info)),
            head.start, head.end))
        return
    # "undeclared": _resolve_identifier already reported it - nothing further.


def _check_assign_target_name(head, scope, block_stack, program):
    """Same idea as _check_question_target, for the name an assignment
    (or augmented assignment) actually targets: illegal when it's a
    module/const/function/imported name, or a *read-only* local
    (let/param/for/lambda/exists - only var/returns/global/sequential
    are mutable)."""
    origin, info = _resolve_identifier(head.value, head.start, head.end, scope, block_stack, program)
    if origin == "wildcard":
        return
    if origin == "local":
        if info.kind in ("const", "import", "module"):
            # A block-scoped const/import/module (info is a raw
            # Declaration here, not a LocalDeclaration - see
            # _resolve_identifier) has no `.mutable` property to check.
            program.errors.append(CheckError(
                "cannot assign to '%s': it is %s" % (head.value, _describe(info)),
                head.start, head.end))
            return
        if info.mutable:
            return
        program.errors.append(CheckError(
            "cannot assign to '%s': it is %s, which is read-only"
            % (head.value, _describe_local(info)), head.start, head.end))
        return
    if origin == "global_ns":
        if info.kind in _GLOBAL_NS_MUTABLE_KINDS:
            return   # a promoted top-level 'global x'/'sequential x' - mutable, like any shared variable
        program.errors.append(CheckError(
            "cannot assign to '%s': it is %s" % (head.value, _describe(info)),
            head.start, head.end))
        return
    # "undeclared": _resolve_identifier already reported it - nothing further.
    # (Note: Harmony no longer has an implicit-global default - assigning
    # to an undeclared name is an error now, not a way to introduce one;
    # use 'var'/'global'/'sequential' to actually declare it.)


def _lvalue_head(node):
    """The head identifier of an identifier-headed application/indexing/
    attribute chain, parens transparent - mirrors harmony_parser.py's own
    _is_identifier_headed (which both '?' and assign-target already
    require of their operand at parse time), but returns the actual
    identifier node instead of a bool. None means there's no single
    fixed name to check:
      - a dereference-headed chain like '(!p)[x]' or a bare '!p'
        assign-target - both write through whatever address the
        '!'-expression computes, not through a named slot;
      - an application chain containing an ARROWID ('->') step
        anywhere: 'p->a' is '(!p).a' with sugar - an implicit
        dereference of whatever 'p' (or a longer chain before the
        arrow) evaluates to, followed by indexing into *that* - so
        the address 'p->a...' computes is fresh, through p's own
        VALUE, and has nothing to do with whether p itself is
        addressable (a bare '?p' is still illegal if p is a plain
        local, but '?p->a' addresses a field of whatever p points to,
        which is exactly the point of '->' as opposed to '.').
    Either way, reading the identifiers actually in the chain (`p`
    itself, whatever its kind) is an ordinary read, checked as such by
    _check_expr instead - see harmony_parser.py's own comment on
    _is_identifier_headed for why these shapes are legal in the first
    place."""
    if node.type == "identifier":
        return node
    if node.type == "application":
        if any(part.type == "arrowid" for part in node.value[1:]):
            return None
        head = node.value[0]
        if harmony_parser._is_identifier_headed(head):
            return _lvalue_head(head)
        return None
    if node.type == "paren_tuple":
        inner = node.value
        if isinstance(inner, list) or inner.type == "tuple":
            return None
        return _lvalue_head(inner)
    return None


# ---------------------------------------------------------------------------
# Pass 2: collecting each function's own local declarations (including
# ones buried inside expressions - a comprehension's 'for', or a
# lambda's bound parameter - which participate in the very same flat
# pool as an ordinary var/let/param/for/exists/global declaration).
# ---------------------------------------------------------------------------

def _collect_locals_expr(node, scope, block_stack, program):
    if node is None:
        return
    t = node.type
    if t in ("identifier", "number", "string", "bool", "none", "atom",
             "keyword", "bin_op", "binary_op", "unary_op", "arrowid"):
        return
    if t == "expr_rule":
        op, inner = node.value
        _collect_locals_expr(inner, scope, block_stack, program)
        return
    if t in ("setintlevel", "save", "stop"):
        _collect_locals_expr(node.value, scope, block_stack, program)
        return
    if t == "application":
        for part in node.value:
            _collect_locals_expr(part, scope, block_stack, program)
        return
    if t in ("paren_tuple", "bracket_tuple"):
        if isinstance(node.value, list):
            return
        _collect_locals_expr(node.value, scope, block_stack, program)
        return
    if t == "tuple":
        for item in node.value:
            _collect_locals_expr(item, scope, block_stack, program)
        return
    if t in ("comprehension", "set_comprehension"):
        head, it = node.value
        frame = {}
        _collect_locals_iter_parse(it, scope, block_stack + [frame], program)
        _collect_locals_expr(head, scope, block_stack + [frame], program)
        return
    if t == "dict_comprehension":
        key, val, it = node.value
        frame = {}
        _collect_locals_iter_parse(it, scope, block_stack + [frame], program)
        _collect_locals_expr(key, scope, block_stack + [frame], program)
        _collect_locals_expr(val, scope, block_stack + [frame], program)
        return
    if t == "set":
        for item in node.value:
            _collect_locals_expr(item, scope, block_stack, program)
        return
    if t == "empty_dict":
        return
    if t == "dict":
        for key, val in node.value:
            _collect_locals_expr(key, scope, block_stack, program)
            _collect_locals_expr(val, scope, block_stack, program)
        return
    if t == "range":
        lo, hi = node.value
        _collect_locals_expr(lo, scope, block_stack, program)
        _collect_locals_expr(hi, scope, block_stack, program)
        return
    if t in ("in", "notin"):
        a, b = node.value
        _collect_locals_expr(a, scope, block_stack, program)
        _collect_locals_expr(b, scope, block_stack, program)
        return
    if t == "ifelse":
        a, cond, b = node.value
        _collect_locals_expr(a, scope, block_stack, program)
        _collect_locals_expr(cond, scope, block_stack, program)
        _collect_locals_expr(b, scope, block_stack, program)
        return
    if t == "nary_rule":
        components, operators = node.value
        for c in components:
            _collect_locals_expr(c, scope, block_stack, program)
        return
    if t == "lambda_expr":
        bound, body = node.value
        frame = {}
        for name in _bound_names(bound):
            scope.declare_block(block_stack + [frame], name.value, "lambda", name.start, name.end, program)
        _collect_locals_expr(body, scope, block_stack + [frame], program)
        return
    if t == "set_rule":
        if isinstance(node.value, list):
            return   # the empty '{}' case - ambiguous empty set/dict, no sub-expression
        _collect_locals_expr(node.value, scope, block_stack, program)
        return
    if t == "assign_target_list":
        for item in node.value:
            _collect_locals_expr(item, scope, block_stack, program)
        return
    if t == "assign_target":
        if isinstance(node.value, tuple) and len(node.value) == 2 and node.value[0] == "!":
            _collect_locals_expr(node.value[1], scope, block_stack, program)
        else:
            _collect_locals_expr(node.value, scope, block_stack, program)
        return
    raise AssertionError("checker._collect_locals_expr: unhandled node type %r" % (t,))


def _collect_locals_iter_parse(it, scope, block_stack, program):
    """`block_stack`'s innermost frame is shared across every for_parse/
    where_parse clause of ONE iter_parse - so a later clause can use an
    earlier one's bound name ('for i in A for j in {1..i}'), and
    repeating a name across clauses of the SAME iter_parse is real
    (sequential-dependency) shadowing, not sibling reuse."""
    for clause in it.value:
        if clause.type == "for_parse":
            b1, b2, src = clause.value
            _collect_locals_expr(src, scope, block_stack, program)
            for name in _bound_names(b1):
                scope.declare_block(block_stack, name.value, "for", name.start, name.end, program)
            if b2 is not None:
                for name in _bound_names(b2):
                    scope.declare_block(block_stack, name.value, "for", name.start, name.end, program)
        elif clause.type == "where_parse":
            _collect_locals_expr(clause.value, scope, block_stack, program)


def _collect_locals_simple(s, scope, block_stack, program):
    if s.type == "simple_stmt":
        _, inner = s.value
        _collect_locals_simple(inner, scope, block_stack, program)
        return
    if s.type == "var_stmt":
        # 'var' is block-scoped, not persistent: it declares into the
        # CURRENT innermost frame (whatever block directly contains this
        # statement), visible for the rest of that block onward - not
        # to a sibling block, and not beyond that block's own end. The
        # rhs is processed first, so 'var x = x + 1' reads whatever x
        # meant *before* this declaration, not itself. rhs is None for
        # a bare 'var x' (or 'var x, y', ...) with no '= ...' -
        # harmony_parser.py only allows that for a flat, parenthesis-free list of plain
        # names, uninitialized, exactly like 'global x, y'/'sequential
        # x, y' - so there's nothing to walk here.
        bound, rhs = s.value
        _collect_locals_expr(rhs, scope, block_stack, program)
        for name in _bound_names(bound):
            scope.declare_block(block_stack, name.value, "var", name.start, name.end, program)
        return
    if s.type == "const_assign_stmt":
        # const is global (Phase 1 already collected it) - but its
        # initializer is still textually evaluated in this function's
        # own scope, so still walk it for embedded lambda/comprehension
        # locals.
        bound, rhs = s.value
        _collect_locals_expr(rhs, scope, block_stack, program)
        return
    if s.type == "global_stmt":
        # 'global x' is block-scoped, exactly like 'var x': it declares
        # into the CURRENT innermost frame (whatever block directly
        # contains this statement), visible from here to the end of
        # that block onward - see FunctionScope.declare_shared, which
        # also tolerates repeating the same name/kind (a harmless
        # restatement) and specifically flags the same name being
        # declared 'sequential' elsewhere. note_shared_kind is the one
        # thing that's still program-wide about it: which kind (global
        # or sequential) a name was first claimed as anywhere, purely to
        # catch that same cross-function contradiction.
        for item in s.value:
            if item.type == "identifier":
                scope.declare_shared(block_stack, item.value, "global", item.start, item.end, program)
                program.note_shared_kind(item.value, "global", item.start, item.end)
            else:
                _collect_locals_expr(item, scope, block_stack, program)
        return
    if s.type == "sequential_stmt":
        # 'sequential x' is itself a version of 'global x' - see above.
        for item in s.value:
            scope.declare_shared(block_stack, item.value, "sequential", item.start, item.end, program)
            program.note_shared_kind(item.value, "sequential", item.start, item.end)
        return
    if s.type == "assign_stmt":
        targets, rhs = s.value
        for target in targets:
            _collect_locals_expr(target, scope, block_stack, program)
        _collect_locals_expr(rhs, scope, block_stack, program)
        return
    if s.type == "aug_assign_stmt":
        lhs, op, rhs = s.value
        _collect_locals_expr(lhs, scope, block_stack, program)
        _collect_locals_expr(rhs, scope, block_stack, program)
        return
    if s.type == "expr_stmt":
        _collect_locals_expr(s.value, scope, block_stack, program)
        return
    if s.type == "return_stmt":
        # Harmony has no 'return' statement - it exists in the grammar
        # only so this common Python habit gets its own recognizable
        # node and a specific, on-point error here, instead of either
        # misparsing or (since 'return' would then be an ordinary,
        # never-declared identifier) being silently accepted as a
        # meaningless expression statement. Reported unconditionally,
        # every time, regardless of what's inside it.
        program.errors.append(CheckError(
            "Harmony has no 'return' statement (that's a Python habit) - "
            "give the function a 'returns' name in its signature and "
            "assign the result to that name instead",
            s.start, s.end))
        return
    if s.type in ("break_stmt", "continue_stmt"):
        # Same story as return_stmt: 'break'/'continue' are reserved and
        # have their own grammar productions purely so these Python
        # habits are recognizable here and get a specific error, rather
        # than either misparsing or silently doing nothing (which is
        # what a bare keyword with no expr to check would otherwise
        # mean). Harmony has neither statement - a 'for'/'while' loop
        # runs to completion; use a boolean flag or restructure the
        # loop's condition instead.
        word = "break" if s.type == "break_stmt" else "continue"
        program.errors.append(CheckError(
            "Harmony has no '%s' statement (that's a Python habit) - "
            "there's no way to exit a loop early or skip to its next "
            "iteration; use a boolean flag or restructure the loop's "
            "condition instead" % word,
            s.start, s.end))
        return
    if s.type in ("await_stmt", "trap_stmt", "finally_stmt",
                  "invariant_stmt", "del_stmt"):
        _collect_locals_expr(s.value, scope, block_stack, program)
        return
    if s.type == "spawn_stmt":
        eternal, value = s.value
        _collect_locals_expr(value, scope, block_stack, program)
        return
    if s.type == "go_stmt":
        target, value = s.value
        _collect_locals_expr(target, scope, block_stack, program)
        if value is not None:
            _collect_locals_expr(value, scope, block_stack, program)
        return
    if s.type == "print_stmt":
        value, endpoint = s.value
        _collect_locals_expr(value, scope, block_stack, program)
        if endpoint is not None:
            _collect_locals_expr(endpoint, scope, block_stack, program)
        return
    if s.type == "assert_stmt":
        cond, message = s.value
        _collect_locals_expr(cond, scope, block_stack, program)
        if message is not None:
            _collect_locals_expr(message, scope, block_stack, program)
        return
    # builtin_stmt's name/string is not a general expression (nothing to
    # collect there); pass_stmt carries none
    # at all.


def _collect_locals_stmt(stmt, scope, block_stack, program):
    kind = stmt.value[0]
    if kind == "blank":
        return
    if kind == "simple":
        _, prefix, one_line = stmt.value
        for s in _flatten_one_line(one_line):
            _collect_locals_simple(s, scope, block_stack, program)
        return
    if kind == "compound":
        _, prefix, compound = stmt.value
        _collect_locals_compound(compound, scope, block_stack, program)
        return
    if kind == "import":
        return
    if kind == "labeled_block":
        _, prefix, block = stmt.value
        _collect_locals_block(block, scope, block_stack, program)
        return


def _collect_locals_stmts(stmts, scope, block_stack, program):
    for stmt in stmts:
        _collect_locals_stmt(stmt, scope, block_stack, program)


def _collect_locals_block(block, scope, block_stack, program):
    """Every block - an if/elif/else/while/atomically body, a for/let's
    own body, a function's own top-level body - gets its own fresh
    frame here, which is what gives 'var' its scoping (see FunctionScope
    and _collect_locals_simple's var_stmt handling): a var declared
    directly in this block lives in THIS frame, visible to the rest of
    this block (and anything nested inside the remainder of it, since
    nested blocks extend this same block_stack), but gone once this
    block itself ends - a sibling block (the other branch of an if,
    say) never sees it, because it's never part of that sibling's own
    block_stack at all."""
    frame = {}
    new_stack = block_stack + [frame]
    if block.type == "one_line_stmt":
        for s in _flatten_one_line(block):
            _collect_locals_simple(s, scope, new_stack, program)
    elif block.type == "normal_block":
        _collect_locals_stmts(block.value, scope, new_stack, program)


def _collect_locals_compound(compound, scope, block_stack, program):
    if compound.type == "compound_stmt":
        _, inner = compound.value
        _collect_locals_compound(inner, scope, block_stack, program)
        return
    if compound.type == "if_block":
        cond, body, elifs, else_block = compound.value
        _collect_locals_expr(cond, scope, block_stack, program)
        _collect_locals_block(body, scope, block_stack, program)
        for e in elifs:
            econd, ebody = e.value
            _collect_locals_expr(econd, scope, block_stack, program)
            _collect_locals_block(ebody, scope, block_stack, program)
        if else_block is not None:
            _collect_locals_block(else_block.value, scope, block_stack, program)
        return
    if compound.type == "while_block":
        cond, body = compound.value
        _collect_locals_expr(cond, scope, block_stack, program)
        _collect_locals_block(body, scope, block_stack, program)
        return
    if compound.type == "for_block":
        # The for-loop's bound name(s) and its own body share ONE frame,
        # scoped to this loop's own extent - a sibling for-loop elsewhere
        # in the same function may freely reuse the same bound name (see
        # FunctionScope's docstring), but this loop's own body cannot.
        it, body = compound.value
        frame = {}
        new_stack = block_stack + [frame]
        _collect_locals_iter_parse(it, scope, new_stack, program)
        _collect_locals_block(body, scope, new_stack, program)
        return
    if compound.type == "let_when_block":
        # All of this let/when-block's own decls, plus its body, share
        # ONE frame - a later decl may reference an earlier one's bound
        # name, and repeating a name across decls of this SAME block is
        # real (sequential-dependency) shadowing; a sibling let/when
        # block elsewhere may still freely reuse the same name.
        decls, body = compound.value
        frame = {}
        new_stack = block_stack + [frame]
        for d in decls.value:
            if d.type == "let_decl":
                bound, rhs = d.value
                for name in _bound_names(bound):
                    scope.declare_block(new_stack, name.value, "let", name.start, name.end, program)
                _collect_locals_expr(rhs, scope, new_stack, program)
            elif d.type == "when_decl":
                if d.value[0] == "exists":
                    _, bound, cond = d.value
                    for name in _bound_names(bound):
                        scope.declare_block(new_stack, name.value, "exists", name.start, name.end, program)
                    _collect_locals_expr(cond, scope, new_stack, program)
                else:
                    _, cond = d.value
                    _collect_locals_expr(cond, scope, new_stack, program)
        _collect_locals_block(body, scope, new_stack, program)
        return
    if compound.type == "method_decl":
        # A nested function - its own params/returns/body form a wholly
        # independent scope (no closures), built and checked separately;
        # nothing about it belongs to the CURRENT function's own pool.
        # It's still only CALLABLE from `scope` (the function it's
        # lexically nested directly inside - the top-level program, if
        # this method_decl was found while walking that) and anything
        # nested inside `scope` in turn - see _resolve_identifier's def-
        # reachability check, which walks the new scope's own `parent`
        # chain (set here) back up looking for this one.
        name, params, returns, body = compound.value
        program.def_scopes.setdefault(name.value, scope)
        _process_function(name, params, returns, body, program, scope)
        return
    if compound.type == "atomic_block":
        _collect_locals_block(compound.value, scope, block_stack, program)
        return


def _process_function(name, params, returns, body, program, parent):
    scope = FunctionScope("function '%s'" % name.value, name.start, ("block", body), parent)
    program.scopes.append(scope)
    for p in _bound_names(params):
        scope.declare_persistent(p.value, "param", p.start, p.end, program)
    if returns is not None:
        scope.declare_persistent(returns.value, "returns", returns.start, returns.end, program)
    _collect_locals_block(body, scope, [], program)
    return scope


# ---------------------------------------------------------------------------
# Pass 1: promoting each direct, unnested top-level global/sequential/
# const/import/from statement into program.promoted, before anything
# else runs (see the Phase 2 overview comment above and
# Phase2State.declare_promoted). This is a deliberately SHALLOW scan of
# just the top-level statement list - it does not descend into any
# compound statement's own body (an if/while/for/let/atomically-block,
# or a function), since one of these written there is, precisely, NOT
# one of these: it stays only as block-scoped as it's always been (see
# FunctionScope).
# ---------------------------------------------------------------------------

def _collect_top_level_shared_simple(s, program):
    if s.type == "simple_stmt":
        # An 'atomically'-prefixed simple statement - still directly,
        # unnestedly, a top-level statement (atomically doesn't push a
        # block frame the way an 'atomically:' BLOCK does - see
        # _collect_locals_compound's atomic_block, which does, via
        # _collect_locals_block).
        _, inner = s.value
        _collect_top_level_shared_simple(inner, program)
        return
    if s.type in ("global_stmt", "sequential_stmt"):
        kind = "global" if s.type == "global_stmt" else "sequential"
        for item in s.value:
            if item.type == "identifier":
                program.declare_promoted(item.value, kind, item.start, item.end)
                program.note_shared_kind(item.value, kind, item.start, item.end)
        return
    if s.type == "const_assign_stmt":
        # const is always already in Phase 1's global namespace, fully
        # resolved (kind/start/end) - reuse that Declaration object
        # directly rather than building a new one from scratch.
        bound, rhs = s.value
        for name in _bound_names(bound):
            decl = program.global_ns.declared.get(name.value)
            if decl is not None:
                program.declare_promoted(name.value, decl.kind, decl.start, decl.end, decl.module)
        return
    # builtin_stmt is already fully hoisted (_HOISTED_GLOBAL_NS_KINDS),
    # so it never needs promoting; every other simple_stmt kind has
    # nothing to promote either.


def _import_names(imp, program):
    """Every name a top-level `import`/`from ... import ...` statement
    at least nominally binds - used only to look each one up in
    program.global_ns.declared for promotion (see
    _collect_top_level_shared/_check_occ_stmt): Phase 1 has already
    fully resolved each one's kind/start/end/module there, so nothing
    here needs to be reconstructed. `from x import *` is approximated
    by taking every name Phase 1 ended up recording as an "import" from
    that exact module, since exactly replaying ModuleResolver's own
    wildcard resolution here would just duplicate that work - a
    reasonable approximation that can only ever over-promote a name
    that some OTHER duplicate declaration has already made illegal to
    use anyway, never under-promote or wrongly accept an otherwise-
    invalid program."""
    stmt = imp.value   # an "import_name" or "import_from" ParseResult
    if stmt.type == "import_name":
        return [name.value for name in stmt.value.value]   # import_names_seq's list
    mod, names = stmt.value
    if names == "*":
        return [name for name, decl in program.global_ns.declared.items()
                if decl.kind == "import" and decl.module == mod.value]
    return [name.value for name in names.value]


def _collect_top_level_shared(stmts, program):
    for stmt in stmts:
        kind = stmt.value[0]
        if kind == "simple":
            _, prefix, one_line = stmt.value
            for s in _flatten_one_line(one_line):
                _collect_top_level_shared_simple(s, program)
        elif kind == "import":
            _, prefix, imp = stmt.value
            for name in _import_names(imp, program):
                decl = program.global_ns.declared.get(name)
                if decl is not None:
                    program.declare_promoted(name, decl.kind, decl.start, decl.end, decl.module)
        # "compound" (if/while/for/let/def/atomically-block),
        # "labeled_block", "blank" - none of these is a direct, unnested
        # top-level simple statement, so nothing inside any of them gets
        # promoted, however shallow.


def _process_top_level(stmts, program):
    scope = FunctionScope("the top-level program", 0, ("stmts", stmts))
    program.scopes.append(scope)
    # The top-level program has no wrapping block syntax to go through
    # _collect_locals_block (which is what normally pushes a block's own
    # frame) - so its own top-level frame is pushed explicitly here
    # instead, the same way a function's own top-level body gets one
    # from _collect_locals_block(body, scope, [], program) in
    # _process_function.
    frame = {}
    _collect_locals_stmts(stmts, scope, [frame], program)
    return scope


# ---------------------------------------------------------------------------
# Pass 3: no local may shadow a whole-program global - Phase 1's
# import/const/def/builtin namespace, or a promoted top-level
# global/sequential (program.promoted). A promoted const/import/module
# always duplicates an entry already in program.global_ns.declared, so
# it's always the FIRST branch below that catches any local shadowing
# it - the second branch only ever matters for a promoted
# global/sequential (which Phase 1 never puts in global_ns.declared at
# all), hence its own explicit kind filter. For program.promoted this
# check only ever applies to a scope OTHER than the top-level program
# itself: every promoted entry, by construction, comes FROM some
# top-level statement (see _collect_top_level_shared), so checking it
# against the top-level scope's OWN locals would just be comparing that
# declaration against itself (or a legitimate, textually-SIBLING
# declaration of the same name elsewhere at the top level, which the
# ordinary block-scoping/sibling-reuse rule already allows, and whose
# own real conflicts, if any, are already caught by
# declare_block/declare_shared's frame-chain checks at collection time)
# - program.scopes[0] is always that top-level scope, since
# _process_top_level appends it before any def's own _process_function
# gets a chance to. A DIFFERENT function's own local (var/let/param/
# for/lambda/exists) of the same name, though, is genuinely independent
# of the top-level declaration and would hide it for that function's
# whole extent - a real shadow, exactly like a local shadowing
# import/const/def; a function's own MATCHING global/sequential
# restatement is exempt (the same harmless no-op it's always been), and
# a CONFLICTING one is caught earlier, more specifically, by
# note_shared_kind rather than reported again here.
# ---------------------------------------------------------------------------

def _check_shadowing(program):
    top_level = program.scopes[0] if program.scopes else None
    for scope in program.scopes:
        for name, decl in scope.locals.items():
            if name in program.global_ns.declared:
                gdecl = program.global_ns.declared[name]
                program.errors.append(CheckError(
                    "'%s' in %s shadows %s of the same name - "
                    "Harmony does not allow shadowing"
                    % (name, scope.label, _describe(gdecl)), decl.start, decl.end))
            elif (scope is not top_level and name in program.promoted
                    and program.promoted[name].kind in ("global", "sequential")
                    and decl.kind not in ("global", "sequential")):
                sdecl = program.promoted[name]
                program.errors.append(CheckError(
                    "'%s' in %s shadows %s of the same name - "
                    "Harmony does not allow shadowing"
                    % (name, scope.label, _describe(sdecl)), decl.start, decl.end))


# ---------------------------------------------------------------------------
# Pass 4: walking every expression in every scope's own body, resolving
# every name it reads and applying the '?'/assignment-target lvalue-kind
# restrictions. This walk threads its own `block_stack`, built live as
# it descends - a list of currently-open block frames (innermost last),
# each just a set of the names that construct binds - mirroring Pass
# 2's own block_stack (see FunctionScope) so that a block-declared name
# (var/for/let/lambda/exists/global/sequential) only resolves as "local"
# for occurrences textually within its own construct's still-open
# extent, exactly the way Pass 2 only let it CONFLICT within that same
# extent. An occurrence outside every frame that declares it - even
# later in the very same function - falls through to
# persistent/global_ns, same as if it had never been declared as a
# block name at all; if that doesn't explain it either, it's now an
# unconditional error (see _resolve_identifier), not a warning.
# (Persistent names need no such tracking: they're genuinely visible
# from anywhere in the function, which is exactly why they live in
# `scope.persistent` rather than in any frame.)
# ---------------------------------------------------------------------------


def _already_reported(program, start, end):
    """Whether program.errors already has an entry at exactly this
    (start, end) span - used to avoid reporting the same identifier
    occurrence twice under two different messages when it's visited via
    two different paths for two different reasons (see the 'module used
    as a plain value' check in _check_expr's identifier case, and its
    callers _check_question_target/_check_assign_target_name, which
    both resolve/report a '?'/assign-target's head FIRST and only then
    re-walk the same node as an ordinary expression to reach whatever
    else it contains)."""
    return any(e.start == start and e.end == end for e in program.errors)


def _check_expr(node, scope, block_stack, program):
    if node is None:
        return
    t = node.type
    if t == "identifier":
        origin, info = _resolve_identifier(node.value, node.start, node.end, scope, block_stack, program)
        if (origin in ("local", "global_ns") and info is not None and info.kind == "module"
                and not _already_reported(program, node.start, node.end)):
            # A module name has no runtime value at all in Harmony - it
            # exists purely so 'from m import ...' can resolve it (see
            # ModuleResolver); Harmony has no 'm.attr' syntax to make it
            # useful as one either (unlike '.attr', which is its own
            # atom literal, not attribute access). So a bare module name
            # is illegal absolutely everywhere an ordinary value is
            # expected - not just as a '?'-operand or assignment target,
            # which already have their own, more specific messages
            # (_check_question_target/_check_assign_target_name) - this
            # is the general case those two are narrower instances of.
            # The _already_reported guard is what keeps this from ALSO
            # firing (with a less specific message) when this exact
            # identifier is a '?'/assign-target head that one of those
            # two already reported: both call sites resolve/report the
            # head first and only then re-walk the same node as an
            # ordinary expression (to reach whatever else it contains -
            # an index, a call argument, ...), so the head is genuinely
            # visited twice for two different reasons, not just here.
            program.errors.append(CheckError(
                "'%s' is an imported module, and has no value of its own - "
                "use 'from %s import ...' to bring in specific names instead"
                % (node.value, node.value),
                node.start, node.end))
        return
    if t in ("number", "string", "bool", "none", "atom", "keyword",
             "bin_op", "binary_op", "unary_op", "arrowid"):
        return
    if t == "expr_rule":
        op, inner = node.value
        if op.value == '?':
            head = _lvalue_head(inner)
            if head is not None:
                _check_question_target(head, scope, block_stack, program)
        _check_expr(inner, scope, block_stack, program)
        return
    if t in ("setintlevel", "save", "stop"):
        _check_expr(node.value, scope, block_stack, program)
        return
    if t == "application":
        parts = node.value
        if parts[0].type == "identifier" and len(parts) >= 2 and parts[1].type == "atom":
            # 'name.field...' - Harmony has no general attribute-access
            # syntax; '.field' is its own atom literal, and applying an
            # identifier to one is how BOTH plain record field access
            # ('p.a') AND a module-qualified reference to one of its
            # exports ('bags.empty', 'bags.empty()') are written - the
            # only legitimate way to use a module name at all, since it
            # otherwise has no value (see the "identifier" case below).
            # So resolve the head WITHOUT that bare-module-value check
            # (this doesn't verify 'field' is actually one of the
            # module's exports - only that qualified-access shape
            # itself is fine), then check whatever remains of the chain
            # normally (the atom itself never needs checking).
            _resolve_identifier(parts[0].value, parts[0].start, parts[0].end, scope, block_stack, program)
            for part in parts[2:]:
                _check_expr(part, scope, block_stack, program)
            return
        for part in parts:
            _check_expr(part, scope, block_stack, program)
        return
    if t in ("paren_tuple", "bracket_tuple"):
        if isinstance(node.value, list):
            return
        _check_expr(node.value, scope, block_stack, program)
        return
    if t == "tuple":
        for item in node.value:
            _check_expr(item, scope, block_stack, program)
        return
    if t in ("comprehension", "set_comprehension"):
        # One frame shared by the whole iter_parse AND the head
        # expression - the head can reference any of the iter_parse's
        # own bound names, so it's processed after, with the now-
        # complete frame (mirrors _collect_locals_expr's order).
        head, it = node.value
        frame = {}
        new_stack = block_stack + [frame]
        _check_occ_iter_parse(it, scope, new_stack, program)
        _check_expr(head, scope, new_stack, program)
        return
    if t == "dict_comprehension":
        key, val, it = node.value
        frame = {}
        new_stack = block_stack + [frame]
        _check_occ_iter_parse(it, scope, new_stack, program)
        _check_expr(key, scope, new_stack, program)
        _check_expr(val, scope, new_stack, program)
        return
    if t == "set":
        for item in node.value:
            _check_expr(item, scope, block_stack, program)
        return
    if t == "empty_dict":
        return
    if t == "dict":
        for key, val in node.value:
            _check_expr(key, scope, block_stack, program)
            _check_expr(val, scope, block_stack, program)
        return
    if t == "range":
        lo, hi = node.value
        _check_expr(lo, scope, block_stack, program)
        _check_expr(hi, scope, block_stack, program)
        return
    if t in ("in", "notin"):
        a, b = node.value
        _check_expr(a, scope, block_stack, program)
        _check_expr(b, scope, block_stack, program)
        return
    if t == "ifelse":
        a, cond, b = node.value
        _check_expr(a, scope, block_stack, program)
        _check_expr(cond, scope, block_stack, program)
        _check_expr(b, scope, block_stack, program)
        return
    if t == "nary_rule":
        components, operators = node.value
        for c in components:
            _check_expr(c, scope, block_stack, program)
        return
    if t == "lambda_expr":
        bound, body = node.value
        frame = {}
        for name in _bound_names(bound):
            frame[name.value] = LocalDeclaration(name.value, "lambda", name.start, name.end)
        _check_expr(body, scope, block_stack + [frame], program)
        return
    if t == "set_rule":
        if isinstance(node.value, list):
            return   # the empty '{}' case - ambiguous empty set/dict, no sub-expression
        _check_expr(node.value, scope, block_stack, program)
        return
    raise AssertionError("checker._check_expr: unhandled node type %r" % (t,))


def _check_occ_iter_parse(it, scope, block_stack, program):
    """block_stack[-1] is the frame shared by every for_parse/where_parse
    clause of this ONE iter_parse - built up incrementally, exactly as
    Pass 2 does, so a later clause's expressions see an earlier
    clause's bound names but a clause's own SOURCE expression doesn't
    see names it's itself about to bind."""
    frame = block_stack[-1]
    for clause in it.value:
        if clause.type == "for_parse":
            b1, b2, src = clause.value
            _check_expr(src, scope, block_stack, program)
            for name in _bound_names(b1):
                frame[name.value] = LocalDeclaration(name.value, "for", name.start, name.end)
            if b2 is not None:
                for name in _bound_names(b2):
                    frame[name.value] = LocalDeclaration(name.value, "for", name.start, name.end)
        elif clause.type == "where_parse":
            _check_expr(clause.value, scope, block_stack, program)


def _check_assign_target(node, scope, block_stack, program):
    """One target from an assign_stmt/aug_assign_stmt's target list (or
    an element of one, recursively, for a destructuring target): apply
    the lvalue-kind restriction to its fixed name, if it has one (see
    _lvalue_head), and walk the whole thing as an ordinary expression
    too - an index like 'a[i]' still reads 'i' normally, even though 'a'
    is also this target's lvalue name."""
    if node.type == "assign_target_list":
        for item in node.value:
            _check_assign_target(item, scope, block_stack, program)
        return
    if node.type == "assign_target":
        if isinstance(node.value, tuple) and len(node.value) == 2 and node.value[0] == "!":
            # '!expr = value' stores through whatever 'expr' addresses -
            # there's no fixed named lvalue here at all (see _lvalue_head).
            _check_expr(node.value[1], scope, block_stack, program)
        else:
            _check_assign_target(node.value, scope, block_stack, program)
        return
    # The plain fallback shape: an identifier-headed application (or a
    # bare identifier), returned directly rather than wrapped.
    head = _lvalue_head(node)
    if head is not None:
        _check_assign_target_name(head, scope, block_stack, program)
    _check_expr(node, scope, block_stack, program)


def _check_occ_simple(s, scope, block_stack, program):
    if s.type == "simple_stmt":
        _, inner = s.value
        _check_occ_simple(inner, scope, block_stack, program)
        return
    if s.type == "var_stmt":
        # Mirrors _collect_locals_simple's var_stmt handling: the rhs is
        # checked with whatever x meant BEFORE this declaration, then
        # x joins the current (innermost, still-open) block's frame -
        # visible to sibling statements from here to the end of that
        # block, but not to ones textually before it in the same block.
        bound, rhs = s.value
        _check_expr(rhs, scope, block_stack, program)
        for name in _bound_names(bound):
            block_stack[-1][name.value] = LocalDeclaration(name.value, "var", name.start, name.end)
        return
    if s.type == "const_assign_stmt":
        # const is now block-scoped exactly like var/global (unless
        # promoted - see _collect_top_level_shared): the rhs is checked
        # first, then each bound name joins block_stack[-1], reusing
        # Phase 1's own already-resolved Declaration object directly
        # (it carries kind/start/end/module already correct - see
        # _resolve_identifier's "local" origin).
        bound, rhs = s.value
        _check_expr(rhs, scope, block_stack, program)
        for name in _bound_names(bound):
            decl = program.global_ns.declared.get(name.value)
            if decl is not None:
                block_stack[-1][name.value] = decl
        return
    if s.type == "global_stmt":
        # 'global x' is now block-scoped, exactly like 'var x' above:
        # any non-identifier item is still an ordinary expression to
        # check, but each identifier item joins block_stack[-1] AT THIS
        # POINT in the walk - visible to sibling statements from here to
        # the end of this block, but not to ones textually before it in
        # the same block (see FunctionScope.declare_shared/Phase 1's
        # mirroring _collect_locals_simple handling).
        for item in s.value:
            if item.type == "identifier":
                block_stack[-1][item.value] = LocalDeclaration(item.value, "global", item.start, item.end)
            else:
                _check_expr(item, scope, block_stack, program)
        return
    if s.type == "assign_stmt":
        targets, rhs = s.value
        for target in targets:
            _check_assign_target(target, scope, block_stack, program)
        _check_expr(rhs, scope, block_stack, program)
        return
    if s.type == "aug_assign_stmt":
        lhs, op, rhs = s.value
        _check_assign_target(lhs, scope, block_stack, program)
        _check_expr(rhs, scope, block_stack, program)
        return
    if s.type == "expr_stmt":
        _check_expr(s.value, scope, block_stack, program)
        return
    if s.type in ("await_stmt", "trap_stmt", "finally_stmt",
                  "invariant_stmt", "del_stmt"):
        _check_expr(s.value, scope, block_stack, program)
        return
    if s.type == "spawn_stmt":
        eternal, value = s.value
        _check_expr(value, scope, block_stack, program)
        return
    if s.type == "go_stmt":
        target, value = s.value
        _check_expr(target, scope, block_stack, program)
        if value is not None:
            _check_expr(value, scope, block_stack, program)
        return
    if s.type == "print_stmt":
        value, endpoint = s.value
        _check_expr(value, scope, block_stack, program)
        if endpoint is not None:
            _check_expr(endpoint, scope, block_stack, program)
        return
    if s.type == "assert_stmt":
        cond, message = s.value
        _check_expr(cond, scope, block_stack, program)
        if message is not None:
            _check_expr(message, scope, block_stack, program)
        return
    if s.type == "sequential_stmt":
        # Block-scoped exactly like global_stmt just above.
        for item in s.value:
            block_stack[-1][item.value] = LocalDeclaration(item.value, "sequential", item.start, item.end)
        return
    # builtin_stmt: handled at the global-namespace level (Phase 1);
    # return_stmt/break_stmt/continue_stmt: already reported
    # unconditionally in Phase 1 (_collect_locals_simple), so nothing
    # further to do here; pass_stmt: nothing to do.


def _check_occ_stmt(stmt, scope, block_stack, program):
    kind = stmt.value[0]
    if kind == "blank":
        return
    if kind == "simple":
        _, prefix, one_line = stmt.value
        for s in _flatten_one_line(one_line):
            _check_occ_simple(s, scope, block_stack, program)
        return
    if kind == "compound":
        _, prefix, compound = stmt.value
        _check_occ_compound(compound, scope, block_stack, program)
        return
    if kind == "import":
        # import/from is now block-scoped exactly like const (unless
        # promoted): each name it binds joins block_stack[-1] here,
        # reusing Phase 1's own already-resolved Declaration object
        # directly (see const_assign_stmt's own handling just above, in
        # _check_occ_simple).
        _, prefix, imp = stmt.value
        for name in _import_names(imp, program):
            decl = program.global_ns.declared.get(name)
            if decl is not None:
                block_stack[-1][name] = decl
        return
    if kind == "labeled_block":
        _, prefix, block = stmt.value
        _check_occ_block(block, scope, block_stack, program)
        return


def _check_occ_block(block, scope, block_stack, program):
    """Mirrors _collect_locals_block: every block gets its own fresh
    frame here too, so a 'var' declared directly in it (see
    _check_occ_simple's var_stmt handling) is only visible for the rest
    of THIS block - never to a sibling block, which never shares this
    frame at all."""
    frame = {}
    new_stack = block_stack + [frame]
    if block.type == "one_line_stmt":
        for s in _flatten_one_line(block):
            _check_occ_simple(s, scope, new_stack, program)
    elif block.type == "normal_block":
        for stmt in block.value:
            _check_occ_stmt(stmt, scope, new_stack, program)


def _check_occ_compound(compound, scope, block_stack, program):
    if compound.type == "compound_stmt":
        _, inner = compound.value
        _check_occ_compound(inner, scope, block_stack, program)
        return
    if compound.type == "if_block":
        cond, body, elifs, else_block = compound.value
        _check_expr(cond, scope, block_stack, program)
        _check_occ_block(body, scope, block_stack, program)
        for e in elifs:
            econd, ebody = e.value
            _check_expr(econd, scope, block_stack, program)
            _check_occ_block(ebody, scope, block_stack, program)
        if else_block is not None:
            _check_occ_block(else_block.value, scope, block_stack, program)
        return
    if compound.type == "while_block":
        cond, body = compound.value
        _check_expr(cond, scope, block_stack, program)
        _check_occ_block(body, scope, block_stack, program)
        return
    if compound.type == "for_block":
        # The for-loop's bound name(s) and its own body share ONE frame,
        # scoped to this loop's own extent (mirrors _collect_locals_compound).
        it, body = compound.value
        frame = {}
        new_stack = block_stack + [frame]
        _check_occ_iter_parse(it, scope, new_stack, program)
        _check_occ_block(body, scope, new_stack, program)
        return
    if compound.type == "let_when_block":
        # All of this let/when-block's own decls, plus its body, share
        # ONE frame - a decl's own rhs/cond is checked BEFORE its own
        # name(s) join the frame (so "let x = x + 1:" reads the OUTER
        # x, not itself), but a LATER decl in the same chain does see
        # an earlier one's bound name, exactly like Pass 2's shadowing
        # rule for chained decls.
        decls, body = compound.value
        frame = {}
        new_stack = block_stack + [frame]
        for d in decls.value:
            if d.type == "let_decl":
                bound, rhs = d.value
                _check_expr(rhs, scope, new_stack, program)
                for name in _bound_names(bound):
                    frame[name.value] = LocalDeclaration(name.value, "let", name.start, name.end)
            elif d.type == "when_decl":
                if d.value[0] == "exists":
                    _, bound, cond = d.value
                    _check_expr(cond, scope, new_stack, program)
                    for name in _bound_names(bound):
                        frame[name.value] = LocalDeclaration(name.value, "exists", name.start, name.end)
                else:
                    _, cond = d.value
                    _check_expr(cond, scope, new_stack, program)
        _check_occ_block(body, scope, new_stack, program)
        return
    if compound.type == "method_decl":
        return   # a nested function - checked separately, as its own scope
    if compound.type == "atomic_block":
        _check_occ_block(compound.value, scope, block_stack, program)
        return


def _check_occ_in_scope(scope, program):
    kind, body = scope.body
    if kind == "block":
        _check_occ_block(body, scope, [], program)
    else:
        # The top-level program has no wrapping block syntax to go
        # through _check_occ_block (which is what normally pushes a
        # block's own frame) - so its own top-level frame is pushed
        # explicitly here, mirroring _process_top_level's Pass-1 side.
        frame = {}
        block_stack = [frame]
        for stmt in body:
            _check_occ_stmt(stmt, scope, block_stack, program)


# ---------------------------------------------------------------------------
# Phase 2 entry point
# ---------------------------------------------------------------------------

def check_identifiers(document, module_map=None, source_label="<program>", source_dir=None,
                       default_module_dir=DEFAULT_MODULE_DIR, extra_consts=None):
    """Phase 1 + Phase 2 together. Returns a Phase2State:
      `.errors`   - every Phase 1 collision plus every Phase 2 shadowing/
                    lvalue-kind violation (a parse failure is the only
                    entry, same as check_global_namespace on its own)
      `.warnings` - currently always empty (Harmony no longer has an
                    implicit-global fallback to merely warn about); kept
                    as its own list for any future merely-advisory
                    finding
      `.global_ns`- the Phase 1 GlobalNamespace (also reachable this way
                    if only Phase 1's own result is wanted)
      `.promoted` - name -> Declaration, for every `global`/`sequential`/
                    `const`/`import`/`from` statement written directly,
                    unnested, in the program's own top-level statement
                    list - genuinely usable from any function with no
                    declaration of its own (subject to the same
                    declared-before-use ordering an ordinary block-
                    scoped declaration would need, never def/builtin's
                    full hoisting)
      `.scopes`   - every function's own FunctionScope, implicit
                    top-level program first, in the order encountered

    `source_dir` and `default_module_dir` are passed straight through
    to check_global_namespace - see there for the module-lookup
    fallback order they control. `extra_consts` (see
    check_global_namespace - a `-c NAME=VALUE` only overrides the value
    of a matching in-source `const`, it never creates a new binding) is
    also promoted here: when the name really is declared `const`
    in-source, this just makes sure it's promoted (matching Phase 2's
    own promotion of that same statement - declare_promoted is a no-op
    the second time); when check_global_namespace had to fall back to
    declaring it itself (no matching in-source `const` found), this is
    what actually makes the name usable from every function immediately,
    with no declared-before-use ordering to satisfy.
    """
    global_ns = check_global_namespace(document, module_map, source_label, source_dir,
                                        default_module_dir, extra_consts)
    program = Phase2State(global_ns)
    program.errors.extend(global_ns.errors)
    for name in (extra_consts or ()):
        if name in global_ns.declared and global_ns.declared[name].kind == "const":
            program.declare_promoted(name, "const", -1, -1)
    parsed = harmony_parser.parse_program(document)
    if not parsed.success:
        return program   # already reported above, via global_ns.errors
    _collect_top_level_shared(parsed.value, program)
    _process_top_level(parsed.value, program)
    _check_shadowing(program)
    for scope in program.scopes:
        _check_occ_in_scope(scope, program)
    return program


# ---------------------------------------------------------------------------
# Small standalone CLI, mirroring preprocess.py's own.
# ---------------------------------------------------------------------------

def offset_to_line_col(document, offset):
    """Character offset -> (1-based line, 1-based column) within
    `document` - a small, genuinely reusable utility (not just this
    CLI's own helper): any caller embedding this checker (e.g. as a
    preprocessing pass ahead of another compiler) needs this same
    conversion to report a CheckError's `.start`/`.end` the way its own
    error format expects."""
    line = document.count('\n', 0, offset) + 1
    line_start = document.rfind('\n', 0, offset) + 1
    col = offset - line_start + 1
    return line, col


def main(argv):
    import sys
    if len(argv) < 2:
        print("usage: python3 checker.py path/to/program.hny [module=path.hny ...]", file=sys.stderr)
        return 2

    path = argv[1]
    module_map = {}
    for arg in argv[2:]:
        name, _, mod_path = arg.partition('=')
        module_map[name] = mod_path

    try:
        with open(path, 'r') as f:
            document = f.read()
    except OSError as e:
        print("error: could not read %s: %s" % (path, e.strerror or e), file=sys.stderr)
        return 2

    program = check_identifiers(document, module_map, source_label=path)
    for err in program.errors:
        line, col = offset_to_line_col(document, err.start)
        print("%s:%d:%d: error: %s" % (path, line, col, err.message))
    for warn in program.warnings:
        line, col = offset_to_line_col(document, warn.start)
        print("%s:%d:%d: warning: %s" % (path, line, col, warn.message))
    if not program.errors:
        print("OK: %s has no identifier problems" % path)
        return 0
    return 1


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
