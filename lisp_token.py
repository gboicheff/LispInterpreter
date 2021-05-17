import enum

class TokenType(enum.Enum):
    STR = 1
    ID = 2
    NUM = 3
    OPEN_PAREN = 4
    CLOSE_PAREN = 5

class Token:
    def __init__(self, type, literal, index):
        self.type = type
        self.literal = literal
        self.index = index

    def __str__(self):
        return "type:[{}]  literal:[{}]  index:[{}]".format(
            self.type, self.literal, self.index)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.type == other.type and self.literal == other.literal and self.index == other.index
        else:
            return False