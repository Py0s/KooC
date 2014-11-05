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
        print(self)
        print("=============================")
        if isinstance(self._ctype, knodes.KFuncType):
            params += self._ctype.mangle_params();
        return (('' if self._scope is None else self._scope + '__') \
                + self.mangle_type() + sm.id_m(self._name) + params)

@meta.add_method(knodes.KDecl)
def mangle_type(self):
    if hasattr(self._ctype, 'mangle'):
        return self._ctype.mangle()

@meta.add_method(knodes.KPrimaryType)
def mangle(self):
    ptr = ''
    if self._decltype != None and hasattr(self._decltype, 'mangle'):
        ptr += self._decltype.mangle()
    return ptr + sm.type_m(self._identifier)

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
    gen = (item.mangle_type() if hasattr(item, 'mangle_type') else raise_params(item) for item in self._params)
    return ''.join(gen)
