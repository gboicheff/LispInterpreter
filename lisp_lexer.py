# https://theory.stanford.edu/~amitp/yapps/yapps-doc/node2.html
import re
from lisp_token import TokenType, Token

class LexException(Exception):
    def __init__(self, index, message="Exception occured while lexing"):
        self.index = index
        self.message = message
        super().__init__(self.message)
        
class Lexer:
    def __init__(self):
        pass

    def lex(self, input):
        self.code = input
        self.index = 0
        self.start_index = 0
        self.tokens = []

        while self.index < len(self.code):
            self.lex_token()

        return self.tokens

    def lex_token(self):
        if self.peek("\("):
            self.lex_OPEN_PAREN()
        elif self.peek("\)"):
            self.lex_CLOSE_PAREN()
        elif self.peek("[0-9]"):
            self.lex_NUM()
        elif self.peek("[-+*/!@%^&=.a-zA-Z0-9_]"):
            self.lex_ID()
        elif self.peek("\""):
            self.lex_STR()
        elif self.peek("\s"):
            self.advance()
        else:
            raise LexException(self.index)

    def lex_ID(self):
        self.match("[-+*/!@%^&=.a-zA-Z0-9_]") # match the first
        while self.peek("[-+*/!@%^&=.a-zA-Z0-9_]"):
            self.match("[-+*/!@%^&=.a-zA-Z0-9_]")
        self.tokens.append(self.emit(TokenType.ID))

    def lex_NUM(self):
        self.match("[0-9]")
        while self.peek("[0-9]"):
            self.match("[0-9]")
        self.tokens.append(self.emit(TokenType.NUM))
    
    def lex_STR(self):
        self.match("\"")
        while self.peek("[^\"]"):
            self.match("[^\"]")
        if not self.match("\""):
            raise LexException(self.index, "String missing closing double quote")
        self.tokens.append(self.emit(TokenType.STR))
    
    def lex_OPEN_PAREN(self):
        self.match("\(")
        self.tokens.append(self.emit(TokenType.OPEN_PAREN))
    
    def lex_CLOSE_PAREN(self):
        self.match("\)")
        self.tokens.append(self.emit(TokenType.CLOSE_PAREN))

    def peek(self, *reg_strs):
        for offset,reg_str in enumerate(reg_strs):
            if self.index+offset > len(self.code)-1:
                return False
            if not re.match(reg_str, self.code[self.index+offset]):
                return False
        return True         

    def match(self, *reg_strs):
        for reg_str in reg_strs:
            if not self.peek(reg_str):
                return False
            self.index+=1
        return True

    def advance(self):
        self.index+=1
        self.start_index+=1

    def emit(self, token_type):
        substr = self.code[self.start_index:self.index]
        start_index = self.start_index
        self.start_index = self.index # reset the token start index

        literal = None

        if token_type == TokenType.NUM:
            literal = int(substr)
        elif token_type == TokenType.STR:
            literal = substr[1:-1] # remove double quotes and both sides
        else:
            literal = substr

        return Token(token_type, literal, start_index)
    

    



    