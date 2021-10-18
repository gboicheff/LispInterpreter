from linterpreter import Lexer
from linterpreter import Parser
from linterpreter import Interpreter
import sys
import os

if __name__ == "__main__":

    file_name = sys.argv[1]
    with open(os.path.join("codefiles",file_name), "r") as file:
        program = file.read()

    lexer = Lexer()
    parser = Parser()
    interpreter = Interpreter()

    lexed_tokens = lexer.lex(program)
    ast = parser.parse(lexed_tokens)

    return_val = interpreter.interpret(ast)
    print(return_val)