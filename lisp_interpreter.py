from lisp_token import TokenType
from lisp_ast import lisp_Expr, lisp_Terminal
import math
from functools import partial


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
                return self.parent_scope.get_var(name)
            else:
                raise ScopeException(name, "Variable not defined in this scope")

    def dec_func(self, func):
        if func.name in self.funcs:
            raise ScopeException(func.name, "Function already defined in this scope")
        else:
            self.funcs[func.name] = func
        
    def get_func(self, name):
        if name in self.funcs:
            return self.funcs[name]
        else:
            if self.parent_scope != None:
                    return self.parent_scope.get_func(name)
            else:
                raise ScopeException(name, "Function not defined in this scope")


    
class InterpretException(Exception):
    def __init__(self, ast, message="Exception occured while executing"):
        self.ast = ast
        self.message = message
        super().__init__(self.message)

class Func:
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
        for func in self.init_stl():  # TODO this is kind of jank
            self.global_scope.dec_func(func)
        self.current_scope = self.global_scope


        self.global_scope.init_var("t", True) # set t to true
        self.global_scope.init_var("NIL", False) 

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
            elif func_name == "while":
                return self.eval_while(expr)
            elif func_name == "setq":
                return self.eval_set_q(expr)
            elif func_name == "dotimes":
                return self.eval_do_times(expr)
            elif func_name == "list":
                return self.eval_list(expr)
            elif func_name == "defun":
                return self.eval_de_fun(expr)
            elif func_name == "if":
                return self.eval_if(expr)
            else:
                func = self.current_scope.get_func(func_name)
                if not func.check_arg_count(len(expr.args) - 1):
                    raise InterpretException(expr, "Incorrect number of arguments")

                return func.func(tuple(self.eval(arg) for arg in expr.args[1:]))


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

    def eval_while(self, while_ast):
        if not len(while_ast.args) > 1:
            raise InterpretException(while_ast, "Too few args for while")
        while self.eval(while_ast.args[1]):
            self.eval_args(while_ast.args[2:])

        return False # always returns NIL?

    def eval_args(self, args):
        for index,arg_ast in enumerate(args):
            arg_return = self.eval(arg_ast)
            if index == len(args)-1:
                return arg_return
            


    def is_ID(self, ast):
        return isinstance(ast, lisp_Terminal) and ast.token.type == TokenType.ID

    def is_Expr(self, ast):
        return isinstance(ast, lisp_Expr)


    def eval_set_q(self, set_q_ast):
        if not len(set_q_ast.args) > 2:
            raise InterpretException(set_q_ast, "Too few args for setq")
        self.current_scope.update_var(set_q_ast.args[1].token.literal, self.eval(set_q_ast.args[2]))
        return False

    def eval_do_times(self, do_times_ast):
        if not len(do_times_ast.args) > 2:
            raise InterpretException(do_times_ast, "Too few args for dotimes")
        
        if not len(do_times_ast.args[1].args) == 2:
            raise InterpretException(do_times_ast, "exception in index var")
        
        index_var_name = do_times_ast.args[1].args[0].token.literal
        index_var_max_val = self.eval(do_times_ast.args[1].args[1])

        for index in range(index_var_max_val):
            if index == 0:
                self.current_scope.init_var(index_var_name, index)
            else:
                self.current_scope.update_var(index_var_name, index)
            self.eval_args(do_times_ast.args[2:])
        return False


        
    def eval_de_fun(self, defun_ast):
        if not len(defun_ast.args) > 2:
            raise InterpretException(defun_ast, "Too few args for defun")
        if not self.is_ID(defun_ast.args[1]):
            raise InterpretException(defun_ast, "Name of function must be an ID")
        if not self.is_Expr(defun_ast.args[2]):
            raise InterpretException(defun_ast, "Exception in args for defun")
        for param in defun_ast.args[2].args:
            if not isinstance(param, lisp_Terminal) and param.type == TokenType.ID:
                raise InterpretException(defun_ast, "Parameters must be IDs")
        
        func_name = defun_ast.args[1].token.literal
        param_list = list(defun_ast.args[2].args)
        func_ast = defun_ast.args[3]
    

        function_lambda = partial(self.execute_func, param_list, func_ast)
        
        self.current_scope.dec_func(Func(func_name, function_lambda, num_args=len(param_list)))

        return False # TODO false should be NIL


        

    def execute_func(self, parameters, ast, args):
        old_scope = self.current_scope
        self.current_scope = Scope(self.current_scope)

        for index, param in enumerate(parameters): # TODO handle mismatched argument amounts
            self.current_scope.init_var(param.token.literal, args[index])
        
        return_val = self.eval(ast)

        self.current_scope = old_scope

        return return_val



    def eval_if(self, if_ast):
        if len(if_ast.args) != 4:
            raise InterpretException(if_ast, "Too few args for if")
        
        if self.eval(if_ast.args[1]):
            return self.eval(if_ast.args[2])
        else:
            return self.eval(if_ast.args[3])
        

        
    def eval_list(self, list_ast):
        if len(list_ast.args) == 1:
            return False
        else:
            return list(self.eval(arg) for arg in list_ast.args[1:])
        


    # needs more functions
    def init_stl(self):
        stl = [
            Func("+", lambda args: sum(args)),
            Func("-", lambda args: 0 if len(args) == 0 else -args[0] if len(args) == 1 else args[0] - sum(args[1:])),
            Func("*", lambda args: math.prod(args)),
            Func("/", lambda args: division(args), -2),
            Func("write", lambda args: print(args[0])),
            Func("exp", lambda args: math.exp(args[0]), 1),
            Func("sin", lambda args: math.sin(args[0]), 1),
            Func("cos", lambda args: math.cos(args[0]), 1),
            Func("tan", lambda args: math.tan(args[0]), 1), 
            Func("abs", lambda args: math.abs(args[0]), 1), 
            Func("max", lambda args: max(args)), 
            Func("min", lambda args: min(args)),
            Func("=", lambda args: equality(args), -2),
            Func("eql", lambda args: equality_eql(args), -2),
            Func("/=", lambda args: disequality(args), -2),
            Func("<", lambda args: less(args), -2),
            Func("<=", lambda args: less_eq(args), -2),
            Func(">", lambda args: greater(args), -2),
            Func(">=", lambda args: greater_eq(args), -2),
            Func("and", lambda args: l_and(args)),
            Func("or", lambda args: l_or(args)),
            Func("not", lambda args: not args[0], 1),
        ]
        return stl

def less(args):
    less_b = True
    last_arg = args[0]
    for arg in args[1:]:
        less_b = less_b and last_arg < arg
        last_arg = arg
    return less_b

def less_eq(args):
    less_b = True
    last_arg = args[0]
    for arg in args[1:]:
        less_b = less_b and last_arg <= arg
        last_arg = arg
    return less_b

def greater(args):
    greater_b = True
    last_arg = args[0]
    for arg in args[1:]:
        greater_b = greater_b and last_arg > arg
        last_arg = arg
    return greater_b

def greater_eq(args):
    greater_b = True
    last_arg = args[0]
    for arg in args[1:]:
        greater_b = greater_b and last_arg >= arg
        last_arg = arg
    return greater_b



def equality(args):
    equal = True
    arg0 = args[0]
    for arg in args[1:]:
        equal = equal and arg0 == arg
    return equal

def equality_eql(args):
    equal = True
    arg0 = args[0]
    for arg in args[1:]:
        equal = equal and arg0 == arg and arg0 is arg
    return equal

def disequality(args):
    equal = True
    arg0 = args[0]
    for arg in args[1:]:
        equal = equal and arg0 != arg
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

def l_and(args):
    result = True 
    for arg in args:
        if not isinstance(arg, bool):
            raise Exception("All args must be boolean")
        else:
            result = result and arg
    return result

def l_or(args):
    result = False
    for arg in args:
        if not isinstance(arg, bool):
            raise Exception("All args must be boolean")
        else:
            result = result or arg
    return result