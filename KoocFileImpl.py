
class KFImpl():
    def __init__(self, imported_file_names, modules):
        self.imported_file_names = imported_file_names
        self.modules = modules

    def get_vartype(self, params_types):
        vartype = "fun"
        if params_types == "":
            vartype = "var"
            params_types = "__666__"
        return vartype
    # def get_module_content(self, module_name):
    #     return self.modules[module_name]

    # def get_symbol_content(self, module_name, symbol_name):
    #     return self.modules[module_name][symbol_name]

    # # vartype = "var" ou "fun"
    def get_vartype_content(self, module_name, symbol_name, vartype):
        vartype_content = self.modules[module_name][symbol_name][vartype]
        if not vartype_content:
            raise RuntimeError("No definition of symbol \"" + symbol_name + "\" in the module \"" + module_name + "\"")
        return vartype_content

    def get_params_content(self, module_name, symbol_name, vartype, params_types):
        params_content = self.modules[module_name][symbol_name][vartype][params_types]
        if not params_content:
            raise RuntimeError("No definition of symbol \"" + symbol_name + "\" in the module \"" + module_name + "\"")
        return params_content

    def get_overload_content(self, module_name, symbol_name, vartype, params_types, symbol_type):
        overload_content = self.modules[module_name][symbol_name][vartype][params_types][symbol_type]
        if not overload_content:
            raise RuntimeError("No definition of symbol \"" + symbol_name + "\" in the module \"" + module_name + "\"")
        return overload_content


    # def set_module_content(self, module_name, content):
    #     self.modules[module_name] = content

    # def set_symbol_content(self, module_name, symbol_name, content):
    #     self.modules[module_name][symbol_name] = content

    # # vartype = "var" ou "fun"
    # def set_vartype_content(self, module_name, symbol_name, vartype, content):
    #     self.modules[module_name][symbol_name][vartype] = content

    # def set_params_content(self, module_name, symbol_name, vartype, params_types, content):
    #     self.modules[module_name][symbol_name][vartype][params_types] = content

    def set_overload_content(self, module_name, symbol_name, vartype, params_types, symbol_type, content):
        if self.modules[module_name][symbol_name][vartype][params_types][symbol_type]:
            # print("EEEEEEEEEEERRRRRRRRRRRRRRRRRROOOOOOOOOOOOOOOOOOOOOOOOOOOOOOORRRRRRRRRRRRRRR POURQUOIIII ?")
            # print("params_types = ", params_types)
            # print("symbol_type = ", symbol_type)
            # print("vartype = ", vartype)
            # print("content = ", content)
            raise RuntimeError("Redefinition of symbol \"" + symbol_name + "\" in the module \"" + module_name + "\"")
        self.modules[module_name][symbol_name][vartype][params_types][symbol_type] = content
