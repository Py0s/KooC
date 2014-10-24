
from pyrser.grammar import Grammar
from pyrser import meta
from KoocGrammar.Import import Import
from KoocGrammar.Module import Module
from KoocGrammar.Class import Class
from KoocGrammar.Implementation import Implementation

class K_Declaration(Grammar, Import, Module, Class, Implementation):
    entry = "k_declaration"
    grammar = """
    k_declaration = [ Import.import | Module.module | Class.class | Implementation.implementation
    | Class.member:body #add_class_member(current_block, body)
    ]
    """

@meta.hook(K_Declaration)
def add_class_member(self, block, body):
    if hasattr(block, "ref") and hasattr(block.ref, "body") and hasattr(body, "body"):
        for elem in body.body:
            block.ref.body.append(elem)
    ## print("block member : ", block)
    return True
