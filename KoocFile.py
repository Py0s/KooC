
from KoocGrammar import KoocG
from KoocFileImpl import KFImpl
import collections

includePath = "./"
imported_file_names = []

def kooc_a_file(kooc_file_name):
    cparse = KoocG()
    ast = cparse.parse_file(kooc_file_name)
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

def register_module_symbol(module_name, symbol_name, symbol_type, mangled_name, params_types="", assign_node = None):
    vartype = "fun"
    if params_types == "":
        vartype = "var"
        params_types = "__666__"
    content = (mangled_name, assign_node)
    # modules["Moncul"]["tuturu"]["__saisonne__6"] = "poulet"
    # print(modules["Moncul"]["tuturu"]["__saisonne__6"])
    kfimpl.set_overload_content(module_name, symbol_name, vartype, params_types, symbol_type, content)




def debugCleanAll():
    imported_file_names.clear()
    modules.clear()
    kfimpl = KFImpl(imported_file_names, modules)
