#!/usr/bin/env python3

from pyrser.grammar import Grammar
from pyrser import meta
from cnorm import nodes
from KoocGrammar.KC_Statement import KC_Statement
import knodes

class   Module(Grammar, KC_Statement):
    entry = 'module'
    grammar = """
                module = [  "@module"
                            Module.Name:module_name
                            module_single_statement:body
                            //KC_Statement.kc_single_statement:body
                            #add_module(current_block, module_name, body) ]

                module_single_statement = [ module_compound_statement:>_ ]

                module_compound_statement = [
                    [
                     '{'
                        __scope__:current_block
                        #new_blockstmt(_, current_block)
                        [
                            kc_line_of_code
                            //kc_declaration
                        ]*
                     '}'
                    ]
                ]

                Name = [ [['a'..'z']|['A'..'Z']]+ ]
              """


@meta.hook(Module)
def add_module(self, ast, module_name, body):
    if hasattr(body, "body") and body.body:
        module = knodes.Module()
        for item in body.body:
            if (hasattr(item, "_ctype") and hasattr(item._ctype, "_storage")):
                item._ctype._storage = nodes.Storages.STATIC
                module.declarations.append(item)
        ast.ref.body.append(module)
    return True
