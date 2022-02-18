# Generated from Harmony.g4 by ANTLR 4.9.3
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .HarmonyParser import HarmonyParser
else:
    from HarmonyParser import HarmonyParser

# This class defines a complete generic visitor for a parse tree produced by HarmonyParser.

class HarmonyVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by HarmonyParser#program.
    def visitProgram(self, ctx:HarmonyParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#import_stmt.
    def visitImport_stmt(self, ctx:HarmonyParser.Import_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#import_name.
    def visitImport_name(self, ctx:HarmonyParser.Import_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#import_from.
    def visitImport_from(self, ctx:HarmonyParser.Import_fromContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#import_names_seq.
    def visitImport_names_seq(self, ctx:HarmonyParser.Import_names_seqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#tuple_bound.
    def visitTuple_bound(self, ctx:HarmonyParser.Tuple_boundContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#bound.
    def visitBound(self, ctx:HarmonyParser.BoundContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#arith_op.
    def visitArith_op(self, ctx:HarmonyParser.Arith_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#comp_op.
    def visitComp_op(self, ctx:HarmonyParser.Comp_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#unary_op.
    def visitUnary_op(self, ctx:HarmonyParser.Unary_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#int.
    def visitInt(self, ctx:HarmonyParser.IntContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#bool.
    def visitBool(self, ctx:HarmonyParser.BoolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#atom.
    def visitAtom(self, ctx:HarmonyParser.AtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#name.
    def visitName(self, ctx:HarmonyParser.NameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#str.
    def visitStr(self, ctx:HarmonyParser.StrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#none.
    def visitNone(self, ctx:HarmonyParser.NoneContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#set_rule_1.
    def visitSet_rule_1(self, ctx:HarmonyParser.Set_rule_1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#paren_tuple.
    def visitParen_tuple(self, ctx:HarmonyParser.Paren_tupleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#bracket_tuple.
    def visitBracket_tuple(self, ctx:HarmonyParser.Bracket_tupleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#address.
    def visitAddress(self, ctx:HarmonyParser.AddressContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#set_rule.
    def visitSet_rule(self, ctx:HarmonyParser.Set_ruleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#iter_parse.
    def visitIter_parse(self, ctx:HarmonyParser.Iter_parseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#for_parse.
    def visitFor_parse(self, ctx:HarmonyParser.For_parseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#where_parse.
    def visitWhere_parse(self, ctx:HarmonyParser.Where_parseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#tuple_rule.
    def visitTuple_rule(self, ctx:HarmonyParser.Tuple_ruleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#nary_expr.
    def visitNary_expr(self, ctx:HarmonyParser.Nary_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#expr_rule.
    def visitExpr_rule(self, ctx:HarmonyParser.Expr_ruleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#application.
    def visitApplication(self, ctx:HarmonyParser.ApplicationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#expr.
    def visitExpr(self, ctx:HarmonyParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#aug_assign_op.
    def visitAug_assign_op(self, ctx:HarmonyParser.Aug_assign_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#expr_stmt.
    def visitExpr_stmt(self, ctx:HarmonyParser.Expr_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#assign_stmt.
    def visitAssign_stmt(self, ctx:HarmonyParser.Assign_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#aug_assign_stmt.
    def visitAug_assign_stmt(self, ctx:HarmonyParser.Aug_assign_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#const_assign_stmt.
    def visitConst_assign_stmt(self, ctx:HarmonyParser.Const_assign_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#assert_stmt.
    def visitAssert_stmt(self, ctx:HarmonyParser.Assert_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#await_stmt.
    def visitAwait_stmt(self, ctx:HarmonyParser.Await_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#var_stmt.
    def visitVar_stmt(self, ctx:HarmonyParser.Var_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#trap_stmt.
    def visitTrap_stmt(self, ctx:HarmonyParser.Trap_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#pass_stmt.
    def visitPass_stmt(self, ctx:HarmonyParser.Pass_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#invariant_stmt.
    def visitInvariant_stmt(self, ctx:HarmonyParser.Invariant_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#del_stmt.
    def visitDel_stmt(self, ctx:HarmonyParser.Del_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#spawn_stmt.
    def visitSpawn_stmt(self, ctx:HarmonyParser.Spawn_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#go_stmt.
    def visitGo_stmt(self, ctx:HarmonyParser.Go_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#print_stmt.
    def visitPrint_stmt(self, ctx:HarmonyParser.Print_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#sequential_stmt.
    def visitSequential_stmt(self, ctx:HarmonyParser.Sequential_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#atomic_block.
    def visitAtomic_block(self, ctx:HarmonyParser.Atomic_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#for_block.
    def visitFor_block(self, ctx:HarmonyParser.For_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#let_decl.
    def visitLet_decl(self, ctx:HarmonyParser.Let_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#when_decl.
    def visitWhen_decl(self, ctx:HarmonyParser.When_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#let_when_decl.
    def visitLet_when_decl(self, ctx:HarmonyParser.Let_when_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#let_when_block.
    def visitLet_when_block(self, ctx:HarmonyParser.Let_when_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#method_decl.
    def visitMethod_decl(self, ctx:HarmonyParser.Method_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#while_block.
    def visitWhile_block(self, ctx:HarmonyParser.While_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#elif_block.
    def visitElif_block(self, ctx:HarmonyParser.Elif_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#else_block.
    def visitElse_block(self, ctx:HarmonyParser.Else_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#if_block.
    def visitIf_block(self, ctx:HarmonyParser.If_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#block_stmts.
    def visitBlock_stmts(self, ctx:HarmonyParser.Block_stmtsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#block.
    def visitBlock(self, ctx:HarmonyParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#normal_block.
    def visitNormal_block(self, ctx:HarmonyParser.Normal_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#simple_stmt.
    def visitSimple_stmt(self, ctx:HarmonyParser.Simple_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#compound_stmt.
    def visitCompound_stmt(self, ctx:HarmonyParser.Compound_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#one_line_stmt.
    def visitOne_line_stmt(self, ctx:HarmonyParser.One_line_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#label.
    def visitLabel(self, ctx:HarmonyParser.LabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HarmonyParser#stmt.
    def visitStmt(self, ctx:HarmonyParser.StmtContext):
        return self.visitChildren(ctx)



del HarmonyParser