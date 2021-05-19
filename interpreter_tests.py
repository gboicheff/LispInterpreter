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
        test = "(+ 1)"
        lexed_tokens = lexer.lex(test)
        parsed_ast = parser.parse(lexed_tokens)
        actual_output = interpreter.interpret(parsed_ast)
        expected_output = 1
        message = "positive test 1 failed"
        self.assertEqual(actual_output, expected_output, message)

    def test_2_positive(self):
        lexer = Lexer()
        parser = Parser()
        interpreter = Interpreter()
        test = "(+)"
        lexed_tokens = lexer.lex(test)
        parsed_ast = parser.parse(lexed_tokens)
        actual_output = interpreter.interpret(parsed_ast)
        expected_output = 0
        message = "positive test 2 failed"
        self.assertEqual(actual_output, expected_output, message)

    def test_3_positive(self):
        lexer = Lexer()
        parser = Parser()
        interpreter = Interpreter()
        test = "(+ 1 2)"
        lexed_tokens = lexer.lex(test)
        parsed_ast = parser.parse(lexed_tokens)
        actual_output = interpreter.interpret(parsed_ast)
        expected_output = 3
        message = "positive test 3 failed"
        self.assertEqual(actual_output, expected_output, message)

    def test_4_positive(self):
        lexer = Lexer()
        parser = Parser()
        interpreter = Interpreter()
        test = "(- 10 1 2 3 4)"
        lexed_tokens = lexer.lex(test)
        parsed_ast = parser.parse(lexed_tokens)
        actual_output = interpreter.interpret(parsed_ast)
        expected_output = 0
        message = "positive test 4 failed"
        self.assertEqual(actual_output, expected_output, message)
    
    def test_5_positive(self):
        lexer = Lexer()
        parser = Parser()
        interpreter = Interpreter()
        test = "(- 10)"
        lexed_tokens = lexer.lex(test)
        parsed_ast = parser.parse(lexed_tokens)
        actual_output = interpreter.interpret(parsed_ast)
        expected_output = -10
        message = "positive test 5 failed"
        self.assertEqual(actual_output, expected_output, message)

    def test_6_positive(self):
        lexer = Lexer()
        parser = Parser()
        interpreter = Interpreter()
        test = "(* 10)"
        lexed_tokens = lexer.lex(test)
        parsed_ast = parser.parse(lexed_tokens)
        actual_output = interpreter.interpret(parsed_ast)
        expected_output = 10
        message = "positive test 6 failed"
        self.assertEqual(actual_output, expected_output, message)

    def test_7_positive(self):
        lexer = Lexer()
        parser = Parser()
        interpreter = Interpreter()
        test = "(* 10 3)"
        lexed_tokens = lexer.lex(test)
        parsed_ast = parser.parse(lexed_tokens)
        actual_output = interpreter.interpret(parsed_ast)
        expected_output = 30
        message = "positive test 7 failed"
        self.assertEqual(actual_output, expected_output, message)

    def test_8_positive(self):
        lexer = Lexer()
        parser = Parser()
        interpreter = Interpreter()
        test = "(* 10 3 4)"
        lexed_tokens = lexer.lex(test)
        parsed_ast = parser.parse(lexed_tokens)
        actual_output = interpreter.interpret(parsed_ast)
        expected_output = 120
        message = "positive test 8 failed"
        self.assertEqual(actual_output, expected_output, message)

    def test_9_positive(self):
        lexer = Lexer()
        parser = Parser()
        interpreter = Interpreter()
        test = "(*)"
        lexed_tokens = lexer.lex(test)
        parsed_ast = parser.parse(lexed_tokens)
        actual_output = interpreter.interpret(parsed_ast)
        expected_output = 1
        message = "positive test 9 failed"
        self.assertEqual(actual_output, expected_output, message)


    # def test_2_negative(self):
    #     lexer = Lexer()
    #     parser = Parser()
    #     test2 = "test)"
    #     message = "negative test 2 failed"

    #     with self.assertRaises(ParseException, msg=message) as em:
    #         lexed_tokens = lexer.lex(test2)
    #         parsed_ast = parser.parse(lexed_tokens)
    #     self.assertIsInstance(em.exception, ParseException)
    #     self.assertEqual(em.exception.message, "Missing opening paren")






if __name__ == "__main__":
    unittest.main()
