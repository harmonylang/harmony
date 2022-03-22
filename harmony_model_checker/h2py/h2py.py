from harmony_model_checker.h2py.H2PyStmtVisitor import H2PyStmtVisitor
import harmony_model_checker.harmony.ast as hast

import ast as past


def h2py(hast: hast.AST) -> past.AST:
    stmt_visitor = H2PyStmtVisitor()
    return past.Module(
        body=stmt_visitor(hast),
        type_ignores=[]
    )
