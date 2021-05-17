# class lisp_Ast:
#     def __init__(self):
#         pass


class lisp_Expr:
    def __init__(self, value):
        self.value = value
        # super().__init__()
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value
        else:
            return False

    def __str__(self):
        return "(Expr " + str(self.value) + ")"

class lisp_Seq:
    def __init__(self, exprs):
        self.exprs = exprs
        # super().__init__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.exprs == other.exprs
        else:
            return False

    def __str__(self):
        string = "(Seq "
        for index, expr in enumerate(self.exprs):
            if index == len(self.exprs) - 1:
                string += str(expr)
            else:
                string += str(expr) + " "
        return string + ")"

class lisp_List:
    def __init__(self, seq):
        self.seq = seq
        # super().__init__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.seq == other.seq
        else:
            return False

    def __str__(self):
        return "(List " + str(self.seq) + ")"

class lisp_Terminal:
    def __init__(self, token):
        self.token = token

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.token == other.token
        else:
            return False
    def __str__(self):
        return "(Terminal " + str(self.token.type) + ")"
