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

    def test_equality_eql(self):
        test = "(eql 1)"
        actual_output = run_test(test)
        expected_output = True
        self.assertEqual(actual_output, expected_output)

        test = "(eql 1 2)"
        actual_output = run_test(test)
        expected_output = False
        self.assertEqual(actual_output, expected_output)

        test = "(eql 1 1 1 1 1)"
        actual_output = run_test(test)
        expected_output = True
        self.assertEqual(actual_output, expected_output)

        test = "(eql 1 1.0)"
        actual_output = run_test(test)
        expected_output = False
        self.assertEqual(actual_output, expected_output)

    def test_disequality(self):
        test = "(/= 1)"
        actual_output = run_test(test)
        expected_output = True
        self.assertEqual(actual_output, expected_output)

        test = "(/= 1 2)"
        actual_output = run_test(test)
        expected_output = True
        self.assertEqual(actual_output, expected_output)

        test = "(/= 1 1 1 1 1)"
        actual_output = run_test(test)
        expected_output = False
        self.assertEqual(actual_output, expected_output)

    def test_less(self):
        test = "(< 1)"
        actual_output = run_test(test)
        expected_output = True
        self.assertEqual(actual_output, expected_output)

        test = "(< 1 7)"
        actual_output = run_test(test)
        expected_output = True
        self.assertEqual(actual_output, expected_output)

        test = "(< 1 7 2)"
        actual_output = run_test(test)
        expected_output = False
        self.assertEqual(actual_output, expected_output)

    def test_greater(self):
        test = "(> 1)"
        actual_output = run_test(test)
        expected_output = True
        self.assertEqual(actual_output, expected_output)

        test = "(> 1 7)"
        actual_output = run_test(test)
        expected_output = False
        self.assertEqual(actual_output, expected_output)

        test = "(> 7 3 2)"
        actual_output = run_test(test)
        expected_output = True
        self.assertEqual(actual_output, expected_output)
    
    def test_max(self):
        test = "(max 1)"
        actual_output = run_test(test)
        expected_output = 1
        self.assertEqual(actual_output, expected_output)

        test = "(max 1 7 2)"
        actual_output = run_test(test)
        expected_output = 7
        self.assertEqual(actual_output, expected_output)

    def test_min(self):
        test = "(min 1)"
        actual_output = run_test(test)
        expected_output = 1
        self.assertEqual(actual_output, expected_output)

        test = "(min 1 7 2)"
        actual_output = run_test(test)
        expected_output = 1
        self.assertEqual(actual_output, expected_output)

    
    def test_while(self):
        test = "(let ((x 1)) (while (< x 5) (setq x (+ x 1))) x)"
        actual_output = run_test(test)
        expected_output = 5
        self.assertEqual(actual_output, expected_output)

    def test_defun(self):
        test = "(let ((x 5)) (defun test (z) (+ z 5)) (setq x (test x)) x)"
        actual_output = run_test(test)
        expected_output = 10
        self.assertEqual(actual_output, expected_output)

    def test_if(self):
        test = "(if t 0 1)"
        actual_output = run_test(test)
        expected_output = 0
        self.assertEqual(actual_output, expected_output)

        test = "(if NIL 0 1)"
        actual_output = run_test(test)
        expected_output = 1
        self.assertEqual(actual_output, expected_output)

    def test_and(self):
        test = "(and)"
        actual_output = run_test(test)
        expected_output = True
        self.assertEqual(actual_output, expected_output)

        test = "(and t NIL)"
        actual_output = run_test(test)
        expected_output = False
        self.assertEqual(actual_output, expected_output)

        test = "(or t t)"
        actual_output = run_test(test)
        expected_output = True
        self.assertEqual(actual_output, expected_output)

    def test_or(self):
        test = "(or)"
        actual_output = run_test(test)
        expected_output = False
        self.assertEqual(actual_output, expected_output)

        test = "(or t NIL)"
        actual_output = run_test(test)
        expected_output = True
        self.assertEqual(actual_output, expected_output)

        test = "(or NIL NIL)"
        actual_output = run_test(test)
        expected_output = False
        self.assertEqual(actual_output, expected_output)

    def test_not(self):
        test = "(not t)"
        actual_output = run_test(test)
        expected_output = False
        self.assertEqual(actual_output, expected_output)

        test = "(not NIL)"
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
