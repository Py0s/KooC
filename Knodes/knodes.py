from cnorm import nodes

# class K_(nodes.??):
#     def __init__(self, call_expr, params):
#         super().__init__(call_expr, params)

#     def to_c(self):
#         return syper().to_c()

#     def mangle(self):
#         return

class   k_decl_type(nodes.DeclType):
    """For type in declaration"""
    def __init__(self, call_expr, params):
        super().__init__(call_expr, params)

    def to_c(self):
        return syper().to_c()

    def mangle(self):
        return


class   k_pointer_type(nodes.PointerType):
    """For pointer in declaration"""
    def __init__(self, call_expr, params):
        super().__init__(call_expr, params)

    def to_c(self):
        return syper().to_c()

    def mangle(self):
        return


class   k_array_type(nodes.ArrayType):
    """For array in declaration"""
    def __init__(self, call_expr, params):
        super().__init__(call_expr, params)

    def to_c(self):
        return syper().to_c()

    def mangle(self):
        return


class   k_paren_type(nodes.ParenType):
    """For parenthesis in declaration"""
    def __init__(self, call_expr, params):
        super().__init__(call_expr, params)

    def to_c(self):
        return syper().to_c()

    def mangle(self):
        return


class   k_qual_type(nodes.QualType):
    """For qualifier in declaration"""
    def __init__(self, call_expr, params):
        super().__init__(call_expr, params)

    def to_c(self):
        return syper().to_c()

    def mangle(self):
        return


class   k_attr_type(nodes.AttrType):
    """For attribute specifier in declaration"""
    def __init__(self, call_expr, params):
        super().__init__(call_expr, params)

    def to_c(self):
        return syper().to_c()

    def mangle(self):
        return


class   k_ctype(nodes.CType):
    """Base for primary/func"""
    def __init__(self, call_expr, params):
        super().__init__(call_expr, params)

    def to_c(self):
        return syper().to_c()

    def mangle(self):
        return


class   k_primary_type(nodes.PrimaryType):
    """For primary type in declaration"""
    def __init__(self, call_expr, params):
        super().__init__(call_expr, params)

    def to_c(self):
        return syper().to_c()

    def mangle(self):
        return


class   k_composed_type(nodes.ComposedType):
    """For composed type in declaration"""
    def __init__(self, call_expr, params):
        super().__init__(call_expr, params)

    def to_c(self):
        return syper().to_c()

    def mangle(self):
        return


class   k_func_type(nodes.FuncType):
    """For function in declaration"""
    def __init__(self, call_expr, params):
        super().__init__(call_expr, params)

    def to_c(self):
        return syper().to_c()

    def mangle(self):
        return


class   k_decl(nodes.Decl):
    """For basic declaration
    A declaration contains the following attributes:
    * _name: name of the declaration
    * _ctype: the CType describing the type of the declaration
    * _assign_expr: when the declaration have a value
    * _colon_expr: When it's a bitfield
    * body: when it's function definition """
    def __init__(self, call_expr, params):
        super().__init__(call_expr, params)

    def to_c(self):
        return syper().to_c()

    def mangle(self):
        return
