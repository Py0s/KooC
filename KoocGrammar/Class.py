#!/usr/bin/env python3

from pyrser.grammar import Grammar
from pyrser import meta
from cnorm import nodes
from cnorm.parsing.declaration import Declaration
from KoocGrammar.KC_Statement import KC_Statement
from cnorm.parsing.expression import Idset
from cnorm.nodes import *
from mangler.simple_mangling import VARS
import knodes
import KoocFile

gr = Declaration()

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
                line_of_code #is_member(class_name, current_block) // For implicit member function
                | member:body #add_member(current_block, body)     // For explicit member function
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
  class_type = self.value(class_type)
  Idset[class_type] = "type"
  # VARS[class_type] = class_type AJOUT DANS LE VARS DE SIMPLE_MANGLING D UN NOUVEAU TYPE
  return True

def create_delete_function(ast, class_name):
    free_node = knodes.KExprStmt(knodes.KFunc(Id("free"), params=[Id("ptr")]))

    # TODO : clean_node

    delete_node_body = []
    delete_node_body.append(free_node)

    params = [knodes.KDecl("ptr", knodes.KPrimaryType(class_name))]
    params[0]._ctype._decltype = knodes.KPointerType()
    #print(params)
    delete_node = knodes.KDecl("delete", knodes.KFuncType('void', params=params))
    delete_node.body = knodes.KBlockStmt(delete_node_body)
    # print(delete_node)
    # print("\n")
    # print(delete_node.to_c())
    # print("\n")
    # print(gr.parse("void delete(void *ptr) { free(ptr); }").body[0].body)
    ast.ref.body.append(delete_node)

def create_new_function(ast, class_name):
  print(gr.parse("void *new() { /*void *ptr = */malloc(sizeof(float)); }").body[0])

  malloc_node_params = [Sizeof(Raw("sizeof"), params=[PrimaryType(class_name)])]
  malloc_node = knodes.KExprStmt(knodes.KFunc(Id("malloc"), params=malloc_node_params))

  # TODO : init_node

  new_node_body = []
  new_node_body.append(malloc_node)

  new_node = knodes.KDecl("new", knodes.KFuncType('void', params=[]))
  new_node._ctype._decltype = knodes.KPointerType()

  new_node.body = knodes.KBlockStmt(new_node_body)
  # print("\n")
  # print(new_node)
  # print(new_node.to_c())
  ast.ref.body.append(new_node)

@meta.hook(Class)
def add_class(self, ast, class_name, body):
    class_name = self.value(class_name)

    if hasattr(body, "body") and body.body:
        # Enregistrement de la classe dans KoocFile sous Classe/Module?
        # KoocFile.register_class(class_name)
        # KoocFile.register_module(class_name)

        class_var = knodes.Class(class_name)
        class_var.fields = body.body

        class_var.to_c()

        decl_struct = nodes.Decl(class_name)
        decl_struct._ctype = class_var
        ast.ref.body.append(decl_struct)
        ##ast.ref.body.append(myModule)

        create_delete_function(ast, class_name)
        create_new_function(ast, class_name)

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
    # if "name" == init
    # creer fonction new
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
    # print(decl._ctype._params[0]._ctype)
    current_block.ref.body[-1] = knodes.Member(current_block.ref.body[-1])
  else:
    # print("Declaration non member: ",  current_block.ref.body[-1])
    non_member = current_block.ref.body.pop()
    # print(non_member)
  # if "name" == init
  # creer fonction new
  return True
