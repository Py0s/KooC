
from pyrser.grammar import Grammar
from cnorm.parsing.expression import Expression
from KoocGrammar.K_Expression import K_Expression

class KC_Expression(Grammar, Expression, K_Expression):
    entry = "unary_expression"
    grammar = """
        kc_expression = [ Expression.expression:>_ ]
        kc_assignement_expression = [ Expression.assignement_expression:>_ ]
        unary_expression = [ Expression.unary_expression:>_ ]
        primary_expression = [
            '(' expression:expr ')' #new_paren(_, expr)
            | [ Literal.literal | identifier | kc_primary_expression]:>_
        ]
        kc_primary_expression = [ K_Expression.k_primary_expression:>_ ]

        K_Expression.assmt_expr_overide = [ KC_Expression.kc_assignement_expression:>_ ]
    """
