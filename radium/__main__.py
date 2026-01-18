from .lib.lexer import Lexer
from .lib.parser import Parser
from .lib.compiler import Compiler
from .lib.vm import VM


import sys
import os
from colorama import Fore
args = sys.argv

args = "".join(args[1:])

def validate_file():
    if len(args) < 1:
        print(Fore.RED + "No path was entered!" + Fore.RESET)
        sys.exit(1)

    if not os.path.exists(args) or not os.path.isfile(args):
        print(Fore.RED + f"{args} is not a file or does not exist!" + Fore.RESET)
        sys.exit(1)

    if not args.endswith(".rad"):
        print(Fore.YELLOW + f"{args} is not a Radium Script file by Type, auto checks are disabled!" + Fore.RESET)

def parse_file():
    validate_file()

    with open(args, "r") as f:
        return f.read()


def call_main(source: str):
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    compiler = Compiler()
    bytecode, top_level_functions = compiler.compile(ast)
    VM(bytecode, compiler.classes, top_level_functions).run()


def complete_call():
    call_main(parse_file())


if __name__ == "__main__":
    complete_call()
