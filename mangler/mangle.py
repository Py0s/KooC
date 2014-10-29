from pyrser import meta
import knodes
import mangler.simple_mangling as sm

@meta.add_method(knodes.Module)
def mangle(self):
    self._identifier = 'M' + sm.id_m(self._identifier)

@meta.add_method(knodes.Class)
def mangle(self):
    self._identifier = 'K' + sm.id_m(self._identifier)

@meta.add_method(knodes.KDeclType)
def mangle(self):
    self._identifier = sm.type_m(self._identifier)

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
    self._identifier = sm.qual_m(self._identifier)

@meta.add_method(knodes.KAttrType)
def mangle(self):
    pass

@meta.add_method(knodes.KCType)
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
