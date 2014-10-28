#!/usr/bin/env python3

from pyrser.grammar import Grammar
from pyrser import meta
from KoocGrammar.KC_Statement import KC_Statement

class   Implementation(Grammar, KC_Statement):
    entry = 'Implementation'
    grammar = """
                implementation = [ "@implementation" Implementation.Name:name KC_Statement.kc_single_statement:body #Impl(current_block, name, body) ]

                Name = [ [['a'..'z']|['A'..'Z']]+ ]
              """


@meta.hook(Implementation)
def Impl(self, ast, name, body):
    if hasattr(body, "body") and body.body:
        for item in body.body:
            ast.ref.body.append(item)
    return True
