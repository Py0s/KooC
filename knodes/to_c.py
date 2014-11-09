
from pyrser import meta, fmt
from cnorm.passes import to_c
from cnorm import nodes
import knodes
import mangler

def k_to_c(ast):
    return ast.to_c()

@meta.add_method(knodes.Import)
def to_c(self):
    if self.already_imported:
        return fmt.sep("", [])
    lsbody = []
    lsbody.append(self.ifndef.to_c())
    lsbody.append(self.define.to_c())
    lsbody.append(self.body.to_c())
    lsbody.append(self.endif.to_c())
    return fmt.end("\n\n", fmt.tab(fmt.sep("\n", lsbody)))

@meta.add_method(knodes.Module)
def to_c(self):
    res = fmt.sep("", [])
    for elem in self._declarations:
        res.lsdata.append(elem.to_c())
    return res

@meta.add_method(knodes.Class)
def to_c(self):
    self._identifier = self.mangle()
    self._specifier = nodes.Specifiers.STRUCT
    self._storage = nodes.Storages.TYPEDEF
    for item in self.fields:
        if not isinstance(item, knodes.Member):
            item._ctype._storage = nodes.Storages.EXTERN

@meta.add_method(knodes.Member)
def to_c(self):
    return self._content.to_c()

@meta.add_method(knodes.KDecl)
def to_c(self):
    # self._name = self.mangle()
    return nodes.Decl.to_c(self)

# @meta.add_method(knodes.KDeclType)
# def to_c(self):
#     return super().to_c()

# @meta.add_method(knodes.KPointerType)
# def to_c(self):
#     return super().to_c()

# @meta.add_method(knodes.KArrayType)
# def to_c(self):
#     return super().to_c()

# @meta.add_method(knodes.KParenType)
# def to_c(self):
#     return super().to_c()

# @meta.add_method(knodes.KQualType)
# def to_c(self):
#     return super().to_c()

# @meta.add_method(knodes.KAttrType)
# def to_c(self):
#     return super().to_c()

# @meta.add_method(knodes.KCType)
# def to_c(self):
#     return super().to_c()

# @meta.add_method(knodes.KPrimaryType)
# def to_c(self):
#     return super().to_c()

# @meta.add_method(knodes.KComposedType)
# def to_c(self):
#     return super().to_c()

# @meta.add_method(knodes.KFuncType)
# def to_c(self):
#     return super().to_c()

# @meta.add_method(knodes.KExpr)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KFunc)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KBlockInit)
# def to_c(self):
#     return super().to_c()
#
# @meta.add_method(knodes.KBlockExpr)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KUnary)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KParen)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KArray)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KDot)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KArrow)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KPost)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KSizeof)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KBinary)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KCast)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KRange)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KTernary)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KTerminal)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KId)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KLiteral)
# def to_c(self):
#     return super().to_c()


# @meta.add_method(knodes.KRaw)
# def to_c(self):
#     return super().to_c(self)


# DECLARATION PART

# @meta.add_method(knodes.KEnumerator)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KDeclType)
# def to_c(self):
#     return super().to_c()
#
# @meta.add_method(knodes.KPointerType)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KArrayType)
# def to_c(self):
#     return super().to_c()
#
# @meta.add_method(knodes.KParenType)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KQualType)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KAttrType)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KCType)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KPrimaryType)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KComposedType)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KFuncType)
# def to_c(self):
#     return super().to_c()


# STATEMENT PART


# @meta.add_method(knodes.KStmt)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KExprStmt)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KBlockStmt)
# def to_c(self):
#     return super().to_c()

# @meta.add_method(knodes.KRootBlockStmt)
# def to_c(self):
#     return ""


# @meta.add_method(knodes.KLabel)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KBranch)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KCase)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KReturn)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KGoto)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KLoopControl)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KBreak)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KContinue)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KConditional)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KIf)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KWhile)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KSwitch)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KDo)
# def to_c(self):
#     return super().to_c()
#
#
# @meta.add_method(knodes.KFor)
# def to_c(self):
#     return super().to_c()

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
