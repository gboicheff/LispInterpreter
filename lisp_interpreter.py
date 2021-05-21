from lisp_token import TokenType
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
        self.vars = dict()
        self.funcs = dict()

    def init_var(self, name, value):                
        if name in self.vars:
            raise ScopeException(name, "Variable already defined in this scope")
        else:
            self.vars[name] = value # allow dynamic override

    def update_var(self, name, value):
        if not name in self.vars:
            if self.parent_scope != None:
                if not name in self.parent_scope.vars:
                    raise ScopeException(name, "Variable not defined in this scope")
                else:
                    self.parent_scope.update_var(name, value)
            else:
                raise ScopeException(name, "Variable not defined in this scope")
        else:
            self.vars[name] = value
    
    def get_var(self, name):
        if name in self.vars:
            return self.vars[name]
        else:
            if self.parent_scope != None:
                if name in self.parent_scope.vars:
                    return self.parent_scope.get_var(name)
                else:
                    raise ScopeException(name, "Variable not defined in this scope")
            else:
                raise ScopeException(name, "Variable not defined in this scope")

    def dec_func(self, name, ast):
        if name in self.funcs:
            raise ScopeException(name, "Function already defined in this scope")
        else:
            self.funcs[name] = ast
        
    def get_func(self, name):
        if name in self.funcs:
            return self.funcs[name]
        else:
            if self.parent_scope != None:
                if name in self.parent_scope.funcs:
                    return self.parent_scope.get_func(name)
                else:
                    raise ScopeException(name, "Function not defined in this scope")
            else:
                raise ScopeException(name, "Function not defined in this scope")


    
class InterpretException(Exception):
    def __init__(self, ast, message="Exception occured while executing"):
        self.ast = ast
        self.message = message
        super().__init__(self.message)



class STLFunc:
    # num_args=-1 when the function can take an arbitrary number of arguments
    def __init__(self, name, func, num_args=-1):
        self.name = name
        self.num_args = num_args # -1 for any number of args, -2 for 1 or more args
        self.func = func
    
    def check_arg_count(self, other_count):
        if self.num_args == -1:
            return True
        elif self.num_args == -2 and other_count > 0:
            return True
        elif self.num_args == other_count:
            return True
        else:
            return False

class Interpreter:
    def __init__(self):
        pass

    def interpret(self, ast):
        self.ast = ast
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        self.stl_funcs = self.init_stl()
        self.global_scope.init_var("t", True) # set t to true

        return self.eval(ast)

    def eval(self, ast):
        if isinstance(ast, lisp_Expr):
            return self.eval_expr(ast)
        else:
            return self.eval_terminal(ast)

    def eval_expr(self, expr):
        if len(expr.args) == 0: # handle NIL
            return False

        if not self.is_ID(expr.args[0]):
            raise InterpretException(expr, "First term must be an ID")
        else:
            func_name = expr.args[0].token.literal
            if func_name == "let":
                return self.eval_let(expr)
            elif func_name == "do":
                return self.eval_do(expr)
            elif func_name == "defvar":
                return self.eval_def_var(expr)
            else:
                if not func_name in self.stl_funcs:
                    raise InterpretException(expr)
                
                if not self.stl_funcs[func_name].check_arg_count(len(expr.args) - 1):
                    raise InterpretException(expr, "Incorrect number of arguments")

                return self.stl_funcs[func_name].func(tuple(self.eval(arg) for arg in expr.args[1:]))


    def eval_terminal(self, terminal):
        if terminal.token.type == TokenType.ID:
            return self.current_scope.get_var(terminal.token.literal)
        else:
            return terminal.token.literal
    
    def eval_let(self, let_ast):

        if not len(let_ast.args) > 2:
            raise InterpretException(let_ast, "Too few args for let")

        var_init_exprs = let_ast.args[1]
        if not len(var_init_exprs.args):
            raise InterpretException(let_ast, "No variables to define in let")


        var_init_dict = dict()
        for var_init_expr in var_init_exprs.args:
            if len(var_init_expr.args) != 2:
                raise InterpretException(var_init_expr)

            if not self.is_ID(var_init_expr.args[0]):
                raise InterpretException(var_init_expr) # requires ID

            var_init_dict[var_init_expr.args[0].token.literal] = self.eval(var_init_expr.args[1])
        
        self.current_scope = Scope(self.current_scope)

        for name in var_init_dict.keys():
            self.current_scope.init_var(name, var_init_dict[name])


        return_val = self.eval_args(let_ast.args[2:])


        self.current_scope = self.current_scope.parent_scope
    
        return return_val

    def eval_def_var(self, def_var_ast):
        if not len(def_var_ast.args) > 1:
            raise InterpretException(def_var_ast, "Too few args for defvar")  
        self.global_scope.init_var(self.eval(def_var_ast.args[1]))

    def eval_do(self, do_ast):
        if not len(do_ast.args) > 1:
            raise InterpretException(do_ast, "Too few args for let")

        self.current_scope = Scope(self.current_scope)

        return_val = self.eval_args(do_ast.args[1:])

        self.current_scope = self.current_scope.parent_scope

        return return_val

    
    def eval_args(self, args):
        for index,arg_ast in enumerate(args):
            arg_return = self.eval(arg_ast)
            if index == len(args)-1:
                return arg_return
            


    def is_ID(self, ast):
        return isinstance(ast, lisp_Terminal) and ast.token.type == TokenType.ID


    def division(self, args):
        if len(args) == 1:
            return 1/args[0]
        else:
            x = args[0]
            for y in args[1:]:
                x /= y
            return x

    # needs more functions
    def init_stl(self):
        stl = {
            "+": STLFunc("+", lambda args: sum(args)),
            "-": STLFunc("-", lambda args: 0 if len(args) == 0 else -args[0] if len(args) == 1 else args[0] - sum(args[1:])),
            "*": STLFunc("*", lambda args: math.prod(args)),
            "/": STLFunc("/", lambda args: division(args), -2),
            "write": STLFunc("write", lambda args: print(args[0])),
            "exp": STLFunc("exp", lambda args: math.exp(args[0]), 1),
            "sin": STLFunc("sin", lambda args: math.sin(args[0]), 1),
            "cos": STLFunc("cos", lambda args: math.cos(args[0]), 1),
            "tan": STLFunc("tan", lambda args: math.tan(args[0]), 1), 
            "max": STLFunc("max", lambda args: max(args)), 
            "min": STLFunc("min", lambda args: min(args)),
            "=":  STLFunc("=", lambda args: equality(args),-2)
        }
        return stl

def equality(args):
    equal = True
    arg0 = args[0]
    for arg in args[1:]:
        equal = equal and arg0 == arg
    return equal
def division(args):
        if len(args) == 1:
            return 1/args[0]
        else:
            x = args[0]
            all_int = isinstance(x, int)
            for y in args[1:]:
                all_int = all_int and isinstance(y, int)

            for y in args[1:]:
                if y == 0:
                    raise Exception("Division by zero") # change the error type to interpret?
                if all_int:
                    x //= y
                else:
                    x /= y
            return x