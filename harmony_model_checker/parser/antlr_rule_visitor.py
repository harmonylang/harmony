from typing import Any, Union
from antlr4.Token import CommonToken

from harmony_model_checker.parser.HarmonyVisitor import HarmonyVisitor
from harmony_model_checker.parser.HarmonyParser import HarmonyParser
from harmony_model_checker.harmony.harmony import *
import math

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
        return BlockAST(endtoken, tkn, False, stmts)

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

    # Visit a parse tree produced by HarmonyParser#comp_op.
    def visitComp_op(self, ctx: HarmonyParser.Comp_opContext):
        return self.get_token(ctx.start, ctx.getText())

    # Visit a parse tree produced by HarmonyParser#unary_op.
    def visitUnary_op(self, ctx: HarmonyParser.Unary_opContext):
        return self.get_token(ctx.start, ctx.getText())

    # Visit a parse tree produced by HarmonyParser#int.
    def visitInt(self, ctx: HarmonyParser.IntContext):
        txt = ctx.getText()
        tkn = self.get_token(ctx.start, int(txt))
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
        txt = ctx.getText()
        tkn = self.get_token(ctx.start, txt)
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
        cond = self.visit(ctx.expr())
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return PrintAST(endtoken, tkn, False, cond)

    # Visit a parse tree produced by HarmonyParser#none.
    def visitNone(self, ctx: HarmonyParser.NoneContext):
        tkn = self.get_token(ctx.start, AddressValue([]))
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return ConstantAST(endtoken, tkn)

    # Visit a parse tree produced by HarmonyParser#address.
    def visitAddress(self, ctx: HarmonyParser.AddressContext):
        expr = self.visit(ctx.expr_rule())
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return AddressAST(endtoken, tkn, expr)

    # Visit a parse tree produced by HarmonyParser#aug_assign_op.
    def visitAug_assign_op(self, ctx: HarmonyParser.Aug_assign_opContext):
        return self.get_token(ctx.start, ctx.getText())

    # Visit a parse tree produced by HarmonyParser#expr_stmt.
    def visitExpr_stmt(self, ctx: HarmonyParser.Expr_stmtContext):
        e = self.visit(ctx.tuple_rule())
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return CallAST(endtoken, tkn, False, e)

    # Visit a parse tree produced by HarmonyParser#assign_stmt.
    def visitAssign_stmt(self, ctx: HarmonyParser.Assign_stmtContext):
        expr = [self.visit(e) for e in ctx.tuple_rule()]
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return AssignmentAST(endtoken, tkn, expr[:-1], expr[-1], self.get_token(ctx.start, '='), False)

    # Visit a parse tree produced by HarmonyParser#aug_assign_stmt.
    def visitAug_assign_stmt(self, ctx: HarmonyParser.Aug_assign_stmtContext):
        op = self.visit(ctx.aug_assign_op())
        expressions = [self.visit(e) for e in ctx.tuple_rule()]
        lhs = expressions[:-1]
        rhs = expressions[-1]
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return AssignmentAST(endtoken, tkn, lhs, rhs, op, False)

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
        return LetWhenAST(endtoken, tkn, False, [('cond', cond)], PassAST(endtoken, tkn, False))

    # Visit a parse tree produced by HarmonyParser#trap_stmt.
    def visitTrap_stmt(self, ctx: HarmonyParser.Trap_stmtContext):
        func = self.visit(ctx.expr())
        if not isinstance(func, ApplyAST):
            tkn = self.get_token(func.ast_token, func.ast_token[0])
            raise HarmonyCompilerError(
                message="Expected a method call but found something else.",
                filename=self.file,
                line=tkn[2],
                column=tkn[3],
                lexeme=tkn[0]
            )
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return TrapAST(endtoken, tkn, False, func.method, func.arg)

    # Visit a parse tree produced by HarmonyParser#pass_stmt.
    def visitPass_stmt(self, ctx: HarmonyParser.Pass_stmtContext):
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return PassAST(endtoken, tkn, False)

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
            a.atomically = True
            return a
        return super().visitSimple_stmt(ctx)

    def visitCompound_stmt(self, ctx: HarmonyParser.Compound_stmtContext):
        if ctx.ATOMICALLY():
            a = self.visit(ctx.children[-1])
            assert isinstance(a, AST)
            a.atomically = True
            return a
        return super().visitCompound_stmt(ctx)

    # Visit a parse tree produced by HarmonyParser#spawn_stmt.
    def visitSpawn_stmt(self, ctx: HarmonyParser.Spawn_stmtContext):
        is_eternal = ctx.ETERNAL() is not None
        target = self.visit(ctx.expr())
        if not isinstance(target, ApplyAST):
            tkn = self.get_token(target.ast_token, target.ast_token[0])
            raise HarmonyCompilerError(
                message="Expected a method call but found something else.",
                filename=self.file,
                line=tkn[2],
                column=tkn[3],
                lexeme=tkn[0]
            )
        method, arg = target.method, target.arg
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return SpawnAST(endtoken, tkn, False, method, arg, None, is_eternal)

    # Visit a parse tree produced by HarmonyParser#go_stmt.
    def visitGo_stmt(self, ctx: HarmonyParser.Go_stmtContext):
        target = self.visit(ctx.expr(0))
        args = self.visit(ctx.expr(1))
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return GoAST(endtoken, tkn, False, target, args)

    # Visit a parse tree produced by HarmonyParser#sequential_stmt.
    def visitSequential_stmt(self, ctx: HarmonyParser.Sequential_stmtContext):
        expr = [self.visit(e) for e in ctx.expr()]
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return SequentialAST(endtoken, tkn, False, expr)

    # Visit a parse tree produced by HarmonyParser#atomic_block.
    def visitAtomic_block(self, ctx: HarmonyParser.Atomic_blockContext):
        stmts = self.visit(ctx.block())
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return AtomicAST(endtoken, tkn, True, stmts)

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
        return "var", lvalues, values

    # Visit a parse tree produced by HarmonyParser#when_decl.
    def visitWhen_decl(self, ctx:HarmonyParser.When_declContext):
        expr = self.visit(ctx.expr())
        if ctx.EXISTS() is not None:
            bv = self.visit(ctx.bound())
            return 'exists', bv, expr
        else:
            return 'cond', expr

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

    # Visit a parse tree produced by HarmonyParser#method_decl.
    def visitMethod_decl(self, ctx: HarmonyParser.Method_declContext):
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        value = str(ctx.NAME())
        method_name = self.get_token(ctx.NAME().symbol, value)
        args = self.visit(ctx.bound()) if ctx.bound() else []
        body = self.visit(ctx.block())
        ast = MethodAST(endtoken, tkn, False, method_name, args, body)
        return ast

    # Visit a parse tree produced by HarmonyParser#while_block.
    def visitWhile_block(self, ctx: HarmonyParser.While_blockContext):
        cond = self.visit(ctx.expr())
        stmts = self.visit(ctx.block())
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        return WhileAST(endtoken, tkn, False, cond, stmts)

    # Visit a parse tree produced by HarmonyParser#if_block.
    def visitIf_block(self, ctx: HarmonyParser.If_blockContext):
        cond = self.visit(ctx.expr())
        if_block = self.visit(ctx.block())
        alts = [(cond, if_block, self.file, ctx.start.line)]
        else_block = None
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        if ctx.elif_block() is not None:
            for c in ctx.elif_block():
                alts.append(self.visit(c))
        if ctx.else_block() is not None:
            else_block = self.visit(ctx.else_block())
        return IfAST(endtoken, tkn, False, alts, else_block)

    # Visit a parse tree produced by HarmonyParser#elif_block.
    def visitElif_block(self, ctx: HarmonyParser.Elif_blockContext):
        cond = self.visit(ctx.expr())
        stmts = self.visit(ctx.block())
        return cond, stmts, self.file, ctx.start.line

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
            return BlockAST(endtoken, tkn, False, stmts)
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
            block = BlockAST(endtoken, tkn, False, stmt_block)
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
            return BlockAST(endtoken, tkn, False, self.visit(ctx.one_line_stmt()))
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
        return [self.visit(e) for e in ctx.children]

    # Visit a parse tree produced by HarmonyParser#for_parse.
    def visitFor_parse(self, ctx: HarmonyParser.For_parseContext):
        l1 = self.visit(ctx.bound(0))
        l2 = self.visit(ctx.bound(1)) if ctx.bound(1) else None
        expr = self.visit(ctx.nary_expr())
        if l2 is not None:
            return "for", (l2, l1, expr)
        else:
            return "for", (l1, None, expr)

    # Visit a parse tree produced by HarmonyParser#where_parse.
    def visitWhere_parse(self, ctx: HarmonyParser.Where_parseContext):
        expr = self.visit(ctx.nary_expr())
        return "where", expr

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

    # Visit a parse tree produced by HarmonyParser#nary_expr.
    def visitNary_expr(self, ctx: HarmonyParser.Nary_exprContext):
        expressions = [self.visit(e) for e in ctx.expr_rule()]
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        if ctx.comp_op():
            comps = [self.visit(o) for o in ctx.comp_op()]
            return CmpAST(endtoken, tkn, comps, expressions)
        if ctx.arith_op():
            ops = [self.visit(o) for o in ctx.arith_op()]
            expected = ops[0]
            if expected[0] not in self.associative_operators and len(ops) > 1:
                second_op = ops[1]
                raise HarmonyCompilerError(
                    message=f"Cannot have expression with multiple non-associative operators.",
                    filename=self.file,
                    line=second_op[2],
                    column=second_op[3],
                    lexeme=second_op[0]
                )
            for actual in ops[1:]:
                if actual[0] != expected[0]:
                    raise HarmonyCompilerError(
                        message=f"Cannot have multiple types of operators in one expression. Expected {expected[0]} but got {actual[0]}",
                        filename=self.file,
                        line=actual[2],
                        column=actual[3],
                        lexeme=actual[0]
                    )
            binop = ops[0]
            return NaryAST(endtoken, tkn, binop, expressions)
        if ctx.IF():
            condition = self.visit(ctx.nary_expr())
            expressions.insert(1, condition)
            op_token = self.get_token(ctx.IF().symbol, str(ctx.IF()))
            return NaryAST(endtoken, tkn, op_token, expressions)
        if ctx.IN():
            in_token = self.get_token(ctx.IN().symbol, str(ctx.IN()))
            ast = NaryAST(endtoken, tkn, in_token, expressions)
            if ctx.NOT():
                not_token = self.get_token(ctx.NOT().symbol, str(ctx.NOT()))
                return NaryAST(endtoken, tkn, not_token, [ast])
            return ast
        return expressions[0]

    # Visit a parse tree produced by HarmonyParser#expr_rule.
    def visitExpr_rule(self, ctx:HarmonyParser.Expr_ruleContext):
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        if ctx.LAMBDA():
            args = self.visit(ctx.bound()) if ctx.bound() is not None else []
            body = self.visit(ctx.nary_expr())
            return LambdaAST(endtoken, args, body, tkn, False)
        if ctx.SETINTLEVEL():
            expr = self.visit(ctx.expr_rule())
            return SetIntLevelAST(endtoken, tkn, expr)
        if ctx.SAVE():
            expr = self.visit(ctx.expr_rule())
            return SaveAST(endtoken, tkn, expr)
        if ctx.STOP():
            expr = self.visit(ctx.expr_rule())
            return StopAST(endtoken, tkn, expr)
        if ctx.POINTER_OF():
            expr = self.visit(ctx.expr_rule())
            return PointerAST(endtoken, expr, tkn)
        if ctx.unary_op():
            op = self.visit(ctx.unary_op())
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

    # Visit a parse tree produced by HarmonyParser#application.
    def visitApplication(self, ctx:HarmonyParser.ApplicationContext):
        tkn = self.get_token(ctx.start, ctx.start.text)
        endtoken = self.get_token(ctx.stop, ctx.stop.text)
        if ctx.ARROW():
            p = self.visit(ctx.application())
            name = self.get_token(ctx.NAME().symbol, str(ctx.NAME()))
            return ApplyAST(endtoken, PointerAST(endtoken, p, tkn), ConstantAST(endtoken, name), tkn)
        elif ctx.application():
            f = self.visit(ctx.application())
            return ApplyAST(endtoken, f, self.visit(ctx.basic_expr()), tkn)
        else:
            return self.visit(ctx.basic_expr())
