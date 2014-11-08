
class KFImpl():
    def __init__(self, imported_file_names, modules):
        self.imported_file_names = imported_file_names
        self.modules = modules

    # def get_module_content(self, module_name):
    #     return self.modules[module_name]

    # def get_symbol_content(self, module_name, symbol_name):
    #     return self.modules[module_name][symbol_name]

    # # vartype_name = "var" ou "fun"
    # def get_vartype_content(self, module_name, symbol_name, vartype_name):
    #     return self.modules[module_name][symbol_name][vartype_name]

    # def get_params_content(self, module_name, symbol_name, vartype_name, params_types):
    #     return self.modules[module_name][symbol_name][vartype_name][params_types]

    # def get_overload_content(self, module_name, symbol_name, vartype_name, params_types, symbol_type):
    #     return self.modules[module_name][symbol_name][vartype_name][params_types][symbol_type]


    # def set_module_content(self, module_name, content):
    #     self.modules[module_name] = content

    # def set_symbol_content(self, module_name, symbol_name, content):
    #     self.modules[module_name][symbol_name] = content

    # # vartype_name = "var" ou "fun"
    # def set_vartype_content(self, module_name, symbol_name, vartype_name, content):
    #     self.modules[module_name][symbol_name][vartype_name] = content

    # def set_params_content(self, module_name, symbol_name, vartype_name, params_types, content):
    #     self.modules[module_name][symbol_name][vartype_name][params_types] = content

    def set_overload_content(self, module_name, symbol_name, vartype_name, params_types, symbol_type, content):
        if self.modules[module_name][symbol_name][vartype_name][params_types][symbol_type]:
            # print("EEEEEEEEEEERRRRRRRRRRRRRRRRRROOOOOOOOOOOOOOOOOOOOOOOOOOOOOOORRRRRRRRRRRRRRR POURQUOIIII ?")
            # print("params_types = ", params_types)
            # print("symbol_type = ", symbol_type)
            # print("vartype_name = ", vartype_name)
            # print("content = ", content)
            raise RuntimeError("Redefinition of symbol \"" + symbol_name + "\" in the module \"" + module_name + "\"")
        self.modules[module_name][symbol_name][vartype_name][params_types][symbol_type] = content
