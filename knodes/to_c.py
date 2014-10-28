
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
    for elem in self.declarations:
        res.lsdata.append(elem.to_c())
    return res

@meta.add_method(knodes.Class)
def to_c(self):
    self.mangle()
    self._specifier = nodes.Specifiers.STRUCT
    self._storage = nodes.Storages.TYPEDEF
    for item in self.fields:
        if not isinstance(item, knodes.Member):
            item._ctype._storage = nodes.Storages.EXTERN

@meta.add_method(knodes.Member)
def to_c(self):
    return self._content.to_c()

@meta.add_method(knodes.KDeclType)
def to_c(self):
    return super().to_c()

@meta.add_method(knodes.KPointerType)
def to_c(self):
    return super().to_c()

@meta.add_method(knodes.KArrayType)
def to_c(self):
    return super().to_c()

@meta.add_method(knodes.KParenType)
def to_c(self):
    return super().to_c()

@meta.add_method(knodes.KQualType)
def to_c(self):
    return super().to_c()

@meta.add_method(knodes.KAttrType)
def to_c(self):
    return super().to_c()

@meta.add_method(knodes.KType)
def to_c(self):
    return super().to_c()

@meta.add_method(knodes.KPrimaryType)
def to_c(self):
    return super().to_c()

@meta.add_method(knodes.KComposedType)
def to_c(self):
    return super().to_c()

@meta.add_method(knodes.KFuncType)
def to_c(self):
    return super().to_c()

@meta.add_method(knodes.KDecl)
def to_c(self):
    return super().to_c()
