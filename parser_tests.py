from lisp_ast import lisp_Expr
import unittest
from lisp_lexer import *
from lisp_parser import *
from unittest import TestCase
from lisp_token import *

class TestBasics(unittest.TestCase):
    def test_1_positive(self):
        lexer = Lexer()
        parser = Parser()
        test1 = "(test 1)"
        lexed_tokens = lexer.lex(test1)
        parsed_ast = parser.parse(lexed_tokens)
        # print(parsed_ast)
        expected_ast = lisp_List(lisp_Seq([lisp_Expr(lisp_Terminal(Token(TokenType.ID, "test", 1))), 
        lisp_Terminal(lisp_Expr(Token(TokenType.NUM, 1, 6)))]))
        print(expected_ast)
        message = "positive test 1 failed"
        self.assertEqual(parsed_ast, expected_ast, message)





if __name__ == "__main__":
    unittest.main()
