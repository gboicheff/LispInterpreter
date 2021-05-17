from lisp_token import TokenType, Token
from lisp_ast import *

class Parser:

    def __init__(self):
        pass

    def parse(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.Ast = None

        return self.parse_list()


    # top level
    def parse_list(self):
        if not self.match(TokenType.OPEN_PAREN):
            raise Exception("Missing opening paren")

        seq = self.parse_seq()

        if not self.match(TokenType.CLOSE_PAREN):
            raise Exception("Missing closing paren")
        
        return lisp_List(seq)

    def parse_seq(self):
        exprs = []
        while self.peek(TokenType.NUM) or self.peek(TokenType.STR) or self.peek(TokenType.ID) or self.peek(TokenType.OPEN_PAREN):
            exprs.append(self.parse_expr())
        return lisp_Seq(exprs)
    
    def parse_expr(self):
        value = None
        if self.peek(TokenType.OPEN_PAREN):
            value = self.parse_list()
        else:
            value = self.parse_terminal()
        return lisp_Expr(value)
            

    def parse_terminal(self):
        if self.peek(TokenType.NUM):
            self.match(TokenType.NUM)
        elif self.peek(TokenType.STR):
            self.match(TokenType.STR)
        elif self.peek(TokenType.ID):
            self.match(TokenType.ID)
        else:
            raise Exception("Invalid terminal at index {}".format(self.index))        
        return lisp_Terminal(self.tokens[self.index-1])


    def peek(self, *token_types):
        for offset, token_type in enumerate(token_types):
            if self.index+offset > len(self.tokens)-1:
                raise Exception("Invalid peek index:{}".format(self.index+offset))
            if not self.tokens[self.index+offset].type == token_type:
                return False
        return True
    
    def match(self, *token_types):
        for token_type in token_types:
            if not self.peek(token_type):
                return False
            self.advance()
        return True

    def advance(self):
        self.index+=1