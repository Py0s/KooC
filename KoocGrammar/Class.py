#!/usr/bin/env python3

from pyrser.grammar import Grammar
from pyrser import meta
from cnorm import nodes
from KoocGrammar.KC_Statement import KC_Statement
import Knodes

class   Class(Grammar, KC_Statement):
    entry = 'class'
    grammar = """
    class = [ "@class" Class.Name:classe_name #echo("tuturu~")
               classe_kc_statement:body
               #add_classe(current_block, classe_name, body)    ]

    classe_kc_statement = [ Statement.single_statement:>_ | classe_k_statement:>_ ]
    classe_k_statement = [ classe_kc_expression:>_ ]
    classe_kc_expression = [ classe_expression:>_ ]
    classe_expression = [
                as_member_expression:>_
                [
                ',':op #new_raw(op, op)
                as_member_expression:param
                #new_binary(_, op, param)
                ]*
              ]

    as_member_expression = [ member | assignement_expression ]


    member = [
              "@member"
              KC_Statement.kc_statement:body
             ]

    Name = [ [['a'..'z']|['A'..'Z']]+ ]
              """


@meta.hook(Class)
def add_classe(self, ast, classe_name, body):
    print(body)
    if hasattr(body, "body") and body.body:
        classe = Knodes.Class()
        for item in body.body:
            if (hasattr(item, "_ctype") and hasattr(item._ctype, "_storage")):
                item._ctype._storage = nodes.Storages.STATIC
                classe.declarations.append(item)
        ast.ref.body.append(classe)
    return True
