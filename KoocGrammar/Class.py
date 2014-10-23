#!/usr/bin/env python3

from pyrser.grammar import Grammar
from pyrser import meta
from cnorm import nodes
from KoocGrammar.KC_Statement import KC_Statement
import Knodes

class   Class(Grammar, KC_Statement):
    entry = 'class'
    grammar = """
    class = [ "@class" Class.Name:class_name
               classe_kc_statement:body
               #add_class(current_block, class_name, body)    ]

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
              [ "@member"
                KC_Statement.kc_statement:body
                ]
              |
              [ "@member" "{"
                [ classe_kc_statement:>_ ]*
                "}" ]
             ]

    Name = [ [['a'..'z']|['A'..'Z']]+ ]
              """


@meta.hook(Class)
def add_class(self, ast, class_name, body):
    if hasattr(body, "body") and body.body:
        struct = nodes.ComposedType("Hououin") ## TODO : Nom de la classe manglé
        struct._specifier = nodes.Specifiers.STRUCT
        struct._storage = nodes.Storages.TYPEDEF
        struct.fields = []
        for item in body.body:
            struct.fields.append(item)
        Declstruct = nodes.Decl(self.value(class_name))
        Declstruct._ctype = struct
        ast.ref.body.append(Declstruct)
    return True
