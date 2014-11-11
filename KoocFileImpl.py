
class KFImpl():
    def __init__(self, imported_file_names, modules, classes):
        self.imported_file_names = imported_file_names
        self.modules = modules
        self.classes = classes

# TODO : raise KoocException instead of RuntimeError

###########
## UTILS ##
###########

    def check_no_definition(self, content, module_name, symbol_name, vartype):
        if not content:
            raise RuntimeError("No declaration of " + vartype + " \"" + symbol_name + "\" in the module \"" + module_name + "\"")
        return content

    def check_ambiguous(self, content, module_name, symbol_name, vartype):
        if len(content) > 1:
            raise RuntimeError("Ambiguous call of " + vartype + " \"" + symbol_name + "\" from the module \"" + module_name + "\"")

    def get_vartype(self, params_types):
        if params_types == "":
            vartype = "variable"
            params_types = "__666__"
        else:
            vartype = "function"
        return vartype
    # def get_module_content(self, module_name):
    #     return mc[module_name]

#############
## SETTERS ##
#############

    def register_symbol(self, mc, module_name, symbol_name, params_types, symbol_type, mangled_name, assign_node = None):
        # print("REGISTER: ", module_name, symbol_name, params_types, symbol_type, mangled_name)
        vartype = self.get_vartype(params_types)
        content = (mangled_name, assign_node)
        self.set_overload_content(mc, module_name, vartype, symbol_name, params_types, symbol_type, content)

    def set_overload_content(self, mc, module_name, vartype, symbol_name, params_types, symbol_type, content):
        if mc[module_name][vartype][symbol_name][params_types][symbol_type]:
            raise RuntimeError("Redeclaration of " + vartype + " \"" + symbol_name + "\" in the module \"" + module_name + "\"")
        mc[module_name][vartype][symbol_name][params_types][symbol_type] = content


#############
## GETTERS ##
#############

    def get_vartype_content(self, mc, module_name, vartype):
        vartype_content = mc[module_name][vartype]
        if not vartype_content:
            raise RuntimeError("No " + vartype + "s in the module \"" + module_name + "\"")
        return vartype_content

    def get_symbol_content(self, mc, module_name, vartype, symbol_name):
        symbol_content = mc[module_name][vartype][symbol_name]
        return self.check_no_definition(symbol_content, module_name, symbol_name, vartype)

    def get_params_content(self, mc, module_name, vartype, symbol_name, params_types):
        params_content = mc[module_name][vartype][symbol_name][params_types]
        return self.check_no_definition(params_content, module_name, symbol_name, vartype)

    def get_overload_content(self, mc, module_name, vartype, symbol_name, params_types, symbol_type):
        if type(params_types) != str:
            overload_content = params_types[symbol_type]# params_types est ici params_content
        else:
            overload_content = mc[module_name][vartype][symbol_name][params_types][symbol_type]
        return self.check_no_definition(overload_content, module_name, symbol_name, vartype)

    def mangled_name_of_symbol(self, mc, module_name, symbol_name, params_types=None, symbol_type=""):
        # print("TRY TO GET: ", module_name, symbol_name, params_types, symbol_type)
        if params_types == None:
            vartype = "function"
        else:
            vartype = self.get_vartype(params_types)
    
        symbol_content = self.get_symbol_content(mc, module_name, vartype, symbol_name)
    
        if not params_types:
            self.check_ambiguous(symbol_content, module_name, symbol_name, vartype)
            params_content = next(iter(symbol_content.values()))
        else:
            params_content = self.get_params_content(mc, module_name, vartype, symbol_name, params_types)
    
        if not symbol_type or symbol_type == "":
            self.check_ambiguous(params_content, module_name, symbol_name, vartype)
            overload_content = next(iter(params_content.values()))
        else:
            overload_content = self.get_overload_content(mc, module_name, vartype, symbol_name, params_content, symbol_type)
    
        # print("OK : ", overload_content[0])
        return overload_content[0]

    def assign_node_of_symbol(self, mc, module_name, symbol_name, params_types, symbol_type):
        vartype = self.get_vartype(params_types)
        return self.get_overload_content(module_name, vartype, symbol_name, params_types, symbol_type)[1]
