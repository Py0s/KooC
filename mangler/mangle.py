from pyrser import meta
import knodes
import mangler.simple_mangling as sm

@meta.add_method(knodes.Module)
def mangle(self):
    return 'M' + sm.id_m(self._identifier)

@meta.add_method(knodes.Class)
def mangle(self):
    return 'K' + sm.id_m(self._identifier)

@meta.add_method(knodes.KDecl)
def mangle(self):
    if hasattr(self._ctype, 'mangle'):
        params = ''
        if isinstance(self._ctype, knodes.KFuncType):
            params += self._ctype.mangle_params();
        return (('' if self._scope is None else self._scope + '__') \
                + self.mangle_ctype() + sm.id_m(self._name) + params)

@meta.add_method(knodes.KDecl)
def mangle_ctype(self):
    if hasattr(self._ctype, 'mangle'):
        return self._ctype.mangle()

@meta.add_method(knodes.KPrimaryType)
def mangle(self):
    decltype = ''
    if self._decltype != None and hasattr(self._decltype, 'mangle'):
        decltype += self._decltype.mangle()
    return decltype + sm.type_m(self._identifier)

@meta.add_method(knodes.KPointerType)
def mangle(self):
    res = ''
    if self._decltype != None and hasattr(self._decltype, 'mangle'):
        res += self._decltype.mangle()
    return 'P' + res

@meta.add_method(knodes.KArrayType)
def mangle(self):
    res = ''
    if self._decltype != None and hasattr(self._decltype, 'mangle'):
        res += self._decltype.mangle()
    return 'A' + res

@meta.add_method(knodes.KFuncType)
def mangle(self):
    ptr = ''
    if self._decltype != None and hasattr(self._decltype, 'mangle'):
        ptr += self._decltype.mangle()
    return ptr + sm.type_m(self._identifier)

def raise_params(item):
    raise TypeError("Could not mangle type %s" %str(type(item)))

@meta.add_method(knodes.KFuncType)
def mangle_params(self):
    if len(self._params) == 0:
        return sm.type_m("void")
    gen = (item.mangle_ctype() if hasattr(item, 'mangle_ctype') else raise_params(item) for item in self._params)
    return ''.join(gen)

@meta.add_method(knodes.KQualType)
def mangle(self):
    res = ''
    ptr = ''
    if self._qualifier != None:
        res += sm.qual_m(self._qualifier)
    if self._decltype != None and hasattr(self._decltype, 'mangle'):
        ptr += self._decltype.mangle()
    return res + ptr