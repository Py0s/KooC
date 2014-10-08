
from pyrser.grammar import Grammar
from cnorm.parsing.statement import Statement
from KoocGrammar.K_Statement import K_Statement
from pyrser import meta

class KC_Statement(Grammar, Statement, K_Statement):
    entry = "expression_statement"
    grammar = """
     expression_statement = [
        [KC_Expression.kc_expression:e #new_expr(_, e) #test1(_, e)]? #test(_, current_block)
        ';'
    ]

    kc_statement = [ Statement.single_statement:>_ | K_Statement.k_statement:>_ ]
    """

@meta.hook(KC_Statement)
def test(self, ast, block):
    print("ast Statment : ", ast)
    print("block Statment : ", block, "\n")
    return True

@meta.hook(KC_Statement)
def test1(self, ast, e):
    print("ast Statment : ", ast)
    print("e Statment : ", e, "\n")
    return True
