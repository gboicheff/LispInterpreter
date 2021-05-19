class lisp_Expr:
    def __init__(self, args):
        self.args = args

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if len(self.args) != len(other.args):
                return False
            for index in range(len(self.args)):
                if self.args[index] != other.args[index]:
                    return False
            return True
        else:
            return False

    def __str__(self):
        output_str = "(Expr "
        for index, s in enumerate(self.args):
            if index == len(self.args) - 1:
                output_str += str(s)
            else:
                output_str += str(s) + " "
        return output_str + ")"

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
