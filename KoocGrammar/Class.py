#!/usr/bin/env python3

from pyrser.grammar import Grammar
from pyrser import meta
from cnorm import nodes
from KoocGrammar.KC_Statement import KC_Statement
import Knodes

class   Class(Grammar, KC_Statement):
    entry = 'Class'
    grammar = """
                classe = [ "@classe" Class.Name:classe_name
                            KC_Statement.kc_statement:body
                            #add_classe(current_block, classe_name, body) ]

                Name = [ [['a'..'z']|['A'..'Z']]+ ]
              """


@meta.hook(Class)
def add_classe(self, ast, classe_name, body):
    if hasattr(body, "body") and body.body:
        classe = Knodes.Class()
        for item in body.body:
            if (hasattr(item, "_ctype") and hasattr(item._ctype, "_storage")):
                item._ctype._storage = nodes.Storages.STATIC
                classe.declarations.append(item)
        ast.ref.body.append(classe)
    return True
