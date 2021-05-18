from lisp_interpreter import Interpreter
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
        interpreter = Interpreter()
        test1 = "(write 1)"
        lexed_tokens = lexer.lex(test1)
        parsed_ast = parser.parse(lexed_tokens)
        expected_ast = lisp_Expr([lisp_Terminal(Token(TokenType.ID, "test", 1)), 
        lisp_Terminal(Token(TokenType.NUM, 1, 6))])
        message = "positive test 1 failed"
        self.assertEqual(parsed_ast, expected_ast, message)


    def test_2_negative(self):
        lexer = Lexer()
        parser = Parser()
        test2 = "test)"
        message = "negative test 2 failed"

        with self.assertRaises(ParseException, msg=message) as em:
            lexed_tokens = lexer.lex(test2)
            parsed_ast = parser.parse(lexed_tokens)
        self.assertIsInstance(em.exception, ParseException)
        self.assertEqual(em.exception.message, "Missing opening paren")






if __name__ == "__main__":
    unittest.main()
