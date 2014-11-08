#!/usr/bin/env python3

from pyrser.grammar import Grammar
from pyrser import meta
from KoocGrammar.Kooc_call import Kooc_call

class	K_Expression(Grammar, Kooc_call):
        entry = 'k_expression'
        grammar = """
        k_primary_expression = [ Kooc_call.kooc_call:>_ ]
        """