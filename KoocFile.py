
from KoocGrammar import KoocG

includePath = "./"

imported_file_names = []
modules = {}

# { module_name:
#     { symbol_name:
#         [(symbol_type, node),
#             ...]}}

def kooc_a_file(kooc_file_name):
    cparse = KoocG()
    ast = cparse.parse_file(kooc_file_name)
    return ast

def register_file(file_name):
    imported_file_names.append(file_name)
def is_file_imported(fileName):
    return fileName in imported_file_names


# TODO : UnitTests



def register_module(module_name):
    if not module_name in modules: #TODO : générer une erreur sinon ?
        modules[module_name] = {}

def register_var_in_module(module_name, symbol_name, symbol_type, mangled_name, assign_node = None):
    if not symbol_name in modules[module_name]:
        modules[module_name][symbol_name] = {}
    symbol_entry = modules[module_name][symbol_name]
    symbol_entry[symbol_type] = (mangled_name, assign_node)
    print("MODULE !! ", modules)
    #checker si cette surcharge existe deja, dans ce cas -> erreur
    # '-> appeler is_var_in_module
    
def is_var_in_module(module_name, symbol_name, symbol_type):
    if module_name in modules\
        and symbol_name in modules[module_name]\
            and symbol_type in modules[module_name][symbol_name]:
                    return True
    return False

def get_var_from_module(module_name, symbol_name, symbol_type):
    if not is_var_in_module(module_name, symbol_name, symbol_type):
        raise RuntimeError("try to get unknown node")
    return modules[module_name][symbol_name][symbol_type]

def get_mangled_name_from_module(module_name, symbol_name, symbol_type):
    return get_var_from_module()[0]
def get_assign_node_from_module(module_name, symbol_name, symbol_type):
    return get_var_from_module()[1]



# def register_class(className):
#     classes.append(className)
# def register_module(moduleName):
#     modules.append(moduleName)

# def register_class_function(className, mangled_name):
#     classes[className].append(mangled_name)
# def register_module_function(moduleName, mangled_name):
#     modules[moduleName].append(mangled_name)

# def is_module_function(mangled_name):
#     for module in modules:
#         for symbol in module:
#             if symbol == mangled_name:
#                 return True
#     return False
# def is_class_function(mangled_name):
#     for classe in classes:
#         for symbol in classe:
#             if symbol == mangled_name:
#                 return True
#     return False
