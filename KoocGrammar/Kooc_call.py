#!/usr/bin/env python3
from cnorm.parsing.expression import Expression
from pyrser.grammar import Grammar
from pyrser import meta
from cnorm import nodes
from mangler import simple_mangling as sm
import KoocFile

class   Kooc_call(Grammar):
    entry = 'kooc_call'
    grammar = """
    kooc_call              = [
                                __scope__:type
                                ["@!(" kooc_type:type ")"]? '['
                                    module_id:module
                                    [
                                     [function_id:func list_parameter:params #create_func_symbol(_, module, type, func, params)]
                                     |
                                     ['.' variable_id:var #create_var_symbol(_, module, type, var)]
                                    ]
                                ']'
                             ]
    kooc_type              = [ ['a'..'z'|'A'..'Z'|'*']* ]
    module_id              = [ Base.id ]
    function_id            = [ Base.id ]
    list_parameter         = [ #create_params(_) [':' ["(" kooc_type:type ")"] assmt_expr_overide:param #save_param(_, type, param)]* ]
    variable_id            = [ Base.id ]


    ///////////////////////////
    /// Regles a surcharger ///
    ///////////////////////////
    assmt_expr_overide     = [ "regle overide dans KC_Expression" ]
    """

@meta.hook(Kooc_call)
def heho(self, ast):
    print("NEXT = ", self._stream.peek_char)
    return True

@meta.hook(Kooc_call)
def create_params(self, ast):
    ast.params = []
    ast.types = []
    return True

@meta.hook(Kooc_call)
def save_param(self, ast, typo, param):
    if type(param) is nodes.Func:
        ast.params.append(param)
        ast.types.append(self.value(typo))
    else:
        ast.params.append(nodes.Literal(self.value(param)))
        ast.types.append(self.value(typo))
    return True

@meta.hook(Kooc_call)
def create_func_symbol(self, ast, module_name, typo, func_name, params):
    # print("Module : ", self.value(module_name))
    # print("Type retour : ", self.value(typo))
    # print("Nom fonction :", self.value(func_name))
    # print("Types params : ", params.types)
    # print("Params : ", params.params)
    # print("")
    params_types = ""
    if params.types == []:
        params_types = "v"
    else:
        for item in params.types:
            params_types += sm.type_m(item)
    # print("params_types :", params_types)
    if self.value(typo) == "":
        mangled_name = KoocFile.inferred_mangled_name_of_symbol(self.value(module_name), self.value(func_name), params_types)
    else:
        symbol_type = sm.type_m(self.value(typo))
        # print("symbol_type :", symbol_type)
        mangled_name = KoocFile.mangled_name_of_symbol(self.value(module_name), self.value(func_name), symbol_type, params_types)
    ast.set(nodes.Func(nodes.Id(mangled_name), params.params))
    # ast.set(nodes.Func(nodes.Id(self.value(module_name) + "_" + self.value(typo) + "_" + self.value(func_name)), params.params))
    return True

@meta.hook(Kooc_call)
def create_var_symbol(self, ast, module_name, typo, var_name):
    module_name = self.value(module_name)
    typo = self.value(typo)
    var_name = self.value(var_name)
    if typo == "":
        mangled_name = KoocFile.inferred_mangled_name_of_symbol(module_name, var_name)
    else:
        symbol_type = sm.type_m(typo)
        mangled_name = KoocFile.mangled_name_of_symbol(module_name, var_name, symbol_type)
    ast.set(nodes.Id(mangled_name))
    return True
