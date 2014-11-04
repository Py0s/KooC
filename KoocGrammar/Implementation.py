#!/usr/bin/env python3

from pyrser.grammar import Grammar
from pyrser import meta
from KoocGrammar.KC_Statement import KC_Statement
import KoocFile

class   Implementation(Grammar, KC_Statement):
    entry = 'Implementation'
    grammar = """
                implementation = [  "@implementation"
                                    Implementation.Name:module_name
                                    KC_Statement.kc_single_statement:body
                                    #Impl(current_block, module_name, body) ]

                Name = [ [['a'..'z']|['A'..'Z']]+ ]
              """


@meta.hook(Implementation)
def Impl(self, ast, module_name, body):
    if hasattr(body, "body") and body.body:
        module_name = self.value(module_name)
        for item in body.body:
            ast.ref.body.append(item)
    return True
