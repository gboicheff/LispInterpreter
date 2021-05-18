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
        expected_ast = lisp_Expr([lisp_Terminal(Token(TokenType.ID, "test", 1)), 
        lisp_Terminal(Token(TokenType.NUM, 1, 6))])
        message = "positive test 1 failed"
        self.assertEqual(parsed_ast, expected_ast, message)

    def test_2_positive(self):
        lexer = Lexer()
        parser = Parser()
        test2 = "(test \"x\")"
        lexed_tokens = lexer.lex(test2)
        parsed_ast = parser.parse(lexed_tokens)
        expected_ast = lisp_Expr([lisp_Terminal(Token(TokenType.ID, "test", 1)),
        lisp_Terminal(Token(TokenType.STR, "x", 6))])
        message = "positive test 2 failed"
        self.assertEqual(parsed_ast, expected_ast, message)

    def test_3_positive(self):
        lexer = Lexer()
        parser = Parser()
        test3 = "(x y z)"
        lexed_tokens = lexer.lex(test3)
        parsed_ast = parser.parse(lexed_tokens)
        expected_ast = lisp_Expr([
        lisp_Terminal(Token(TokenType.ID, "x", 1)),
        lisp_Terminal(Token(TokenType.ID, "y", 3)),
        lisp_Terminal(Token(TokenType.ID, "z", 5)),
        ])
        message = "positive test 3 failed"
        self.assertEqual(parsed_ast, expected_ast, message)

    def test_4_positive(self):
        lexer = Lexer()
        parser = Parser()
        test4 = "(x (y z))"
        lexed_tokens = lexer.lex(test4)
        parsed_ast = parser.parse(lexed_tokens)
        expected_ast = lisp_Expr([
        lisp_Terminal(Token(TokenType.ID, "x", 1)),
        lisp_Expr([
        lisp_Terminal(Token(TokenType.ID, "y", 4)), 
        lisp_Terminal(Token(TokenType.ID, "z", 6))])
        ])
        message = "positive test 4 failed"
        self.assertEqual(parsed_ast, expected_ast, message)

    def test_5_positive(self):
        lexer = Lexer()
        parser = Parser()
        test5 = "(x)"
        lexed_tokens = lexer.lex(test5)
        parsed_ast = parser.parse(lexed_tokens)
        expected_ast = lisp_Expr([
        lisp_Terminal(Token(TokenType.ID, "x", 1)),
        ])
        message = "positive test 5 failed"
        self.assertEqual(parsed_ast, expected_ast, message)

    def test_6_positive(self):
        lexer = Lexer()
        parser = Parser()
        test6 = "()"
        lexed_tokens = lexer.lex(test6)
        parsed_ast = parser.parse(lexed_tokens)
        expected_ast = lisp_Expr([])
        message = "positive test 6 failed"
        self.assertEqual(parsed_ast, expected_ast, message)

    def test_1_negative(self):
        lexer = Lexer()
        parser = Parser()
        test1 = "(test"
        message = "negative test 1 failed"
        with self.assertRaises(ParseException, msg=message) as em:
            lexed_tokens = lexer.lex(test1)
            parsed_ast = parser.parse(lexed_tokens)
        self.assertIsInstance(em.exception, ParseException)
        self.assertEqual(em.exception.message, "Missing closing paren")

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
