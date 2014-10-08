
from pyrser import meta, fmt
from cnorm.passes import to_c
from Knodes import ImportNode

@meta.add_method(ImportNode)
def to_c(self):
    if self.already_imported:
        return fmt.sep("", [])
    lsbody = []
    lsbody.append(self.ifndef.to_c())
    lsbody.append(self.define.to_c()) 
    lsbody.append(self.body.to_c())
    lsbody.append(self.endif.to_c())
    return fmt.end("\n\n", fmt.tab(fmt.sep("\n", lsbody)))

def k_to_c(ast):
	return ast.to_c()
