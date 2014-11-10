
from KoocGrammar import KoocG
from KoocFileImpl import KFImpl
import collections

includePath = "./"
imported_file_names = []

def kooc_a_file(kooc_file_name):
    cparse = KoocG()
    ast = cparse.parse_file(kooc_file_name)
    return ast

def kooc_a_string(content):
    cparse = KoocG()
    ast = cparse.parse(content)
    return ast

def is_file_imported(fileName):
    return fileName in imported_file_names
def register_file(file_name):
    imported_file_names.append(file_name)


nested_dict = lambda: collections.defaultdict(nested_dict)
modules = nested_dict()

kfimpl = KFImpl(imported_file_names, modules)

def register_module(module_name):
    pass
    # if not module_name in modules:
    #     modules[module_name] = {}

def register_module_symbol(module_name, symbol_name, params_types, symbol_type, mangled_name, assign_node = None):
    # print("REGISTER: ", module_name, symbol_name, params_types, symbol_type, mangled_name)
    vartype = kfimpl.get_vartype(params_types)
    content = (mangled_name, assign_node)
    kfimpl.set_overload_content(module_name, vartype, symbol_name, params_types, symbol_type, content)


# params_types MUST be set to "" for variables
def mangled_name_of_symbol(module_name, symbol_name, params_types=None, symbol_type=""):
    # print("TRY TO GET: ", module_name, symbol_name, params_types, symbol_type)
    if params_types == None:
        vartype = "function"
    else:
        vartype = kfimpl.get_vartype(params_types)

    symbol_content = kfimpl.get_symbol_content(module_name, vartype, symbol_name)

    if not params_types:
        kfimpl.check_ambiguous(symbol_content, module_name, symbol_name, vartype)
        params_content = next(iter(symbol_content.values()))
    else:
        params_content = kfimpl.get_params_content(module_name, vartype, symbol_name, params_types)

    if not symbol_type or symbol_type == "":
        kfimpl.check_ambiguous(params_content, module_name, symbol_name, vartype)
        overload_content = next(iter(params_content.values()))
    else:
        overload_content = kfimpl.get_overload_content(module_name, vartype, symbol_name, params_content, symbol_type)

    print("OK : ", overload_content[0])
    return overload_content[0]

# def inferred_mangled_name_of_symbol(module_name, symbol_name, params_types=""):
#     vartype = kfimpl.get_vartype(params_types)
#     params_content = kfimpl.get_params_content(module_name, vartype, symbol_name, params_types)
#     kfimpl.check_ambiguous(params_content, module_name, symbol_name, vartype)
#     # if len(params_content) > 1:
#     #     raise RuntimeError("Ambiguous call of " + vartype + " \"" + symbol_name + "\" from the module \"" + module_name + "\"")
#     return next(iter(params_content.values()))[0]

# def mangled_name_of_symbol(module_name, symbol_name, symbol_type, params_types=""):
#     vartype = kfimpl.get_vartype(params_types)
#     return kfimpl.get_overload_content(module_name, vartype, symbol_name, params_types, symbol_type)[0]

# def assign_node_of_symbol(module_name, symbol_name, symbol_type, params_types=""):
#     vartype = kfimpl.get_vartype(params_types)
#     return kfimpl.get_overload_content(module_name, vartype, symbol_name, params_types, symbol_type)[1]

def module_variables_nodes(module_name):
    variables_nodes = []
    try:
        vartype_content = kfimpl.get_vartype_content(module_name, "variable")
    except RuntimeError:
        return variables_nodes
    for symbol_content in iter(vartype_content.values()):
        for params_content in iter(symbol_content.values()):
            for overload_content in iter(params_content.values()):
                variables_nodes.append(overload_content[1])
    return variables_nodes

def debugCleanAll():
    imported_file_names.clear()
    modules.clear()
    kfimpl = KFImpl(imported_file_names, modules)
