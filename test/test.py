#!/usr/bin/env python3

from pyrser.grammar import Grammar
from cnorm.parsing.declaration import Declaration
from cnorm import nodes
from cnorm.passes import to_c

class Test(Grammar, Declaration):
    entry = ""
    grammar = """
        Declaration. = [ '@' id:a #module(_, a) eof]
    """

def toto(ast, a):
    ast = module(module_name, b, c)
    return True

code = """
    int main()
    {
        myfunction();
        return 0;
    }
"""

def main():
    toto = Test()
    ast = toto.parse(code)
    print(ast.to_c())

main()