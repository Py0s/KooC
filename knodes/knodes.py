from pyrser import fmt, parsing, meta
from cnorm import nodes
#import mangler.simple_mangling
import KoocFile
import os


Storages = meta.enum('AUTO', 'REGISTER', 'TYPEDEF',
                     'STATIC', 'EXTERN', 'INLINE',
                     'VIRTUAL', 'EXPLICIT',
                     'FORCEINLINE', 'THREAD')
Qualifiers = meta.enum('AUTO', 'CONST', 'VOLATILE', 'RESTRICT',
                       'W64', 'STDCALL', 'CDECL',
                       'PTR32', 'PTR64', 'FASTCALL')
Specifiers = meta.enum('AUTO', 'STRUCT', 'UNION', 'ENUM', 'LONG',
                       'LONGLONG', 'SHORT')
Signs = meta.enum('AUTO', 'SIGNED', 'UNSIGNED')




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
    """
        Everything here is a waste of my time.
        This class is coded here because cnorm doesn't use to_c() of ComposedType.
        Fuck quoi.
    """
    def __init__(self, identifier: str):
        super().__init__(identifier)

    # Séparer membre et non membre

class Member(parsing.Node):
    def __init__(self, content):
        if not isinstance(content, nodes.Decl):
            raise AttributeError("Content of Member should of declaration type")
        self._content = content










class KExpr(parsing.Node):
    """All expression"""


class KFunc(KExpr):
    """For almost everything"""

    def __init__(self, call_expr: KExpr, params: list):
        KExpr.__init__(self)
        self.call_expr = call_expr
        self.params = params


class KBlockInit(KExpr):
    """Initializer Block KExpression"""

    def __init__(self, body: [KExpr]):
        self.body = body


class KBlockKExpr(KExpr):
    """Compound Block KExpression"""

    def __init__(self, body: [KExpr]):
        self.body = body


class KUnary(KFunc):
    """For Kunary operator"""


class KParen(KUnary):
    """For () expression"""


class KArray(KUnary):
    """For [] expression"""


class KDot(KUnary):
    """For . expression"""


class KArrow(KUnary):
    """For -> expression"""


class KPost(KUnary):
    """For post{inc,dec} expression"""


class KSizeof(KUnary):
    """For sizeof expr/type expression"""


class KBinary(KFunc):
    """For binary operator"""


class KCast(KBinary):
    """For cast operator"""


class KRange(KBinary):
    """For range expression"""


class KTernary(KFunc):
    """For ternary operator"""


class KTerminal(KExpr):
    """For KTerminal expression"""

    def __init__(self, value: str):
        KExpr.__init__(self)
        self.value = value


class KId(KTerminal):
    """KTerminal Id"""


class KLiteral(KTerminal):
    """KTerminal Literal"""


class KRaw(KTerminal):
    """KTerminal Raw"""


# DECLARATION PART

class KEnumerator(parsing.Node):
    """KEnumerator A=x in enums"""

    def __init__(self, ident: str, expr: KExpr):
        self.ident = ident
        self.expr = expr


class KDeclType(parsing.Node):
    """For type in declaration"""

    def __init__(self):
        self._decltype = None

    def link(self, t: 'KDeclType'=None):
        if t is not None:
            if not isinstance(t, KDeclType):
                raise Exception("add only C type declarator")
            self._decltype = t
        return self._decltype

    def push(self, t: 'KDeclType'=None):
        if t is not None:
            if not isinstance(t, KDeclType):
                raise Exception("add only C type declarator")
            old = self._decltype
            self._decltype = t
            self._decltype.link(old)
        return self._decltype


class KPointerType(KDeclType):
    """For pointer in declaration"""


class KArrayType(KDeclType):
    """For array in declaration"""

    def __init__(self, expr=None):
        KDeclType.__init__(self)
        self._expr = expr

    @property
    def expr(self):
        return self._expr


class KParenType(KDeclType):
    """For parenthesis in declaration"""

    def __init__(self, params=None):
        KDeclType.__init__(self)
        if params is None:
            params = []
        self._params = params

    @property
    def params(self):
        return self._params


class KQualType(KDeclType):
    """For qualifier in declaration"""

    def __init__(self, qualifier: Qualifiers=Qualifiers.AUTO):
        KDeclType.__init__(self)
        # qualifier in (auto, const, volatile, restrict)
        self._qualifier = qualifier


class KAttrType(KDeclType):
    """For attribute specifier in declaration"""

    def __init__(self, raw: str):
        KDeclType.__init__(self)
        self._attr = raw


class KCType(parsing.Node):
    """Base for primary/func"""

    def __init__(self):
        parsing.Node.__init__(self)
        self._decltype = None
        # only one storage by declaration
        # i.e: auto, register, typedef, static, extern, ...
        self._storage = Storages.AUTO
        # only one specifier by declaration
        # i.e: auto, short, long, struct, union, enum, ...
        self._specifier = Specifiers.AUTO

    def copy(self):
        import copy
        theclone = copy.copy(self)
        theclone._decltype = None
        return theclone

    def link(self, t: KDeclType=None):
        if t is not None:
            if not isinstance(t, KDeclType):
                raise Exception("add only C type declarator")
            self._decltype = t
        return self._decltype

    def push(self, t: KDeclType=None):
        if t is not None:
            if not isinstance(t, KDeclType):
                raise Exception("add only C type declarator")
            old = self._decltype
            self._decltype = t
            self._decltype.link(old)
        return self._decltype


class KPrimaryType(KCType):
    """For primary type in declaration"""

    def __init__(self, identifier: str):
        KCType.__init__(self)
        # identifier (void, char, int, float, double, typedefname)
        self._identifier = identifier

    @property
    def identifier(self):
        return self._identifier


class KComposedType(KCType):
    """For composed type in declaration"""

    def __init__(self, identifier: str):
        KCType.__init__(self)
        # identifier (name of the struct/union/enum)
        self._identifier = identifier
        # if struct then self.fields = []
        # if enum then self.enums = []

    @property
    def identifier(self):
        return self._identifier


class KFuncType(KPrimaryType):
    """For function in declaration"""

    def __init__(self, identifier: str, params=[], decltype=None):
        KPrimaryType.__init__(self, identifier)
        self.opened = True
        if decltype is not None:
            self._decltype = decltype
        self._params = params

    @property
    def params(self):
        return self._params


# helper to create a KCType from previous one
def makeKCType(declspecifier: str, ctype=None):
    from cnorm.parsing.expression import Idset
    if ctype is None:
        ctype = KPrimaryType('int')
    if Idset[declspecifier] == "type":
        ctype._identifier = declspecifier
    if Idset[declspecifier] == "storage":
        cleantxt = declspecifier.strip("_")
        ctype._storage = Storages.map[cleantxt.upper()]
    if Idset[declspecifier] == "qualifier":
        cleantxt = declspecifier.strip("_")
        ctype.link(QualType(Qualifiers.map[cleantxt.upper()]))
    if Idset[declspecifier] == "funspecifier":
        cleantxt = declspecifier.strip("_")
        ctype._storage = Storages.map[cleantxt.upper()]
    if Idset[declspecifier] == "sign_unsigned":
        cleantxt = declspecifier.strip("_")
        ctype._sign = Signs.map[cleantxt.upper()]
    if Idset[declspecifier] == "sign_signed":
        cleantxt = declspecifier.strip("_")
        ctype._sign = Signs.map[cleantxt.upper()]
    if Idset[declspecifier] == "specifier_block":
        cleantxt = declspecifier.strip("_")
        ctype._specifier = Specifiers.map[cleantxt.upper()]
    if Idset[declspecifier] == "specifier_enum":
        cleantxt = declspecifier.strip("_")
        ctype._specifier = Specifiers.map[cleantxt.upper()]
    if Idset[declspecifier] == "specifier_size":
        cleantxt = declspecifier.strip("_")
        ctype._specifier = Specifiers.map[cleantxt.upper()]
    if Idset[declspecifier] == "specifier_size_size":
        cleantxt = declspecifier.strip("_")
        if ctype._specifier == Specifiers.AUTO:
            ctype._specifier = Specifiers.map[cleantxt.upper()]
        else:
            ctype._specifier = Specifiers.LONGLONG
    return ctype


class KDecl(KExpr):
    """For basic declaration

        A declaration contains the following attributes:

        * _name: name of the declaration
        * _ctype: the KCType describing the type of the declaration
        * _assign_expr: when the declaration have a value
        * _colon_expr: When it's a bitfield
        * body: when it's function definition

    """

    def __init__(self, name: str, ct=None):
        if ct is None:
            ct = KPrimaryType('int')
        KExpr.__init__(self)
        self._name = name
        self._ctype = ct

    @property
    def ctype(self) -> KCType:
        return self._ctype

    def assign_expr(self, expr=None):
        if not hasattr(self, '_assign_expr'):
            self._assign_expr = None
        if expr is not None:
            self._assign_expr = expr
        return self._assign_expr

    def colon_expr(self, expr=None):
        if not hasattr(self, '_colon_expr'):
            self._colon_expr = None
        if expr is not None:
            self._colon_expr = expr
        return self._colon_expr


# STATEMENT PART


class KStmt(parsing.Node):
    """For statement"""


class KExprStmt(KStmt):
    """KExpression statement"""

    def __init__(self, expr: KExpr):
        parsing.Node.__init__(self)
        self.expr = expr


class KBlockStmt(KStmt):
    """Block statement"""

    def __init__(self, body: [KExprStmt]):
        parsing.Node.__init__(self)
        self.body = body

    def func(self, name: str):
        """return the func defined named name"""

    def var(self, name: str):
        """return the var instancied named name"""

    def type(self, name: str):
        """return the complete definition of type 'name'"""

    def declfuncs(self, name: str):
        """return all declaration of function 'name'"""

    def declvars(self, name: str):
        """return all declaration of variable 'name'"""

    def decltypes(self, name: str):
        """return all declaration of type 'name'"""


class KRootBlockStmt(KBlockStmt):
    """Root Block statement"""

    def __init__(self, body: [KExprStmt]):
        KBlockStmt.__init__(self, body)
        from collections import ChainMap
        self.types = ChainMap()


class KLabel(KStmt):
    """KLabel statement"""

    def __init__(self, value: str):
        KStmt.__init__(self)
        self.value = value


class KBranch(KLabel):
    """branch statement"""

    def __init__(self, value: str, expr: KExpr):
        KLabel.__init__(self, value)
        self.expr = expr


class KCase(KBranch):
    """KCase statement"""

    def __init__(self, expr: KExpr):
        KBranch.__init__(self, "case", expr)


class KReturn(KBranch):
    """KReturn statement"""

    def __init__(self, expr: KExpr):
        KBranch.__init__(self, "return", expr)


class KGoto(KBranch):
    """KGoto statement"""

    def __init__(self, expr: KExpr):
        KBranch.__init__(self, "goto", expr)


class KLoopControl(KLabel):
    """Kloop control statement"""


class KBreak(KLoopControl):
    """Kbreak statement"""

    def __init__(self):
        KLabel.__init__(self, "break")


class KContinue(KLoopControl):
    """Kcontinue statement"""

    def __init__(self):
        KLabel.__init__(self, "continue")


class KConditional(KStmt):
    """KConditional statement"""

    def __init__(self, condition: KExpr):
        KStmt.__init__(self)
        self.condition = condition


class KIf(KConditional):
    """KIf statement"""

    def __init__(self, condition: KExpr, thencond: KStmt, elsecond: KStmt=None):
        KConditional.__init__(self, condition)
        self.thencond = thencond
        self.elsecond = elsecond


class KWhile(KConditional):
    """KWhile statement"""

    def __init__(self, condition: KExpr, body: KStmt):
        KConditional.__init__(self, condition)
        self.body = body


class KSwitch(KConditional):
    """KSwitch statement"""

    def __init__(self, condition: KExpr, body: KStmt):
        KConditional.__init__(self, condition)
        self.body = body


class KDo(KConditional):
    """KDo statement"""

    def __init__(self, condition: KExpr, body: KStmt):
        KConditional.__init__(self, condition)
        self.body = body


class KFor(KStmt):
    """KFor statement"""

    def __init__(self, init: KExpr, condition: KExpr,
                 increment: KExpr, body: KStmt):
        KStmt.__init__(self)
        self.init = init
        self.condition = condition
        self.increment = increment
        self.body = body










# class KDeclType(nodes.DeclType):
#     """For type in declaration"""
#     def __init__(self, call_expr, params):
#         super().__init__(call_expr, params)

# class KPointerType(nodes.PointerType):
#     """For pointer in declaration"""
#     def __init__(self, call_expr, params):
#         super().__init__(call_expr, params)

# class KArrayType(nodes.ArrayType):
#     """For array in declaration"""
#     def __init__(self, call_expr, params):
#         super().__init__(call_expr, params)

# class KParenType(nodes.ParenType):
#     """For parenthesis in declaration"""
#     def __init__(self, call_expr, params):
#         super().__init__(call_expr, params)

# class KQualType(nodes.QualType):
#     """For qualifier in declaration"""
#     def __init__(self, call_expr, params):
#         super().__init__(call_expr, params)

# class KAttrType(nodes.AttrType):
#     """For attribute specifier in declaration"""
#     def __init__(self, call_expr, params):
#         super().__init__(call_expr, params)

# class KType(nodes.CType):
#     """Base for primary/func"""
#     def __init__(self, call_expr, params):
#         super().__init__(call_expr, params)

# class KPrimaryType(nodes.PrimaryType):
#     """For primary type in declaration"""
#     def __init__(self, call_expr, params):
#         super().__init__(call_expr, params)

# class KComposedType(nodes.ComposedType):
#     """For composed type in declaration"""
#     def __init__(self, call_expr, params):
#         super().__init__(call_expr, params)

# class KFuncType(nodes.FuncType):
#     """For function in declaration"""
#     def __init__(self, call_expr, params):
#         super().__init__(call_expr, params)

# class KDecl(nodes.Decl):
#     """For basic declaration
#     A declaration contains the following attributes:
#     * _name: name of the declaration
#     * _ctype: the CType describing the type of the declaration
#     * _assign_expr: when the declaration have a value
#     * _colon_expr: When it's a bitfield
#     * body: when it's function definition """
#     def __init__(self, call_expr, params):
#         super().__init__(call_expr, params)
