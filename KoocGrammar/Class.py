#!/usr/bin/env python3

from pyrser.grammar import Grammar
from pyrser import meta
from cnorm import nodes
from KoocGrammar.KC_Statement import KC_Statement
import Knodes

class   Class(Grammar, KC_Statement):
    entry = 'class'
    grammar = """
    class = [  "@class" Class.Name:class_name
               KC_Statement.kc_statement:body
               #add_class(current_block, class_name, body)
               #echo("Hououin Kyouma!")
            ]

    member = [ "@member"
               [
                 ['{'
                  __scope__:current_block
                  #new_member(_, current_block)
                  declaration*
                 '}']
                 |
                 [__scope__:current_block
                  #new_member(_, current_block)
                  declaration*]
               ]

               #print_member_body(current_block)
               #echo("Mad Scientist!")
             ]

    Name = [ [['a'..'z']|['A'..'Z']]+ ]
              """


@meta.hook(Class)
def new_member(self, ast, current_block):
    ast.set(nodes.BlockStmt([]))
    current_block.ref = ast
    parent = self.rule_nodes.parents
    if 'current_block' in parent:
        current_block.ref.types = parent['current_block'].ref.types.new_child()
    return True

@meta.hook(Class)
def print_member_body(self, block):
    ## print("MEMBER BLOCK ---> ", block)
    ## print(self._stream.peek_char)
    return True

@meta.hook(Class)
def add_class(self, ast, class_name, body):
    ## print("CLASS BODY --> ", body)
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
