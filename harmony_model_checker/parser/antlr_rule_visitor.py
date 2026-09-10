from typing import Any, Union
from antlr4.Token import CommonToken  # type: ignore
from antlr4.tree.Tree import TerminalNode  # type: ignore

from harmony_model_checker.parser.HarmonyVisitor import HarmonyVisitor
from harmony_model_checker.parser.HarmonyParser import HarmonyParser
from harmony_model_checker.harmony.ast import *

class HarmonyVisitorImpl(HarmonyVisitor):

    def __init__(self, file: str):
        assert isinstance(file, str)
        self.file = file
        self.associative_operators = { "+", "*", "|", "&", "^", "and", "or" }

    def get_token(self, tkn: Union[CommonToken, tuple], value: Any) -> tuple:
        if isinstance(tkn, CommonToken):
            line = tkn.line
            col = tkn.column + 1
        else:
            line = tkn[2]
            col = tkn[3]

        assert isinstance(col, int)
        assert isinstance(line, int)

        return value, self.file, line, col

    # Visit a parse tree produced by HarmonyParser#import_stmt.
    def visitImport_stmt(self, ctx: HarmonyParser.Import_stmtContext):
        if ctx.import_from():
            return self.visit(ctx.import_from())
        elif ctx.import_name():
            return self.visit(ctx.import_name())
        tkn = self.get_token(ctx.start, ctx.start.text)
        raise HarmonyCompilerError(
            message="Failed to parse import",
            filename=self.file,
            line=tkn[2],
            column=tkn[3],
            lexeme=tkn[0]
        )

    # Visit a parse tree produced by HarmonyParser#import_name.
    def visitImport_name(self, ctx: HarmonyParser.Import_nameContext):
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return ImportAST(endtoken, tkn, False, self.visit(ctx.import_names_seq()))

    # Visit a parse tree produced by HarmonyParser#import_from.
    def visitImport_from(self, ctx: HarmonyParser.Import_fromContext):
        dotted_name = self.get_token(ctx.NAME().symbol, str(ctx.NAME()))
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        if ctx.STAR():
            return FromAST(endtoken, tkn, False, dotted_name, [])
        names = self.visit(ctx.import_names_seq())
        return FromAST(endtoken, tkn, False, dotted_name, names)
    
    def visitImport_names_seq(self, ctx: HarmonyParser.Import_names_seqContext):
        return [self.get_token(d.symbol, str(d)) for d in ctx.NAME()]
    
    def visitSequential_names_seq(self, ctx: HarmonyParser.Sequential_names_seqContext):
        return [self.get_token(d.symbol, str(d)) for d in ctx.NAME()]

    # Visit a parse tree produced by HarmonyParser#program.
    def visitProgram(self, ctx: HarmonyParser.ProgramContext):
        stmts = [s for stmt in ctx.stmt() for s in self.visit(stmt) if s is not None]
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        if len(stmts) == 0:
            raise HarmonyCompilerError(
                message="Empty program",
                filename=self.file,
                line=tkn[2],
                column=tkn[3],
                lexeme=tkn[0]
            )
        return BlockAST(endtoken, tkn, False, stmts, endtoken)

    # Visit a parse tree produced by HarmonyParser#tuple_bound.
    def visitTuple_bound(self, ctx:HarmonyParser.Tuple_boundContext):
        if ctx.bound() is not None:
            return self.visit(ctx.bound())
        if ctx.NAME():
            name = ctx.NAME()
            return self.get_token(name.symbol, str(name))
        return []

    # Visit a parse tree produced by HarmonyParser#bound.
    def visitBound(self, ctx: HarmonyParser.BoundContext):
        bv = [self.visit(t) for t in ctx.tuple_bound()]
        if len(bv) == 1:
            return bv[0]
        return bv

    # Visit a parse tree produced by HarmonyParser#unary_op.
    def visitUnary_op(self, ctx: HarmonyParser.Unary_opContext):
        return self.get_token(ctx.start, ctx.getText())

    # Visit a parse tree produced by HarmonyParser#int.
    def visitInt(self, ctx: HarmonyParser.IntContext):
        txt = ctx.getText()
        tkn = self.get_token(ctx.start, int(txt, 0))
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return ConstantAST(endtoken, tkn)

    # Visit a parse tree produced by HarmonyParser#bool.
    def visitBool(self, ctx: HarmonyParser.BoolContext):
        txt = ctx.getText()
        tkn = self.get_token(ctx.start, txt == 'True')
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return ConstantAST(endtoken, tkn)

    # Visit a parse tree produced by HarmonyParser#atom.
    def visitAtom(self, ctx: HarmonyParser.AtomContext):
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        lexeme = ctx.getText()
        if lexeme.startswith("0x"):
            v = chr(int(lexeme, 16))
            tkn = self.get_token(ctx.start, v)
            return ConstantAST(endtoken, tkn)
        else:
            tkn = self.get_token(ctx.start, lexeme[1:])
            return ConstantAST(endtoken, tkn)

    # Visit a parse tree produced by HarmonyParser#name.
    def visitName(self, ctx: HarmonyParser.NameContext):
        tkn = self.get_token(ctx.start, ctx.getText())
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return NameAST(endtoken, tkn)

    # Visit a parse tree produced by HarmonyParser#str.
    def visitStr(self, ctx: HarmonyParser.StrContext):
        value = ctx.getText()
        if value.startswith("'''") and value.endswith("'''"):
            s = value[3:-3]
        elif value.startswith('"""') and value.endswith('"""'):
            s = value[3:-3]
        elif value.startswith("'") and value.endswith("'"):
            s = value[1:-1]
        elif value.startswith('"') and value.endswith('"'):
            s = value[1:-1]
        else:
            tkn = self.get_token(ctx.start, value)
            raise HarmonyCompilerError(
                message="Unable to parse string",
                filename=self.file,
                line=tkn[2],
                column=tkn[3],
                lexeme=tkn[0]
            )
        tkn = self.get_token(ctx.start, s)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return ConstantAST(endtoken, tkn)

    def visitPrint_stmt(self, ctx: HarmonyParser.Print_stmtContext):
        expr = self.visit(ctx.expr(0))
        msg = self.visit(ctx.expr(1)) if ctx.expr(1) is not None else None
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return PrintAST(endtoken, tkn, False, expr, msg)

    # Visit a parse tree produced by HarmonyParser#none.
    def visitNone(self, ctx: HarmonyParser.NoneContext):
        tkn = self.get_token(ctx.start, AddressValue(None, []))
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return ConstantAST(endtoken, tkn)

    # Visit a parse tree produced by HarmonyParser#address.
    # def visitAddress(self, ctx: HarmonyParser.AddressContext):
    #     expr = self.visit(ctx.expr_rule())
    #     tkn = self.get_token(ctx.start, ctx.start.text)
    #     endtoken = self.get_token(ctx.stop, ctx.stop.text)
    #     return AddressAST(endtoken, tkn, expr)

    # Visit a parse tree produced by HarmonyParser#assign_op.
    def visitAssign_op(self, ctx: HarmonyParser.Assign_opContext):
        return self.get_token(ctx.start, ctx.getText())

    # Visit a parse tree produced by HarmonyParser#aug_assign_op.
    def visitAug_assign_op(self, ctx: HarmonyParser.Aug_assign_opContext):
        return self.get_token(ctx.start, ctx.getText())

    # Visit a parse tree produced by HarmonyParser#expr_stmt.
    def visitExpr_stmt(self, ctx: HarmonyParser.Expr_stmtContext):
        e = self.visit(ctx.expr_rule())
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return CallAST(endtoken, tkn, False, e)

    # Visit a parse tree produced by HarmonyParser#assign_stmt.
    def visitAssign_stmt(self, ctx: HarmonyParser.Assign_stmtContext):
        # (assign_target_list assign_op)+ tuple_rule - assign_target_list and
        # assign_op each appear inside the repeated group (so "a = b = expr"
        # parses as two of each), but tuple_rule (the final rhs) appears
        # exactly once - NOT as one more entry alongside the targets.
        ops = [self.visit(e) for e in ctx.assign_op()]
        targets = [self.visit(e) for e in ctx.assign_target_list()]
        rhs = self.visit(ctx.tuple_rule())
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return AssignmentAST(endtoken, tkn, targets, rhs, ops, False)

    # Visit a parse tree produced by HarmonyParser#aug_assign_stmt.
    def visitAug_assign_stmt(self, ctx: HarmonyParser.Aug_assign_stmtContext):
        lhs = self.visit(ctx.assign_target_list())
        rhs = self.visit(ctx.tuple_rule())
        op = self.visit(ctx.aug_assign_op())
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return AuxAssignmentAST(endtoken, tkn, lhs, rhs, op, False)

    # Visit a parse tree produced by HarmonyParser#assign_target_list.
    # Mirrors visitTuple_rule's own single-vs-tuple handling: a lone target
    # with no trailing comma is passed through as-is; anything else (2+
    # targets, or a single target with a trailing comma) is wrapped in a
    # TupleAST, the same destructuring-target wrapper tuple_rule itself uses
    # for its rhs values - TupleAST.ph1/ph2 already know how to recurse into
    # each element, which is exactly what a destructuring assign needs.
    def visitAssign_target_list(self, ctx: HarmonyParser.Assign_target_listContext):
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        targets = [self.visit(t) for t in ctx.assign_target()]
        comma_count = len(ctx.COMMA())
        if len(targets) == 1 and comma_count != 1:
            return targets[0]
        return TupleAST(endtoken, targets, tkn)

    # Visit a parse tree produced by HarmonyParser#assign_target.
    # A parenthesized/bracketed group just delegates to its inner
    # assign_target_list (parens/brackets are pure grouping here - see the
    # assign_target comment in Harmony.g4); 'application' likewise delegates
    # to the ordinary application visitor. The one case that needs explicit
    # handling is '!' expr_rule: unlike expr_rule's own unary '!' handling
    # (which only fires when '!' is parsed *through* application/expr_rule),
    # assign_target's '!' alternative is its own separate grammar path, so
    # nothing else builds the PointerAST wrapper for it.
    def visitAssign_target(self, ctx: HarmonyParser.Assign_targetContext):
        if ctx.assign_target_list():
            return self.visit(ctx.assign_target_list())
        if ctx.application():
            return self.visit(ctx.application())
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        expr = self.visit(ctx.expr_rule())
        return PointerAST(endtoken, expr, tkn)

    # Visit a parse tree produced by HarmonyParser#const_assign_stmt.
    def visitConst_assign_stmt(self, ctx: HarmonyParser.Const_assign_stmtContext):
        lvalues = self.visit(ctx.bound())
        value = self.visit(ctx.expr())
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return ConstAST(endtoken, tkn, False, lvalues, value)

    # Visit a parse tree produced by HarmonyParser#assert_stmt.
    def visitAssert_stmt(self, ctx: HarmonyParser.Assert_stmtContext):
        assertion = self.visit(ctx.expr(0))
        msg = self.visit(ctx.expr(1)) if ctx.expr(1) is not None else None
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return AssertAST(endtoken, tkn, False, assertion, msg)

    # Visit a parse tree produced by HarmonyParser#await_stmt.
    def visitAwait_stmt(self, ctx: HarmonyParser.Await_stmtContext):
        cond = self.visit(ctx.expr())
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return LetWhenAST(endtoken, tkn, False, [('cond', cond, tkn, endtoken)], PassAST(endtoken, tkn, False))

    # Visit a parse tree produced by HarmonyParser#trap_stmt.
    def visitTrap_stmt(self, ctx: HarmonyParser.Trap_stmtContext):
        func = self.visit(ctx.expr())
        # if not isinstance(func, ApplyAST):
        #     tkn = self.get_token(func.token, func.token[0])
        #     raise HarmonyCompilerError(
        #         message="Expected a method call but found something else.",
        #         filename=self.file,
        #         line=tkn[2],
        #         column=tkn[3],
        #         lexeme=tkn[0]
        #     )
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return TrapAST(endtoken, tkn, False, func)

    # Visit a parse tree produced by HarmonyParser#return_stmt.
    def visitReturn_stmt(self, ctx: HarmonyParser.Return_stmtContext):
        expr = self.visit(ctx.expr())
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return ReturnAST(endtoken, tkn, False, expr)

    # Visit a parse tree produced by HarmonyParser#pass_stmt.
    def visitPass_stmt(self, ctx: HarmonyParser.Pass_stmtContext):
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return PassAST(endtoken, tkn, False)

    def visitBreak_stmt(self, ctx: HarmonyParser.Break_stmtContext):
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return BreakAST(endtoken, tkn, False)

    def visitContinue_stmt(self, ctx: HarmonyParser.Continue_stmtContext):
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return ContinueAST(endtoken, tkn, False)

    # Visit a parse tree produced by HarmonyParser#Finally_stmt.
    def visitFinally_stmt(self, ctx: HarmonyParser.Finally_stmtContext):
        cond = self.visit(ctx.expr())
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return FinallyAST(endtoken, cond, tkn, False)

    # Visit a parse tree produced by HarmonyParser#invariant_stmt.
    def visitInvariant_stmt(self, ctx: HarmonyParser.Invariant_stmtContext):
        cond = self.visit(ctx.expr())
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return InvariantAST(endtoken, cond, tkn, False)

    # Visit a parse tree produced by HarmonyParser#del_stmt.
    def visitDel_stmt(self, ctx: HarmonyParser.Del_stmtContext):
        e = self.visit(ctx.expr())
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return DelAST(endtoken, tkn, False, e)

    def visitSimple_stmt(self, ctx: HarmonyParser.Simple_stmtContext):
        if ctx.ATOMICALLY():
            a = self.visit(ctx.children[-1])
            assert isinstance(a, AST)
            atom = ctx.ATOMICALLY()
            a.atomically = self.get_token(atom.getSymbol(), atom.getText())
            return a
        return super().visitSimple_stmt(ctx)

    def visitCompound_stmt(self, ctx: HarmonyParser.Compound_stmtContext):
        if ctx.ATOMICALLY():
            a = self.visit(ctx.children[-1])
            assert isinstance(a, AST)
            atom = ctx.ATOMICALLY()
            a.atomically = self.get_token(atom.getSymbol(), atom.getText())
            return a
        return super().visitCompound_stmt(ctx)

    # Visit a parse tree produced by HarmonyParser#spawn_stmt.
    def visitSpawn_stmt(self, ctx: HarmonyParser.Spawn_stmtContext):
        is_eternal = ctx.ETERNAL() is not None
        target = self.visit(ctx.expr())
        # if not isinstance(target, ApplyAST):
        #     tkn = self.get_token(target.token, target.token[0])
        #     raise HarmonyCompilerError(
        #         message="Expected a method call but found something else.",
        #         filename=self.file,
        #         line=tkn[2],
        #         column=tkn[3],
        #         lexeme=tkn[0]
        #     )
        # method, arg = target.method, target.arg
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        # return SpawnAST(endtoken, tkn, False, method, arg, None, is_eternal)
        return SpawnAST(endtoken, tkn, False, target, None, is_eternal)

    # Visit a parse tree produced by HarmonyParser#go_stmt.
    def visitGo_stmt(self, ctx: HarmonyParser.Go_stmtContext):
        # go_stmt: GO expr (COMMA expr)?  - the second expr (the value STOP
        # returns to this go) is optional and defaults to None; GoAST.result
        # is compiled unconditionally, so a bare 'go ctx' needs a real
        # ConstantAST for None here, not Python's None.
        target = self.visit(ctx.expr(0))
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        if ctx.expr(1) is not None:
            args = self.visit(ctx.expr(1))
        else:
            args = ConstantAST(endtoken, self.get_token(ctx.start, AddressValue(None, [])))
        return GoAST(endtoken, tkn, False, target, args)

    # Visit a parse tree produced by HarmonyParser#sequential_stmt.
    def visitSequential_stmt(self, ctx: HarmonyParser.Sequential_stmtContext):
        expr = self.visit(ctx.sequential_names_seq())
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return SequentialAST(endtoken, tkn, False, expr)

    # Visit a parse tree produced by HarmonyParser#global_stmt.
    def visitGlobal_stmt(self, ctx: HarmonyParser.Global_stmtContext):
        expr = [self.visit(e) for e in ctx.expr()]
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return GlobalAST(endtoken, tkn, False, expr)

    # Visit a parse tree produced by HarmonyParser#builtin_stmt.
    def visitBuiltin_stmt(self, ctx: HarmonyParser.Builtin_stmtContext):
        name = str(ctx.NAME())
        nametkn = self.get_token(ctx.NAME().symbol, name)
        value = str(ctx.STRING())[1:-1]     # remove quotes
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return BuiltinAST(endtoken, tkn, NameAST(nametkn, nametkn), value)

    # NOTE: there used to be a visitAtomic_block here for a standalone
    # "atomic_block" grammar rule (HarmonyParser#atomic_block). That rule
    # no longer exists - the grammar now folds the ATOMICALLY prefix
    # directly into compound_stmt/simple_stmt themselves (see
    # visitCompound_stmt/visitSimple_stmt above, which already handle
    # ctx.ATOMICALLY() generically for every compound/simple statement
    # kind). This method was dead code that referenced a nonexistent
    # HarmonyParser.Atomic_blockContext - harmless while an older,
    # already-generated parser happened to still define that class, but
    # a hard failure (AttributeError at class-definition time, since the
    # type annotation is evaluated eagerly) the moment the parser is
    # regenerated from the current Harmony.g4. Removed rather than fixed
    # up, since visitCompound_stmt/visitSimple_stmt already cover its job.

    # Visit a parse tree produced by HarmonyParser#for_block.
    def visitFor_block(self, ctx: HarmonyParser.For_blockContext):
        iterables = self.visit(ctx.iter_parse())
        stmts = self.visit(ctx.block())
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return ForAST(endtoken, iterables, stmts, tkn, False)

    # Visit a parse tree produced by HarmonyParser#let_decl.
    def visitLet_decl(self, ctx: HarmonyParser.Let_declContext):
        lvalues = self.visit(ctx.bound())
        values = self.visit(ctx.tuple_rule())
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        op = self.visit(ctx.assign_op())
        return "var", lvalues, values, tkn, endtoken, op

    # Visit a parse tree produced by HarmonyParser#when_decl.
    def visitWhen_decl(self, ctx:HarmonyParser.When_declContext):
        expr = self.visit(ctx.expr())
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        if ctx.EXISTS() is not None:
            bv = self.visit(ctx.bound())
            return 'exists', bv, expr, tkn, endtoken
        else:
            return 'cond', expr, tkn, endtoken

    # Visit a parse tree produced by HarmonyParser#let_when_decl.
    def visitLet_when_decl(self, ctx:HarmonyParser.Let_when_declContext):
        decl = []
        if ctx.when_decl() is not None:
            decl.append(self.visit(ctx.when_decl()))
        elif ctx.let_decl() is not None:
            decl.append(self.visit(ctx.let_decl()))
        else:
            tkn = self.get_token(ctx.start, ctx.start.text)
            raise HarmonyCompilerError(
                message="Unexpected declaration in let/when block declaration.",
                filename=self.file,
                line=tkn[2],
                column=tkn[3],
                lexeme=tkn[0]
            )
        if ctx.let_when_decl() is not None:
            decl.extend(self.visit(ctx.let_when_decl()))
        return decl

    # Visit a parse tree produced by HarmonyParser#let_when_block.
    def visitLet_when_block(self, ctx:HarmonyParser.Let_when_blockContext):
        vars_and_conds = self.visit(ctx.let_when_decl())
        stmts = self.visit(ctx.block())
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        if all(vac[0] == 'var' for vac in vars_and_conds):
            vars = [vac[1:] for vac in vars_and_conds if vac[0] == 'var']
            return LetAST(endtoken, tkn, False, vars, stmts)
        else:
            return LetWhenAST(endtoken, tkn, False, vars_and_conds, stmts)

    # Visit a parse tree produced by HarmonyParser#opt_returns.
    def visitOpt_returns(self, ctx: HarmonyParser.Opt_returnsContext):
        return ctx.NAME()

    # Visit a parse tree produced by HarmonyParser#method_decl.
    def visitMethod_decl(self, ctx: HarmonyParser.Method_declContext):
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        value = str(ctx.NAME())
        method_name = self.get_token(ctx.NAME().symbol, value)
        args = self.visit(ctx.bound()) if ctx.bound() else []
        if ctx.opt_returns() is None:
            result_name = None
        else:
            ors = self.visit(ctx.opt_returns())
            result_name = self.get_token(ors.symbol, str(ors))
        body = self.visit(ctx.block())
        colon = ctx.COLON()
        ctoken = self.get_token(colon.getSymbol(), colon.getText())
        ast = MethodAST(endtoken, tkn, False, method_name, args, result_name, body, ctoken)
        return ast

    # Visit a parse tree produced by HarmonyParser#while_block.
    def visitWhile_block(self, ctx: HarmonyParser.While_blockContext):
        cond = self.visit(ctx.expr())
        stmts = self.visit(ctx.block())
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        colon = ctx.COLON()
        ctoken = self.get_token(colon.getSymbol(), colon.getText())
        return WhileAST(endtoken, tkn, False, cond, stmts, ctoken)

    # Visit a parse tree produced by HarmonyParser#if_block.
    def visitIf_block(self, ctx: HarmonyParser.If_blockContext):
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        colon = ctx.COLON()
        ctoken = self.get_token(colon.getSymbol(), colon.getText())
        cond = self.visit(ctx.expr())
        if_block = self.visit(ctx.block())
        alts = [(cond, if_block, tkn, endtoken, ctoken)]
        else_block = None
        if ctx.elif_block() is not None:
            for c in ctx.elif_block():
                alts.append(self.visit(c))
        if ctx.else_block() is not None:
            else_block = self.visit(ctx.else_block())
        return IfAST(endtoken, tkn, False, alts, else_block)

    # Visit a parse tree produced by HarmonyParser#elif_block.
    def visitElif_block(self, ctx: HarmonyParser.Elif_blockContext):
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        colon = ctx.COLON()
        ctoken = self.get_token(colon.getSymbol(), colon.getText())
        cond = self.visit(ctx.expr())
        stmts = self.visit(ctx.block())
        return cond, stmts, tkn, endtoken, ctoken

    # Visit a parse tree produced by HarmonyParser#else_block.
    def visitElse_block(self, ctx: HarmonyParser.Else_blockContext):
        return self.visit(ctx.block())

    # Visit a parse tree produced by HarmonyParser#var_stmt.
    def visitVar_stmt(self, ctx:HarmonyParser.Var_stmtContext):
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        lv = self.visit(ctx.bound())
        e = self.visit(ctx.tuple_rule())
        return VarAST(endtoken, tkn, False, [(lv, e)])

    # Visit a parse tree produced by HarmonyParser#normal_block.
    def visitNormal_block(self, ctx: HarmonyParser.Normal_blockContext):
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        if ctx.block() is not None:
            return self.visit(ctx.block())
        elif ctx.block_stmts() is not None:
            stmts = self.visit(ctx.block_stmts())
            return BlockAST(endtoken, tkn, False, stmts, endtoken)
        raise HarmonyCompilerError(
            message="Unexpected block structure.",
            filename=self.file,
            line=tkn[2],
            column=tkn[3],
            lexeme=tkn[0]
        )

    # Visit a parse tree produced by HarmonyParser#block_stmts.
    def visitBlock_stmts(self, ctx: HarmonyParser.Block_stmtsContext):
        block = [s for stmt in ctx.stmt() for s in self.visit(stmt)]
        return [s for s in block if s is not None]

    # Visit a parse tree produced by HarmonyParser#label.
    def visitLabel(self, ctx: HarmonyParser.LabelContext):
        names = [self.get_token(n.symbol, str(n)) for n in ctx.NAME()]
        return names

    # Visit a parse tree produced by HarmonyParser#stmt.
    def visitStmt(self, ctx: HarmonyParser.StmtContext):
        labels = []
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        if ctx.label() is not None:
            labels = self.visit(ctx.label())
        if ctx.one_line_stmt() is not None:
            stmt = self.visit(ctx.one_line_stmt())
        elif ctx.compound_stmt() is not None:
            stmt = self.visit(ctx.compound_stmt())
        elif ctx.import_stmt() is not None:
            stmt = self.visit(ctx.import_stmt())
        elif ctx.normal_block() is not None:
            stmt = self.visit(ctx.normal_block())
        else:
            return []

        assert stmt is not None
        if isinstance(stmt, AST):
            stmt_block = [LocationAST(endtoken, tkn, stmt, self.file, tkn[2])]
        elif isinstance(stmt, list):
            stmt_block = [LocationAST(endtoken, tkn, s, self.file, tkn[2]) for s in stmt]
        if ctx.COLON() or labels:
            if ctx.COLON():
                colon = ctx.COLON()
                ctoken = self.get_token(colon.getSymbol(), colon.getText())
                block = BlockAST(endtoken, tkn, False, stmt_block, ctoken)
            else:
                block = BlockAST(endtoken, tkn, False, stmt_block, endtoken)
            if labels:
                return [LocationAST(endtoken, tkn, LabelStatAST(endtoken, tkn, labels, block), self.file, tkn[2])]
            else:
                return [block]
        return stmt_block

    def visitBlock(self, ctx: HarmonyParser.BlockContext):
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        if ctx.normal_block():
            return self.visit(ctx.normal_block())
        elif ctx.one_line_stmt():
            return BlockAST(endtoken, tkn, False, self.visit(ctx.one_line_stmt()), endtoken)
        raise HarmonyCompilerError(
            message="Unable to parse block",
            filename=self.file,
            line=tkn[2],
            column=tkn[3],
            lexeme=tkn[0]
        )

    # Visit a parse tree produced by HarmonyParser#one_line_stmt.
    def visitOne_line_stmt(self, ctx: HarmonyParser.One_line_stmtContext):
        stmts = [self.visit(ctx.simple_stmt())]
        if ctx.one_line_stmt():
            stmts.extend(self.visit(ctx.one_line_stmt()))
        return stmts

    # Visit a parse tree produced by HarmonyParser#arith_op.
    def visitArith_op(self, ctx:HarmonyParser.Arith_opContext):
        return self.get_token(ctx.start, ctx.getText())

    # Visit a parse tree produced by HarmonyParser#set_rule_1.
    def visitSet_rule_1(self, ctx: HarmonyParser.Set_rule_1Context):
        if ctx.set_rule():
            return self.visit(ctx.set_rule())
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return SetAST(endtoken, self.get_token(ctx.start, ctx.start.text), [])

    # Visit a parse tree produced by HarmonyParser#empty_dict.
    def visitEmpty_dict(self, ctx: HarmonyParser.Empty_dictContext):
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return DictAST(endtoken, self.get_token(ctx.start, ctx.start.text), [])

    # Visit a parse tree produced by HarmonyParser#paren_tuple.
    def visitParen_tuple(self, ctx: HarmonyParser.Paren_tupleContext):
        if ctx.tuple_rule():
            return self.visit(ctx.tuple_rule())
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return ConstantAST(endtoken, (emptytuple, self.file, tkn[2], tkn[3]))

    # Visit a parse tree produced by HarmonyParser#brack_tuple.
    def visitBracket_tuple(self, ctx: HarmonyParser.Bracket_tupleContext):
        if ctx.tuple_rule():
            return self.visit(ctx.tuple_rule())
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return ConstantAST(endtoken, (emptytuple, self.file, tkn[2], tkn[3]))

    def visitLambda_expr(self, ctx: HarmonyParser.Lambda_exprContext):
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        args = self.visit(ctx.bound()) if ctx.bound() is not None else []
        body = self.visit(ctx.nary_expr())
        return LambdaAST(endtoken, args, body, tkn, False)

    # Visit a parse tree produced by HarmonyParser#set_rule.
    def visitSet_rule(self, ctx: HarmonyParser.Set_ruleContext):
        values = [self.visit(e) for e in ctx.nary_expr()]
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        if ctx.COLON():
            if ctx.iter_parse():
                k, v = values[0], values[1]
                comp = self.visit(ctx.iter_parse())
                return DictComprehensionAST(endtoken, k, v, comp, tkn)
            k = values[::2]
            v = values[1::2]
            return DictAST(endtoken, tkn, list(zip(k, v)))
        if ctx.iter_parse():
            comp = self.visit(ctx.iter_parse())
            return SetComprehensionAST(endtoken, values[0], comp, tkn)
        if ctx.RANGE():
            return RangeAST(endtoken, values[0], values[1], tkn)
        if ctx.COMMA():
            return SetAST(endtoken, tkn, values)
        return SetAST(endtoken, tkn, [values[0]])

    # Visit a parse tree produced by HarmonyParser#iter_parse.
    def visitIter_parse(self, ctx: HarmonyParser.Iter_parseContext):
        v = [self.visit(e) for e in ctx.children]
        return [x for x in v if x is not None]

    # Visit a parse tree produced by HarmonyParser#for_parse.
    def visitFor_parse(self, ctx: HarmonyParser.For_parseContext):
        l1 = self.visit(ctx.bound(0))
        l2 = self.visit(ctx.bound(1)) if ctx.bound(1) else None
        expr = self.visit(ctx.nary_expr())
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        if l2 is not None:
            return "for", (l2, l1, expr, tkn, endtoken)
        else:
            return "for", (l1, None, expr, tkn, endtoken)

    # Visit a parse tree produced by HarmonyParser#where_parse.
    def visitWhere_parse(self, ctx: HarmonyParser.Where_parseContext):
        expr = self.visit(ctx.nary_expr())
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return "where", (expr, tkn, endtoken)

    # Visit a parse tree produced by HarmonyParser#tuple_rule.
    def visitTuple_rule(self, ctx: HarmonyParser.Tuple_ruleContext):
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        values = [self.visit(e) for e in ctx.nary_expr()]
        if ctx.iter_parse():
            iterators = self.visit(ctx.iter_parse())
            return ListComprehensionAST(endtoken, values[0], iterators, tkn)
        comma_count = len(ctx.COMMA())
        if len(values) == 1 and comma_count != 1:
            return values[0]
        return TupleAST(endtoken, values, tkn)

    # --- Expression construction helpers -----------------------------
    #
    # The grammar's nary_expr/logic_expr/compare_expr/arith_expr chain is
    # deliberately flat CFG-wise at each tier (see the comments above
    # those rules in Harmony.g4), so each tier's own operator-chain
    # restriction (which combinations are legal, and how a legal chain
    # regroups into a binary-ish AST) is enforced here in Python rather
    # than in the grammar itself. Each visitXxx_expr method below pulls
    # its rule's already-flat list of operands/operators straight from
    # its own ANTLR context (no more cross-tier operator classification
    # needed - that used to be necessary back when a single flat rule
    # carried logic/compare/arith operators all together) and hands them
    # to the matching helper.

    def factor_expr(self, ops, exprs):
        # ops/exprs cover one maximal run of multiplicative-tier
        # operators (*, /, //, mod, %). At most one operator in the run
        # may be something other than '*', and it must be the LAST one
        # ("a * b * ... * c @ d") - see the arith_expr comment in
        # Harmony.g4. This also keeps the construction below honest: once
        # every op but the last is guaranteed to be '*' (associative), the
        # exprs[:-1] group can be combined under a single flat '*' NaryAST
        # with no ambiguity about how it was actually grouped.
        if len(ops) == 0:
            return exprs[0]
        if len(ops) == 1:
            return NaryAST(exprs[1].endtoken, exprs[0].token, ops[0], exprs)
        for o in ops[:-1]:
            if o[0] != '*':
                raise HarmonyCompilerError(
                    message="Expression too complicated: use parentheses",
                    filename=self.file,
                    line=o[2],
                    column=o[3],
                    lexeme=o[0]
                )
        if ops[-1][0] == '*':
            return NaryAST(exprs[-1].endtoken, exprs[0].token, ops[-1], exprs)
        return NaryAST(exprs[-1].endtoken, exprs[0].token, ops[-1],
            [ NaryAST(exprs[-2].endtoken, exprs[0].token, ops[0], exprs[:-1]), exprs[-1] ])

    def simple_expr(self, ops, exprs):
        # Splits an arith_expr chain that's already known to be a legal
        # mix of {+, -, *, /, //, mod, %} on its '+'/'-' (additive-tier)
        # operators, recursing into factor_expr for each maximal
        # multiplicative-tier run in between - this is the "regrouped by
        # standard arithmetic precedence" step from the Harmony.g4
        # comment.
        simple_ops = [ o for o in ops if o[0] in { '+', '-' } ]
        if len(simple_ops) == 0:
            return self.factor_expr(ops, exprs)
        sub_ops = []
        sub_exprs = [ exprs[0] ]
        sub_asts = []
        for i in range(len(ops)):
            if ops[i] in simple_ops:
                sub_asts.append(self.factor_expr(sub_ops, sub_exprs))
                sub_ops = []
                sub_exprs = [ exprs[i+1] ]
            else:
                sub_ops.append(ops[i])
                sub_exprs.append(exprs[i+1])
        sub_asts.append(self.factor_expr(sub_ops, sub_exprs))
        ast = sub_asts[0]
        for i in range(len(simple_ops)):
            ast = NaryAST(sub_asts[i+1].endtoken, sub_asts[0].token, simple_ops[i], [ ast, sub_asts[i+1] ])
        return ast

    def arith_expr(self, ops, exprs):
        assert len(ops) + 1 == len(exprs)
        if len(ops) == 0:
            return exprs[0]
        if len(ops) == 1:
            return NaryAST(exprs[1].endtoken, exprs[0].token, ops[0], exprs)

        # See if all are the same associative operator
        if ops[0][0] in self.associative_operators and all(o[0] == ops[0][0] for o in ops):
            return NaryAST(exprs[-1].endtoken, exprs[0].token, ops[0], exprs)

        # See if it's a legal mix of standard arithmetic operators
        if all(o[0] in { '+', '-', '*', '/', '//', '%', 'mod' } for o in ops):
            return self.simple_expr(ops, exprs)

        # Anything else (repeated non-associative operators like '<<',
        # '>>', '**', or a mix involving a non-arithmetic operator) has no
        # defined relative precedence.
        token = ops[0]
        raise HarmonyCompilerError(
            message="Expression too complicated: use parentheses",
            filename=self.file,
            line=token[2],
            column=token[3],
            lexeme=token[0]
        )

    def cmp_expr(self, ops, exprs):
        # compare_expr's own operators are always genuine comparison
        # operators (compare_op is its own grammar rule/token type now),
        # and exprs are already-resolved arith_expr subexpressions, so
        # there's no cross-tier classification left to do here.
        assert len(ops) + 1 == len(exprs)
        return CmpAST(exprs[-1].endtoken, exprs[0].token, ops, exprs)

    def bool_expr(self, ops, exprs):
        # logic_expr's own operators are always genuine logic operators
        # (logic_op is its own grammar rule/token type now). A chain of
        # 2+ is only legal if every operator is identical, and that
        # operator is 'and' or 'or' - never '=>' (see the logic_expr
        # comment in Harmony.g4).
        assert len(ops) > 0
        assert len(ops) + 1 == len(exprs)
        if any(o[0] != ops[0][0] for o in ops):
            token = ops[0]
            raise HarmonyCompilerError(
                message="Boolean expression too complicated: use parentheses",
                filename=self.file,
                line=token[2],
                column=token[3],
                lexeme=token[0]
            )
        if ops[0][0] == '=>' and len(ops) > 1:
            token = ops[0]
            raise HarmonyCompilerError(
                message="Boolean imply expression too complicated: use parentheses",
                filename=self.file,
                line=token[2],
                column=token[3],
                lexeme=token[0]
            )
        return NaryAST(exprs[-1].endtoken, exprs[0].token, ops[0], exprs)

    # Visit a parse tree produced by HarmonyParser#logic_op.
    def visitLogic_op(self, ctx: HarmonyParser.Logic_opContext):
        return self.get_token(ctx.start, ctx.getText())

    # Visit a parse tree produced by HarmonyParser#compare_op.
    def visitCompare_op(self, ctx: HarmonyParser.Compare_opContext):
        return self.get_token(ctx.start, ctx.getText())

    # Visit a parse tree produced by HarmonyParser#logic_expr.
    def visitLogic_expr(self, ctx: HarmonyParser.Logic_exprContext):
        exprs = [self.visit(e) for e in ctx.compare_expr()]
        if not ctx.logic_op():
            return exprs[0]
        ops = [self.visit(o) for o in ctx.logic_op()]
        return self.bool_expr(ops, exprs)

    # Visit a parse tree produced by HarmonyParser#compare_expr.
    def visitCompare_expr(self, ctx: HarmonyParser.Compare_exprContext):
        exprs = [self.visit(e) for e in ctx.arith_expr()]
        if not ctx.compare_op():
            return exprs[0]
        ops = [self.visit(o) for o in ctx.compare_op()]
        return self.cmp_expr(ops, exprs)

    # Visit a parse tree produced by HarmonyParser#arith_expr.
    def visitArith_expr(self, ctx: HarmonyParser.Arith_exprContext):
        exprs = [self.visit(e) for e in ctx.expr_rule()]
        if not ctx.arith_op():
            return exprs[0]
        ops = [self.visit(o) for o in ctx.arith_op()]
        return self.arith_expr(ops, exprs)

    # Visit a parse tree produced by HarmonyParser#nary_expr.
    def visitNary_expr(self, ctx: HarmonyParser.Nary_exprContext):
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        if ctx.IF():
            expressions = [self.visit(e) for e in ctx.expr_rule()]
            condition = self.visit(ctx.nary_expr())
            expressions.insert(1, condition)
            op_token = self.get_token(ctx.IF().symbol, str(ctx.IF()))
            return NaryAST(endtoken, tkn, op_token, expressions)
        if ctx.IN():
            expressions = [self.visit(e) for e in ctx.expr_rule()]
            in_token = self.get_token(ctx.IN().symbol, str(ctx.IN()))
            ast = NaryAST(endtoken, tkn, in_token, expressions)
            if ctx.NOT():
                not_token = self.get_token(ctx.NOT().symbol, str(ctx.NOT()))
                return NaryAST(endtoken, tkn, not_token, [ast])
            return ast
        return self.visit(ctx.logic_expr())

    # Visit a parse tree produced by HarmonyParser#expr_rule.
    def visitExpr_rule(self, ctx:HarmonyParser.Expr_ruleContext):
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        if ctx.SETINTLEVEL():
            expr = self.visit(ctx.expr_rule())
            return SetIntLevelAST(endtoken, tkn, expr)
        if ctx.SAVE():
            expr = self.visit(ctx.expr_rule())
            return SaveAST(endtoken, tkn, expr)
        if ctx.STOP():
            expr = self.visit(ctx.expr_rule())
            return StopAST(endtoken, tkn, expr)
        if ctx.question_operand():
            # '?' (address-of) - deliberately not part of unary_op (see the
            # comment above unary_op in Harmony.g4); it has its own operand
            # rule (question_operand) with its own restricted grammar/shape,
            # validated ahead of time by harmony_parser.py's Phase 0
            # pre-check, so all that's needed here is to build the AST the
            # operand describes and wrap it.
            expr = self.visit(ctx.question_operand())
            return AddressAST(endtoken, expr, tkn)
        if ctx.unary_op():
            op = self.visit(ctx.unary_op())
            if op[0] == '!':
                expr = self.visit(ctx.expr_rule())
                return PointerAST(endtoken, expr, tkn)
            else:
                expr = self.visit(ctx.expr_rule())
                return NaryAST(endtoken, tkn, op, [expr])
        if ctx.application():
            return self.visit(ctx.application())
        raise HarmonyCompilerError(
            message="Invalid expression",
            filename=self.file,
            line=tkn[2],
            column=tkn[3],
            lexeme=tkn[0]
        )

    # Visit a parse tree produced by HarmonyParser#question_operand.
    #
    # question_operand ::= NAME (ARROWID | basic_expr)*
    #                     | '(' question_operand ')' (ARROWID | basic_expr)*
    #                     | '!' expr_rule (ARROWID | basic_expr)*
    #                     | INT | BOOL | ATOM | STRING | NONE
    #
    # harmony_parser.py (Phase 0) has already validated that this operand is
    # legal for '?' to be applied to - this visitor's only job is to build
    # the same AST an equivalent application/'->' chain would build, which
    # visitExpr_rule's '?' handling then wraps in an AddressAST. The
    # construction below mirrors visitApplication's own ARROWID/basic_expr
    # folding, just walking a flat repetition (ctx.children) instead of
    # ANTLR's left-recursive application chain - ARROWID and basic_expr
    # occurrences have to stay in their original left-to-right order, and
    # the generated context's own ARROWID()/basic_expr() accessors return
    # each kind separately, losing that interleaving.
    # A bare literal CONSTANT - INT/BOOL/ATOM/STRING/NONE - is one of
    # question_operand's alternatives in Harmony.g4 (e.g. "?5"), but
    # (unlike NAME/'('/'!') takes no trailing (ARROWID | basic_expr)*
    # chain, so it's parsed as a plain literal, not a chain base -
    # this builds exactly the ConstantAST visitInt/visitBool/visitAtom/
    # visitStr/visitNone (above) would build for the same token as a
    # basic_expr, so "?5" and "5" agree on what the literal 5 means.
    def _question_operand_literal(self, terminal):
        symbol = terminal.symbol
        text = terminal.getText()
        endtoken = self.get_token(symbol, text)
        ttype = symbol.type
        if ttype == HarmonyParser.INT:
            tkn = self.get_token(symbol, int(text, 0))
        elif ttype == HarmonyParser.BOOL:
            tkn = self.get_token(symbol, text == 'True')
        elif ttype == HarmonyParser.ATOM:
            if text.startswith("0x"):
                tkn = self.get_token(symbol, chr(int(text, 16)))
            else:
                tkn = self.get_token(symbol, text[1:])
        elif ttype == HarmonyParser.STRING:
            if text.startswith("'''") and text.endswith("'''"):
                s = text[3:-3]
            elif text.startswith('\"\"\"') and text.endswith('\"\"\"'):
                s = text[3:-3]
            elif text.startswith("'") and text.endswith("'"):
                s = text[1:-1]
            elif text.startswith('\"') and text.endswith('\"'):
                s = text[1:-1]
            else:
                raise HarmonyCompilerError(
                    message="Unable to parse string",
                    filename=self.file,
                    line=symbol.line,
                    column=symbol.column + 1,
                    lexeme=text,
                )
            tkn = self.get_token(symbol, s)
        else:
            assert ttype == HarmonyParser.NONE
            tkn = self.get_token(symbol, AddressValue(None, []))
        return ConstantAST(endtoken, tkn)

    def visitQuestion_operand(self, ctx: HarmonyParser.Question_operandContext):
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        if ctx.OPEN_PAREN():
            # '(' question_operand ')' (ARROWID | basic_expr)* - the parens
            # recurse rather than just being seen through, since (unlike a
            # bare NAME) the parenthesized alternative may itself be
            # followed by more chain material: "?(!p)[x]" needs somewhere
            # for the trailing "[x]" to attach once '!p' is wrapped in
            # parens (see the question_operand comment in Harmony.g4).
            result = self.visit(ctx.question_operand())
            rest = ctx.children[3:]
        elif ctx.NAME():
            name_tok = self.get_token(ctx.NAME().symbol, str(ctx.NAME()))
            result = NameAST(name_tok, name_tok)
            rest = ctx.children[1:]
        elif ctx.INT():
            return self._question_operand_literal(ctx.INT())
        elif ctx.BOOL():
            return self._question_operand_literal(ctx.BOOL())
        elif ctx.ATOM():
            return self._question_operand_literal(ctx.ATOM())
        elif ctx.STRING():
            return self._question_operand_literal(ctx.STRING())
        elif ctx.NONE():
            return self._question_operand_literal(ctx.NONE())
        else:
            expr = self.visit(ctx.expr_rule())
            result = PointerAST(endtoken, expr, tkn)
            rest = ctx.children[2:]
        for child in rest:
            if isinstance(child, TerminalNode) and child.getSymbol().type == HarmonyParser.ARROWID:
                name = self.get_token(child.getSymbol(), child.getText())
                (lexeme, file, line, col) = name
                lexeme = lexeme[2:]
                col += 2
                while lexeme[0] == ' ':
                    lexeme = lexeme[1:]
                    col += 1
                result = ApplyAST(endtoken, PointerAST(endtoken, result, tkn), ConstantAST(endtoken, (lexeme, file, line, col)), tkn)
            else:
                arg = self.visit(child)
                result = ApplyAST(endtoken, result, arg, tkn)
        return result

    # Visit a parse tree produced by HarmonyParser#application.
    def visitApplication(self, ctx:HarmonyParser.ApplicationContext):
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        if ctx.ARROWID():
            p = self.visit(ctx.application())
            name = self.get_token(ctx.ARROWID().symbol, str(ctx.ARROWID()))
            (lexeme, file, line, col) = name
            lexeme = lexeme[2:]
            col += 2
            while lexeme[0] == ' ':
                lexeme = lexeme[1:]
                col += 1
            return ApplyAST(endtoken, PointerAST(endtoken, p, tkn), ConstantAST(endtoken, (lexeme, file, line, col)), tkn)
        elif ctx.application():
            f = self.visit(ctx.application())
            return ApplyAST(endtoken, f, self.visit(ctx.basic_expr()), tkn)
        else:
            return self.visit(ctx.basic_expr())
