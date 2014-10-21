#!/usr/bin/env python3

from pyrser.grammar import Grammar
from pyrser import meta
from cnorm import nodes
from KoocGrammar.KC_Statement import KC_Statement
import Knodes

class   Module(Grammar, KC_Statement):
    entry = 'Module'
    grammar = """
                module = [ "@module" Module.Name:module_name KC_Statement.kc_statement:body #Mod(current_block, module_name, body) ]

                Name = [ [['a'..'z']|['A'..'Z']]+ ]
              """


@meta.hook(Module)
def Mod(self, ast, module_name, body):
    if hasattr(body, "body") and body.body:
        module = Knodes.Module()
        for item in body.body:
            if (hasattr(item, "_ctype") and hasattr(item._ctype, "_storage")):
                item._ctype._storage = nodes.Storages.STATIC
                module.declarations.append(item)
        ast.ref.body.append(module)
    return True
