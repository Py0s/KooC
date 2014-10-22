
from pyrser.grammar import Grammar
from KoocGrammar.Import import Import
from KoocGrammar.Module import Module
from KoocGrammar.Class import Class
from KoocGrammar.Implementation import Implementation

class K_Declaration(Grammar, Import, Module, Implementation):
    entry = "k_declaration"
    grammar = """
    k_declaration = [ Import.import:>_ | Module.module:>_ | Class.class:>_ | Implementation.implementation:>_ ]
    """
