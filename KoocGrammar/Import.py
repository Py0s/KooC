#!/usr/bin/env python3

from pyrser.grammar import Grammar
from pyrser import meta
import knodes

class   Import(Grammar):
    entry = 'translation_unit'
    grammar = """
        import = [ @ignore("blanks") "@import" Import.Name:name #Imp(current_block, name) ]
        Name = [ '"'
                [ ['a'..'z'] | ['A'..'Z'] | '_' ]+
                ".kh" '"' ]
    """

@meta.hook(Import)
def Imp(self, ast, name):
    ast.ref.body.append(knodes.Import(self.value(name)))
    return True
