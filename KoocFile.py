
from KoocGrammar import KoocG

includePath = "./"

imported_file_names = []
modules = {}
classes = {}

# { module_name:
#     { symbol_name:
#         [(symbol_type, node),
#             ...]}}

def kooc_a_file(kooc_file_name):
    cparse = KoocG()
    ast = cparse.parse_file(kooc_file_name)
    return ast

class KFImpl():
    def __init__(self):
        pass

    def params_types_equals(first, second):
        # TODO !
        return True

    def symbol_entry_in_module(module_name, symbol_name):
        return modules[module_name][symbol_name]
    def symbol_entry_in_classe(classe_name, symbol_name):
        return classes[classe_name][symbol_name]

    def symbol_overload(symbol_entry, symbol_type, params_types=[]):
        for overload in symbol_entry:
            if overload[0] == symbol_type and params_types_equals(overload[1], params_types):
                return overload
        return None

    def is_var_in_module(module_name, symbol_name, symbol_type, params_types=[]):
        if module_name in modules\
            and symbol_name in modules[module_name]:
                for overload in modules[module_name][symbol_name]:
                    if overload[0] == symbol_type and params_types_equals(overload[1], params_types):
                        return True
        return False
    
    def get_var_from_module(module_name, symbol_name, symbol_type, params_types=[]):
        if not is_var_in_module(module_name, symbol_name, symbol_type, params_types):
            raise RuntimeError("try to get unknown node")
        symbol_entry = modules[module_name][symbol_name]
        return symbol_overload(symbol_entry, symbol_type, params_types)

    def get_var_for_symbol(module_name, symbol_name, symbol_type, params_types=[]):
        var = None
        if is_var_in_module(module_name, symbol_name, symbol_type, params_types):
            if is_var_in_class(module_name, symbol_name, symbol_type, params_types):
                raise RuntimeError("Unbiguous call")#TODO : jolie msg
            else:
                var = get_var_from_module(module_name, symbol_name, symbol_type, params_types)
        elif is_var_in_class(module_name, symbol_name, symbol_type, params_types):
            var = get_var_from_module(module_name, symbol_name, symbol_type, params_types)
        else:
            raise RuntimeError("No symbol")#TODO : jolie msg
        return var

def is_file_imported(fileName):
    return fileName in imported_file_names
def register_file(file_name):
    imported_file_names.append(file_name)


def register_module(module_name):
    if not module_name in modules:
        modules[module_name] = {}
def register_class(class_name):
    if not class_name in classes:
        classes[class_name] = {}
    else:
        raise RuntimeError("Redefinition of class \"" + class_name + "\"")

def register_module_symbol(module_name, symbol_name, symbol_type, mangled_name, params_types=[], assign_node = None):
    # verifier l'existence du module ?
    if not symbol_name in modules[module_name]:
        modules[module_name][symbol_name] = []
    symbol_entry = modules[module_name][symbol_name]
    for symbol_overload in symbol_entry:
        if symbol_overload[1] == mangled_name:
            raise RuntimeError("Redefinition of symbol \"" + symbol_name + "\" in the module \"" + module_name + "\"")
    symbol_entry.append((symbol_type, params_types, mangled_name, assign_node))
    
def register_class_symbol(module_name, symbol_name, symbol_type, mangled_name, params_types=[], assign_node = None):
    # TODO !
    pass

# def register_class_symbols(class_name, symbols)
#    pass


# ! ici module_name signifie aussi bien nom du module que de la classe
def mangled_name_of_symbol(module_name, symbol_name, symbol_type, params_types=[]):
    return KFImpl.get_var_for_symbol(module_name, symbol_name, symbol_type, params_types)[2]
def assign_node_of_symbol(module_name, symbol_name, symbol_type, params_types=[]):
    return KFImpl.get_var_for_symbol(module_name, symbol_name, symbol_type, params_types)[3]


# TODO : ne retourner que la vtable ou toutes les fonctions membres ?
def symbols_of_class(class_name):
    if not class_name in classes:
        raise RuntimeError("No definition of class \"" + class_name + "\"")
    return classes[class_name]


