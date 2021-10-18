from linterpreter import Lexer
from linterpreter import Parser
from linterpreter import Interpreter

if __name__ == "__main__":
    lexer = Lexer()
    parser = Parser()
    interpreter = Interpreter()
    interpreter.setup()

    current_input = 0

    print("Lisp REPL (enter \"(exit)\" to exit)")
    print("=========================================================")
    
    while True:
        current_input = input()
        if current_input == "(exit)":
            break
        lexed_tokens = lexer.lex(current_input)
        try:
            ast = parser.parse(lexed_tokens)
            result = interpreter.eval(ast)
            if result is not None:
                print(result)
            else:
                print()
        except Exception as e:
            print(e)

