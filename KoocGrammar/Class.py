#!/usr/bin/env python3

from pyrser.grammar import Grammar
from pyrser import meta
from cnorm import nodes
from KoocGrammar.KC_Statement import KC_Statement
import knodes
from cnorm.parsing.expression import Idset

class   Class(Grammar, KC_Statement):
    entry = 'class'
    grammar = """
    class = [ "@class"
              Class.Name:class_name #add_class_to_type(class_name)
              class_single_statement:body
              #add_class(current_block, class_name, body)
            ]

    class_single_statement = [
        [ class_compound_statement ]:>_
      ]

    class_compound_statement = [
        [
        '{'
            __scope__:current_block
            #new_blockstmt(_, current_block)
            [
                line_of_code #is_member(class_name, current_block)
                | member:body #add_member(current_block, body)
            ]*
        '}'
        ]
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
                  declaration]
               ]
             ]

    Name = [ [['a'..'z']|['A'..'Z']]+ ]
              """

@meta.hook(Class)
def add_class_to_type(self, class_type):
    Idset[self.value(class_type)] = "type"
    return True

@meta.hook(Class)
def add_class(self, ast, class_name, body):
    name = self.value(class_name)
    if hasattr(body, "body") and body.body:
        class_var = knodes.Class(name)
        class_var.fields = body.body
        class_var.to_c()
        decl_struct = nodes.Decl(name)
        decl_struct._ctype = class_var
        ast.ref.body.append(decl_struct)
        ##ast.ref.body.append(myModule)
    return True

@meta.hook(Class)
def add_member(self, block, body):
    if hasattr(block, "ref") and hasattr(block.ref, "body") and hasattr(body, "body"):
        for elem in body.body:
            block.ref.body.append(knodes.Member(elem))
    return True

@meta.hook(Class)
def new_member(self, ast, current_block):
    ast.set(nodes.BlockStmt([]))
    current_block.ref = ast
    parent = self.rule_nodes.parents
    if 'current_block' in parent:
        current_block.ref.types = parent['current_block'].ref.types.new_child()
    return True

@meta.hook(Class)
def is_member(self, class_name, current_block):
  name = self.value(class_name)
  if current_block.ref.body == []:
    return False
  decl = current_block.ref.body[-1]
  if type(decl._ctype) == nodes.FuncType                  \
  and decl._ctype._params != []                           \
  and type(decl._ctype._params[0]._ctype) == nodes.PrimaryType   \
  and decl._ctype._params[0]._ctype._identifier == name:
    current_block.ref.body[-1] = knodes.Member(current_block.ref.body[-1])
  return True

