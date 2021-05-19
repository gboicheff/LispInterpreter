from lisp_lexer import Lexer
from lisp_parser import Parser
from lisp_interpreter import Interpreter
import sys
import os
if __name__ == "__main__":

    file_name = sys.argv[1]
    with open(os.path.join("codefiles","{}.lisp".format(file_name)), "r") as file:
        program = file.read()

    lexer = Lexer()
    parser = Parser()
    interpreter = Interpreter()

    lexed_tokens = lexer.lex(program)
    ast = parser.parse(lexed_tokens)
    print(ast)
    return_val = interpreter.interpret(ast)
    print(return_val)

