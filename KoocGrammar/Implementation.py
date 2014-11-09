#!/usr/bin/env python3

from pyrser.grammar import Grammar
from pyrser import meta
from KoocGrammar.KC_Statement import KC_Statement
import KoocFile
import knodes

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
    name = self.value(name)
    variables = KoocFile.module_variables_nodes(name)
    for variable in variables:
        ast.ref.body.append(variable)
    if hasattr(body, "body") and body.body:
        for item in body.body:
            if hasattr(item, "_ctype"):
                params = ""
                if isinstance(item._ctype, knodes.KFuncType):
                     params = item._ctype.mangle_params()
                mangled_name = KoocFile.mangled_name_of_symbol(name, item._name, item._ctype.mangle(), params)
                item._name = mangled_name
                ast.ref.body.append(item)
    return True
