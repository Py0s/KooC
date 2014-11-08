#!/usr/bin/env python3
from cnorm.parsing.expression import Expression
from pyrser.grammar import Grammar
from pyrser import meta
from cnorm import nodes

class   Kooc_call(Grammar):
    entry = 'kooc_call'
    grammar = """
    kooc_call              = [
                                __scope__:type
                                ["@!(" kooc_type:type ")"]? '[' #echo("ET OUAIS!")
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

# @meta.hook(Kooc_call)
# def test_ouais(self, ast):
#     print(self._stream.peek_char)
#     print("OUAIS?")
#     return True

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
def create_func_symbol(self, ast, module, typo, func, params):
    # print("Module : ", self.value(module))
    # print("Type retour : ", self.value(typo))
    # print("Nom fonction :", self.value(func))
    # print("Types params : ", params.types)
    # print("Params : ", params.params)
    # print("")
    ast.set(nodes.Func(nodes.Id(self.value(module) + "_" + self.value(typo) + "_" + self.value(func)), params.params))
    return True

@meta.hook(Kooc_call)
def create_var_symbol(self, ast, module, typo, var):
    # print("Type variable :", self.value(typo))
    # print("")
    ast.set(nodes.Id(self.value(module) + "_" + self.value(typo) + "_" + self.value(var)))
    return True
