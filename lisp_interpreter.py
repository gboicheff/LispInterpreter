from lisp_ast import lisp_Expr, lisp_Terminal
import math



# https://www.cs.iusb.edu/~dvrajito/teach/c311/c311_elisp2.html
class ScopeException(Exception):
    def __init__(self, name, message="Scope exception"):
        self.name = name
        self.message = message
        super().__init__(self.message)

class Scope:
    def __init__(self, parent_scope=None):
        self.parent_scope = parent_scope
        self.scope = dict()

    def init_var(self, name, value):
        if name in self.scope:
            raise ScopeException(name, "Variable already defined")
        else:
            self.scope[name] = value

    def update_var(self, name, value):
        if name not in self.scope:
            raise ScopeException(name, "Variable not defined")
        else:
            self.scope[name] = value

class Interpreter:
    def __init__(self):
        pass

    def interpret(self, ast):
        self.ast = ast

    def eval(self, ast):
        if isinstance(ast, lisp_Expr):
            return self.eval_expr(ast)
        else:
            return self.eval_terminal(ast)

    def eval_expr(self, expr):
        pass

    def eval_terminal(self, terminal):
        return terminal.token.literal

    # needs more functions
    def init_stl(self):
        stl = {
            "+": lambda x,y: x+y,
            "-": lambda x,y: x-y,
            "*": lambda x,y: x*y,
            "/": lambda x,y: x/y,
            "^": lambda x,y: x**y,
            "%": lambda x,y: x%y,
            "exp": lambda x: math.exp(x),
            "sin": lambda x: math.sin(x),
            "cos": lambda x: math.cos(x),
            "tan": lambda x: math.tan(x),
            "floor": lambda x: math.floor(x),            
            "ceil": lambda x: math.ceil(x),      
            "round": lambda x: round(x), 
        }
        return stl
