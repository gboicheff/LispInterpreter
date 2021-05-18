from lisp_ast import lisp_List


class Interpreter:
    def __init__(self):
        pass

    def interpret(self, ast):
        self.ast = ast

    def eval(self, ast):
        return self.eval_list(ast)

    def eval_list(self, list):
        pass

    def eval_expr(self, expr):
        if isinstance(expr.value, lisp_List):
            return self.eval_list(expr.value)
        else:
            return self.eval_terminal(expr.value)

    def eval_terminal(self, terminal):
        return terminal.token.literal
