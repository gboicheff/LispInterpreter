import unittest
from lisp_lexer import *
from unittest import TestCase


class TestBasics(unittest.TestCase):
    def test_1_positive(self):
        lexer = Lexer()
        test1 = "(test 1)"
        test1_expected_output = [Token(TokenType.OPEN_PAREN, "(", 0), Token(TokenType.ID, "test", 1), 
        Token(TokenType.NUM, 1, 6), Token(TokenType.CLOSE_PAREN, ")", 7)]
        message = "positive test 1 failed"
        self.assertEqual(lexer.lex(test1), test1_expected_output, message)

    def test_2_positive(self):
        lexer = Lexer()
        test2 = "(test \"x\")"
        test2_expected_output = [Token(TokenType.OPEN_PAREN, "(", 0), Token(TokenType.ID, "test", 1), 
        Token(TokenType.STR, "x", 6), Token(TokenType.CLOSE_PAREN, ")", 9)]
        message = "positive test 2 failed"
        self.assertEqual(lexer.lex(test2), test2_expected_output, message)

    def test_3_positive(self):
        lexer = Lexer()
        test3 = "(test"
        test3_expected_output = [Token(TokenType.OPEN_PAREN, "(", 0), Token(TokenType.ID, "test", 1)]
        message = "positive test 3 failed"
        self.assertEqual(lexer.lex(test3), test3_expected_output, message)

    def test_1_negative(self):
        lexer = Lexer()
        test1 = "(test \"x)"
        message = "negative test 1 failed"
        with self.assertRaises(LexException, msg=message) as em:
            lexer.lex(test1)
        self.assertIsInstance(em.exception, LexException)
        self.assertEqual(em.exception.message, "String missing closing double quote")




if __name__ == "__main__":
    unittest.main()
