from pyrser import meta
import knodes

@meta.add_method(knodes.Module)
def mangle(self):
    pass

@meta.add_method(knodes.Class)
def mangle(self):
    self._identifier = 'K' + simple_mangling.identifier(self._identifier)

@meta.add_method(knodes.KDeclType)
def mangle(self):
    pass

@meta.add_method(knodes.KPointerType)
def mangle(self):
    pass

@meta.add_method(knodes.KArrayType)
def mangle(self):
    pass

@meta.add_method(knodes.KParenType)
def mangle(self):
    pass

@meta.add_method(knodes.KQualType)
def mangle(self):
    pass

@meta.add_method(knodes.KAttrType)
def mangle(self):
    pass

@meta.add_method(knodes.KType)
def mangle(self):
    pass

@meta.add_method(knodes.KPrimaryType)
def mangle(self):
    pass

@meta.add_method(knodes.KComposedType)
def mangle(self):
    pass

@meta.add_method(knodes.KFuncType)
def mangle(self):
    pass

@meta.add_method(knodes.KDecl)
def mangle(self):
    pass
