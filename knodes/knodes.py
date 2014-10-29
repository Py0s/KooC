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










class KExpr(nodes.Expr):
    """All KExpression"""


class KFunc(nodes.Func):
    """For almost everything"""
    def __init__(self, call_expr: KExpr, params: list):
        super().__init__(call_expr, params)

class KBlockInit(nodes.BlockInit):
    """Initializer Block KExpression"""
    def __init__(self, body: [KExpr]):
        super().__init__(body)


class KBlockExpr(nodes.BlockExpr):
    """Compound Block KExpression"""
    def __init__(self, body: [KExpr]):
        super().__init__(body)

class KUnary(nodes.Unary):
    """For Kunary operator"""


class KParen(nodes.Paren):
    """For () KExpression"""


class KArray(nodes.Array):
    """For [] KExpression"""


class KDot(nodes.Dot):
    """For . KExpression"""


class KArrow(nodes.Arrow):
    """For -> KExpression"""


class KPost(nodes.Post):
    """For post{inc,dec} KExpression"""


class KSizeof(nodes.Sizeof):
    """For sizeof KExpr/type KExpression"""


class KBinary(nodes.Binary):
    """For binary operator"""


class KCast(nodes.Cast):
    """For cast operator"""


class KRange(nodes.Range):
    """For range KExpression"""


class KTernary(nodes.Ternary):
    """For ternary operator"""


class KTerminal(nodes.Terminal):
    """For KTerminal KExpression"""
    def __init__(self, value: str):
        super().__init__(self, value)


class KId(nodes.Id):
    """KTerminal Id"""


class KLiteral(nodes.Literal):
    """KTerminal Literal"""


class KRaw(nodes.Raw):
    """KTerminal Raw"""


# DECLARATION PART

class KEnumerator(nodes.Enumerator):
    """KEnumerator A=x in enums"""
    def __init__(self, ident: str, expr: KExpr):
        super().__init__(ident, expr)


class KDeclType(nodes.DeclType):
    """For type in declaration"""
    def __init__(self):
        super().__init__()


class KPointerType(nodes.PointerType):
    """For pointer in declaration"""


class KArrayType(nodes.ArrayType):
    """For array in declaration"""
    def __init__(self, expr=None):
        super().__init__(expr)


class KParenType(nodes.ParenType):
    """For parenthesis in declaration"""
    def __init__(self, params=None):
        super().__init__(params)


class KQualType(nodes.QualType):
    """For qualifier in declaration"""
    def __init__(self, qualifier: Qualifiers=Qualifiers.AUTO):
        super().__init__(qualifier)


class KAttrType(nodes.AttrType):
    """For attribute specifier in declaration"""
    def __init__(self, raw: str):
        super().__init__(raw)


class KCType(nodes.CType):
    """Base for primary/func"""
    def __init__(self):
        super().__init__()


class KPrimaryType(nodes.PrimaryType):
    """For primary type in declaration"""
    def __init__(self, identifier: str):
        super().__init__(identifier)


class KComposedType(nodes.ComposedType):
    """For composed type in declaration"""
    def __init__(self, identifier: str):
        super().__init__(identifier)


class KFuncType(nodes.FuncType):
    """For function in declaration"""
    def __init__(self, identifier: str, params=[], decltype=None):
        super().__init__(identifier, params, decltype)


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


class KDecl(nodes.Decl):
    """For basic declaration

        A declaration contains the following attributes:

        * _name: name of the declaration
        * _ctype: the KCType describing the type of the declaration
        * _assign_expr: when the declaration have a value
        * _colon_expr: When it's a bitfield
        * body: when it's function definition
    """
    def __init__(self, name: str, ct=None):
        super().__init__(name, ct)

# STATEMENT PART


class KStmt(nodes.Stmt):
    """For statement"""


class KExprStmt(nodes.ExprStmt):
    """KExpression statement"""
    def __init__(self, expr: KExpr):
        super().__init__(expr)


class KBlockStmt(nodes.BlockStmt):
    """Block statement"""
    def __init__(self, body: [KExprStmt]):
        super().__init__(body)


class KRootBlockStmt(nodes.RootBlockStmt):
    """Root Block statement"""
    def __init__(self, body: [KExprStmt]):
        super().__init__(body)


class KLabel(nodes.Label):
    """KLabel statement"""
    def __init__(self, value: str):
        super().__init__(value)


class KBranch(nodes.Branch):
    """branch statement"""
    def __init__(self, value: str, expr: KExpr):
        super().__init__(value, expr)


class KCase(nodes.Case):
    """KCase statement"""
    def __init__(self, expr: KExpr):
        super().__init__(expr)


class KReturn(nodes.Return):
    """KReturn statement"""
    def __init__(self, expr: KExpr):
        super().__init__(expr)


class KGoto(nodes.Goto):
    """KGoto statement"""
    def __init__(self, expr: KExpr):
        super().__init__(expr)


class KLoopControl(nodes.LoopControl):
    """Kloop control statement"""


class KBreak(nodes.Break):
    """Kbreak statement"""


class KContinue(nodes.Continue):
    """Kcontinue statement"""


class KConditional(nodes.Conditional):
    """KConditional statement"""

    def __init__(self, condition: KExpr):
        super().__init__(condition)


class KIf(nodes.If):
    """KIf statement"""

    def __init__(self, condition: KExpr, thencond: KStmt, elsecond: KStmt=None):
        super().__init__(condition, thencond, elsecond)


class KWhile(nodes.While):
    """KWhile statement"""

    def __init__(self, condition: KExpr, body: KStmt):
        super().__init__(condition, body)


class KSwitch(nodes.Switch):
    """KSwitch statement"""

    def __init__(self, condition: KExpr, body: KStmt):
        super().__init__(condition, body)

class KDo(nodes.Do):
    """KDo statement"""

    def __init__(self, condition: KExpr, body: KStmt):
        super().__init__(condition, body)

class KFor(nodes.For):
    """KFor statement"""

    def __init__(self, init: KExpr, condition: KExpr,
                 increment: KExpr, body: KStmt):
        super().__init__(init, condition, increment, body)









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
