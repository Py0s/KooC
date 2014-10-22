from pyrser import meta
import Knodes

@meta.add_method(Knodes.Class)
def mangle(self):
    self._identifier = 'K' + simple_mangling.identifier(self._identifier)
