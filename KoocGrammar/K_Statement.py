
from pyrser.grammar import Grammar
from KoocGrammar.KC_Expression import KC_Expression

class K_Statement(Grammar, KC_Expression):
    entry = "k_statement"
    grammar = """
    k_statement = [ KC_Expression.kc_expression:>_ ]
    """
