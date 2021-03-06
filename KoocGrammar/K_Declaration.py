
from pyrser.grammar import Grammar
from pyrser import meta
from KoocGrammar.Import import Import
from KoocGrammar.Module import Module
from KoocGrammar.Class import Class
from KoocGrammar.Implementation import Implementation

class K_Declaration(Grammar, Import, Module, Class, Implementation):
    entry = "k_declaration"
    grammar = """
    k_declaration =
    [
        Import.import
        | Module.module
        | Class.class
        | Implementation.implementation
    ]
    """