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

class lisp_List:
    def __init__(self, seq):
        self.seq = seq
        # super().__init__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if len(self.seq) != len(other.seq):
                return False
            for index in range(len(self.seq)):
                if self.seq[index] != other.seq[index]:
                    return False
            return True
        else:
            return False

    def __str__(self):
        output_str = "(List "
        for index, s in enumerate(self.seq):
            if index == len(self.seq) - 1:
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
