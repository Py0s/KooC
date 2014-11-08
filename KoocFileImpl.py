
class KFImpl():
    def __init__(self, imported_file_names, modules, classes):
        self.imported_file_names = imported_file_names
        self.modules = modules
        self.classes = classes

    def params_types_equals(self, first, second):
        for f, s in zip(first, second):
            if f != s:
                return False
        return True

    def symbol_entry_in_module(self, module_name, symbol_name):
        return self.modules[module_name][symbol_name]
    def symbol_entry_in_classe(self, classe_name, symbol_name):
        return self.classes[classe_name][symbol_name]

    def symbol_overload(self, symbol_entry, symbol_type, params_types=[]):
        for overload in symbol_entry:
            if overload[0] == symbol_type and params_types_equals(overload[1], params_types):
                return overload
        return None

    def is_var_in_module(self, module_name, symbol_name, symbol_type, params_types=[]):
        if module_name in self.modules\
            and symbol_name in self.modules[module_name]:
                for overload in self.modules[module_name][symbol_name]:
                    if overload[0] == symbol_type and params_types_equals(overload[1], params_types):
                        return True
        return False
    
    def get_var_from_module(self, module_name, symbol_name, symbol_type, params_types=[]):
        if not is_var_in_module(module_name, symbol_name, symbol_type, params_types):
            raise RuntimeError("try to get unknown node")
        symbol_entry = self.modules[module_name][symbol_name]
        return symbol_overload(symbol_entry, symbol_type, params_types)

    def get_var_for_symbol(self, module_name, symbol_name, symbol_type, params_types=[]):
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
