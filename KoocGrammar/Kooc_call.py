#!/usr/bin/env python3
from cnorm.parsing.expression import Expression
from Exceptions.KoocException import KoocException
from pyrser.grammar import Grammar
from pyrser import meta
from cnorm import nodes
from mangler import simple_mangling as sm
import KoocFile
import sys

class   Kooc_call(Grammar):
    entry = 'kooc_call'
    grammar = """
    kooc_call              = [
                                __scope__:type
                                ["@!(" kooc_type:type ")"]? '['
                                    module_id:module
                                    [
                                     [function_id:func list_parameter:params #create_func_symbol(_, module, type, func, params, current_block)]
                                     |
                                     ['.' variable_id:var #create_var_symbol(_, module, type, var, current_block)]
                                    ]
                                ']'
                             ]
    kooc_type              = [ ['a'..'z'|'A'..'Z'|'*'|' ']* ]
    module_id              = [ Base.id ]
    function_id            = [ Base.id ]
    list_parameter         = [ #create_params(_)
                               [':'
                               __scope__:param_type
                               ['(' kooc_type:param_type ')']?
                               assmt_expr_overide:param #save_param(_, param_type, param)]*
                             ]
    variable_id            = [ Base.id ]


    ///////////////////////////
    /// Regles a surcharger ///
    ///////////////////////////
    assmt_expr_overide     = [ "regle overide dans KC_Expression" ]
    """

@meta.hook(Kooc_call)
def create_params(self, ast):
    # print("\nCREATE PARAM")
    ast.params = []
    ast.types = []
    return True

@meta.hook(Kooc_call)
def save_param(self, ast, typo, param):
    # print("SAVE_PARAM")
    typo = self.value(typo)

    if type(param) is nodes.Func:
        ast.params.append(param)
        ast.types.append(typo)
    else:
        if typo == "":
            for item in ast.types:
                if item != "UNDEFINED":
                    raise KoocException("Fuck you, soit tu types tout, soit tu types pas du tout! Aller Salut! Des bisous!")
            ast.types.append("UNDEFINED")
        else:
            for item in ast.types:
                if item == "UNDEFINED":
                    raise KoocException("Fuck you, soit tu types tout, soit tu types pas du tout! Aller Salut! Des bisous!")
            ast.types.append(typo)
        # print("TYPES : ", ast.types)
        ast.params.append(nodes.Literal(param.value))
    return True

@meta.hook(Kooc_call)
def create_func_symbol(self, ast, module_name, typo, func_name, params, block):
    # print("I'm a fucking function")
    # print("Module : ", self.value(module_name))
    # print("Type retour : ", self.value(typo))
    # print("Nom fonction :", self.value(func_name))
    # print("Types params : ", params.types)
    # print("Params : ", params.params)
    # print("")
    module_name = self.value(module_name)
    typo = self.value(typo)
    func_name = self.value(func_name)

    moncul = 0

    params_types = ""
    if params.types == []:
        params_types = "v"
#        params_types = None
    else:
        for item in params.types:
            if item == "UNDEFINED":
                if moncul == 0:
                    params_types = None
                    moncul = 1
                elif params_types != None:
                    print("va te faire farçir l'oignon")
                # params_types = item
                # print("INFERENCE DES PARAMETRES?")
            else:
                if params_types == None:
                    print("va te faire cuire un oeuf")
                param_type_node = KoocFile.kooc_a_string(item + " a;")
                params_types += param_type_node.body[0]._ctype.mangle()
    # print("params_types :", params_types)
    if typo != "":
        symbol_type_node = KoocFile.kooc_a_string(typo + " a;")
        typo = symbol_type_node.body[0]._ctype.mangle()
        # print("TYPE : ", symbol_type)
    # print("TRY TO GET: ", module_name, func_name, symbol_type, params_types)
    mangled_name = KoocFile.mangled_name_of_symbol(module_name, func_name, params_types, typo)
    ast.set(nodes.Func(nodes.Id(mangled_name), params.params))
    # ast.set(nodes.Func(nodes.Id(module_name + "_" + typo + "_" + func_name), params.params))
    return True

@meta.hook(Kooc_call)
def create_var_symbol(self, ast, module_name, typo, var_name, block):
    # print("I'm a fucking variable")
    module_name = self.value(module_name)
    typo = self.value(typo)
    var_name = self.value(var_name)
    if typo != "":
        typo = sm.type_m(typo)
    mangled_name = KoocFile.mangled_name_of_symbol(module_name, var_name, "", typo)
    ast.set(nodes.Id(mangled_name))
    return True
