#!/usr/bin/env python3

from pyrser.grammar import Grammar
from pyrser import meta
from cnorm import nodes
from KoocGrammar.KC_Statement import KC_Statement
from Exceptions.KoocException import KoocException
import KoocFile
import knodes
import copy

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
        module_name = self.value(module_name)
        KoocFile.register_module(module_name)
        module = knodes.Module(module_name)
        for item in body.body:
            if (hasattr(item, "_ctype") and hasattr(item._ctype, "_storage")):
                module.add_item(item)
                params = ""
                if isinstance(item._ctype, knodes.KFuncType):
                    params = item._ctype.mangle_params()
                # TODO : Gerer les ParenType je sais pas comment
                mangled_name = item.mangle()
                if item._ctype._storage == knodes.Storages.STATIC:
                    mangled_name = item._name
                varNode = copy.deepcopy(item)
                varNode._name = varNode.mangle()
                if hasattr(item, "_assign_expr"):
                    delattr(item, "_assign_expr")
                # print("REGISTER: ", module_name, item._name, item._ctype.mangle(), mangled_name, params, varNode)
                KoocFile.register_module_symbol(module_name, item._name, item._ctype.mangle(), mangled_name, params, varNode)
                if item._ctype._storage == knodes.Storages.INLINE:
                    raise KoocException("[Error]: inline key-word in Module " + module_name)# A décommenter? + ", " + str(item.to_c()))
                if item._ctype._storage == knodes.Storages.AUTO:
                    item._ctype._storage = knodes.Storages.EXTERN
                item._name = item.mangle()
        ast.ref.body.append(module)
    return True
