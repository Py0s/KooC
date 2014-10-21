from pyrser import meta
import Knodes
import Mangler.simple_mangling as sm

@meta.add_method(Knodes.Class)
def mangle(self):
    self._identifier = 'K' + sm.identifier(self._identifier)
