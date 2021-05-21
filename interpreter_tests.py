from lisp_interpreter import Interpreter
from lisp_ast import lisp_Expr
import unittest
from lisp_lexer import *
from lisp_parser import *
from unittest import TestCase
from lisp_token import *

class TestBasics(unittest.TestCase):
    def test_addition(self):
        test = "(+)"
        actual_output = run_test(test)
        expected_output = 0
        self.assertEqual(actual_output, expected_output)

        test = "(+ 1)"
        actual_output = run_test(test)
        expected_output = 1
        self.assertEqual(actual_output, expected_output)

        test = "(+ 1 2)"
        actual_output = run_test(test)
        expected_output = 3
        self.assertEqual(actual_output, expected_output)

        test = "(+ 1 2 3 4)"
        actual_output = run_test(test)
        expected_output = 10
        self.assertEqual(actual_output, expected_output)


    def test_subtraction(self):
        test = "(-)"
        actual_output = run_test(test)
        expected_output = 0
        self.assertEqual(actual_output, expected_output)

        test = "(- 1)"
        actual_output = run_test(test)
        expected_output = -1
        self.assertEqual(actual_output, expected_output)

        test = "(- 10 1 2 3 4)"
        actual_output = run_test(test)
        expected_output = 0
        self.assertEqual(actual_output, expected_output)
    

    def test_multiplication(self):
        test = "(*)"
        actual_output = run_test(test)
        expected_output = 1
        self.assertEqual(actual_output, expected_output)

        test = "(* 1)"
        actual_output = run_test(test)
        expected_output = 1
        self.assertEqual(actual_output, expected_output)

        test = "(* 1 2)"
        actual_output = run_test(test)
        expected_output = 2
        self.assertEqual(actual_output, expected_output)

        test = "(* 1 2 3)"
        actual_output = run_test(test)
        expected_output = 6
        self.assertEqual(actual_output, expected_output)

    def test_division(self):
        test = "(/ 1)"
        actual_output = run_test(test)
        expected_output = 1
        self.assertEqual(actual_output, expected_output)

        test = "(/ 2 8)"
        actual_output = run_test(test)
        expected_output = 0
        self.assertEqual(actual_output, expected_output)

        test = "(/ 8 2)"
        actual_output = run_test(test)
        expected_output = 4
        self.assertEqual(actual_output, expected_output)

        test = "(/ 25 3 2)"
        actual_output = run_test(test)
        expected_output = 4
        self.assertEqual(actual_output, expected_output)

        test = "(/ 25 3.0 2)"
        actual_output = run_test(test)
        expected_output = 25/3.0/2
        self.assertEqual(actual_output, expected_output)

    def test_equality(self):
        test = "(= 1)"
        actual_output = run_test(test)
        expected_output = True
        self.assertEqual(actual_output, expected_output)

        test = "(= 1 2)"
        actual_output = run_test(test)
        expected_output = False
        self.assertEqual(actual_output, expected_output)

        test = "(= 1 1 1 1 1)"
        actual_output = run_test(test)
        expected_output = True
        self.assertEqual(actual_output, expected_output)







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


def run_test(input):
    lexer = Lexer()
    parser = Parser()
    interpreter = Interpreter()
    lexed_tokens = lexer.lex(input)
    parsed_ast = parser.parse(lexed_tokens)
    output = interpreter.interpret(parsed_ast)
    return output




if __name__ == "__main__":
    unittest.main()
