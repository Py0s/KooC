
class KFImpl():
    def __init__(self, imported_file_names, modules):
        self.imported_file_names = imported_file_names
        self.modules = modules

# TODO : raise KoocException instead of RuntimeError

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
    #     return self.modules[module_name]

    def get_vartype_content(self, module_name, vartype):
        vartype_content = self.modules[module_name][vartype]
        if not vartype_content:
            raise RuntimeError("No " + vartype + "s in the module \"" + module_name + "\"")
        return vartype_content

    def get_symbol_content(self, module_name, vartype, symbol_name):
        symbol_content = self.modules[module_name][vartype][symbol_name]
        return self.check_no_definition(symbol_content, module_name, symbol_name, vartype)

    def get_params_content(self, module_name, vartype, symbol_name, params_types):
        params_content = self.modules[module_name][vartype][symbol_name][params_types]
        return self.check_no_definition(params_content, module_name, symbol_name, vartype)

    def get_overload_content(self, module_name, vartype, symbol_name, params_types, symbol_type):
        if type(params_types) != str:
            overload_content = params_types[symbol_type]# params_types est ici params_content
        else:
            overload_content = self.modules[module_name][vartype][symbol_name][params_types][symbol_type]
        return self.check_no_definition(overload_content, module_name, symbol_name, vartype)


    def set_overload_content(self, module_name, vartype, symbol_name, params_types, symbol_type, content):
        if self.modules[module_name][vartype][symbol_name][params_types][symbol_type]:
            raise RuntimeError("Redefinition of " + vartype + " \"" + symbol_name + "\" in the module \"" + module_name + "\"")
        self.modules[module_name][vartype][symbol_name][params_types][symbol_type] = content
