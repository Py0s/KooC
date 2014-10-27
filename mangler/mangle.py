from pyrser import meta
import knodes

@meta.add_method(knodes.Class)
def mangle(self):
    self._identifier = 'K' + simple_mangling.identifier(self._identifier)
