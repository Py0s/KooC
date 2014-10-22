
from pyrser.grammar import Grammar
from cnorm.parsing.statement import Statement
from KoocGrammar.K_Statement import K_Statement
from pyrser import meta

class KC_Statement(Grammar, Statement, K_Statement):
    entry = "expression_statement"
    grammar = """
            kc_statement = [ Statement.single_statement:>_ | K_Statement.k_statement:>_ ]
    """
