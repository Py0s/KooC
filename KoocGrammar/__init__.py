
from pyrser.grammar import Grammar
from KoocGrammar.KC_Declaration import KC_Declaration

class KoocG(Grammar, KC_Declaration):
    entry = KC_Declaration.entry
