from pyrser import fmt, parsing
from cnorm import nodes
import KoocFile
import os

class Import(nodes.BlockStmt):
    """Import"""
    def __init__(self, name):
        self.name = name
        self.cut_header_name()
        body = nodes.Raw("")
        self.already_imported = KoocFile.is_file_imported(self.fileNameMacro)
        if not self.already_imported:
            self.ifndef = nodes.Raw("#ifndef " + self.fileNameMacro)
            self.define = nodes.Raw("# define " + self.fileNameMacro)
            self.endif = nodes.Raw("#endif /* " + self.fileNameMacro + " */")
            KoocFile.register_file(self.fileNameMacro)
            body = KoocFile.kooc_a_file(self.fileName + ".kh")
        super().__init__(body)

    def cut_header_name(self):
        self.name = KoocFile.includePath + "/" + self.name[1:]
        self.fileName, fileExtension = os.path.splitext(self.name)
        self.fileNameMacro = (self.fileName.upper() + "_H_").replace("\\", "_").replace(".", "_").replace("/", "_")

class Module(parsing.Node):
    def __init__(self):
        self.declarations = []

class Class(nodes.ComposedType):
    def __init__(self, identifier: str):
        super().__init__(identifier);

class KDeclType(nodes.DeclType):
    """For type in declaration"""
    def __init__(self, call_expr, params):
        super().__init__(call_expr, params)

class KPointerType(nodes.PointerType):
    """For pointer in declaration"""
    def __init__(self, call_expr, params):
        super().__init__(call_expr, params)

class KArrayType(nodes.ArrayType):
    """For array in declaration"""
    def __init__(self, call_expr, params):
        super().__init__(call_expr, params)

class KParenType(nodes.ParenType):
    """For parenthesis in declaration"""
    def __init__(self, call_expr, params):
        super().__init__(call_expr, params)

class KQualType(nodes.QualType):
    """For qualifier in declaration"""
    def __init__(self, call_expr, params):
        super().__init__(call_expr, params)

class KAttrType(nodes.AttrType):
    """For attribute specifier in declaration"""
    def __init__(self, call_expr, params):
        super().__init__(call_expr, params)

class KType(nodes.CType):
    """Base for primary/func"""
    def __init__(self, call_expr, params):
        super().__init__(call_expr, params)

class KPrimaryType(nodes.PrimaryType):
    """For primary type in declaration"""
    def __init__(self, call_expr, params):
        super().__init__(call_expr, params)

class KComposedType(nodes.ComposedType):
    """For composed type in declaration"""
    def __init__(self, call_expr, params):
        super().__init__(call_expr, params)

class KFuncType(nodes.FuncType):
    """For function in declaration"""
    def __init__(self, call_expr, params):
        super().__init__(call_expr, params)

class KDecl(nodes.Decl):
    """For basic declaration
    A declaration contains the following attributes:
    * _name: name of the declaration
    * _ctype: the CType describing the type of the declaration
    * _assign_expr: when the declaration have a value
    * _colon_expr: When it's a bitfield
    * body: when it's function definition """
    def __init__(self, call_expr, params):
        super().__init__(call_expr, params)
