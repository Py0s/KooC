#!/usr/bin/env python3

from pyrser.grammar import Grammar
from pyrser import meta
from KoocGrammar.KC_Statement import KC_Statement
import KoocFile

class   Implementation(Grammar, KC_Statement):
    entry = 'Implementation'
    grammar = """
                implementation = [  "@implementation"
                                    Implementation.Name:name
                                    KC_Statement.kc_single_statement:body
                                    #Impl(current_block, name, body) ]

                Name = [ [['a'..'z']|['A'..'Z']]+ ]
              """


@meta.hook(Implementation)
def Impl(self, ast, name, body):
    if hasattr(body, "body") and body.body:
        name = self.value(name)
        for item in body.body:
            # mangledname = KoocFile.mangled_name_of_symbol(name, item._name, item._ctype.mangle())
            # print(mangledname)
            ast.ref.body.append(item)
    return True
