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
                                ["@!(" kooc_type:type ")"]? "["
                                    module_id:module
                                    [[ function_id:func list_parameter:params #create_func_symbol(_, module, type, func, params)]
                                    |
                                    variable_id:var #create_var_symbol(_, module, var) ]
                                ']'
                             ]
    kooc_type              = [ Base.id:>_ ]
    module_id              = [ Base.id ]
    function_id            = [ Base.id ]
    list_parameter         = [ #create_params(_) [':' assmt_expr_overide:param #save_param(_, param)]* ]
    variable_id            = [ '.' Base.id ]


    ///////////////////////////
    /// Regles a surcharger ///
    ///////////////////////////
    assmt_expr_overide     = [ "regle overide dans KC_Expression" ]
    """


## class Class(nodes.Func):
##     def __init__(self, call_expr, params):
##         super().__init__(call_expr, params)

##     def to_c(self):
##         print("Tuturu~")
##         res = super().to_c()
##         print(res)
##         return res

@meta.hook(Kooc_call)
def create_params(self, ast):
    ast.params = []
    return True

@meta.hook(Kooc_call)
def save_param(self, ast, param):
    if type(param) is nodes.Func:
        ast.params.append(param)
    else:
        ast.params.append(nodes.Literal(self.value(param)))
    return True

@meta.hook(Kooc_call)
def create_func_symbol(self, ast, module, typo, func, params):
##    ast.set(Class(nodes.Id(self.value(module) + self.value(func)), params.params))
    ast.set(nodes.Func(nodes.Id(self.value(module) + "_" + self.value(typo) + "_" + self.value(func)), params.params))
    return True

@meta.hook(Kooc_call)
def create_var_symbol(self, ast, module, var):
    ast.set(nodes.Id(self.value(module) + self.value(var)))
    return True
