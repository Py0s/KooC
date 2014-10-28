
from pyrser.grammar import Grammar
from cnorm.parsing.statement import Statement
from KoocGrammar.K_Statement import K_Statement
from pyrser import meta

# class KC_Statement(Grammar, Statement, K_Statement):
#     entry = "expression_statement"
#     grammar = """
#     kc_statement = [ Statement.single_statement:>_ ]
#     """

class KC_Statement(Grammar, Statement, K_Statement):
    """
        interaction with other CNORM PART:

        Declaration.init_declarator -> kc_compound_statement
        Expression.primary_expression -> block_item_listC_Sta
    """
    entry = "kc_single_statement"
    grammar = """

        /*
            Comment works as in C/C++
        */

        kc_single_statement = [
            [kc_compound_statement
            | kc_labeled_statement
            | kc_expression_statement
            ]:>_
        ]

        kc_compound_statement = [
            [
            '{'
                __scope__:current_block
                #new_blockstmt(_, current_block)
                [
                    kc_line_of_code
                ]*
            '}'
            ]
        ]

        kc_line_of_code = [
            kc_single_statement:line
            #end_loc(current_block, line)
        ]

        kc_labeled_statement = [
            KC_Expression.kc_rootidentifier:ident
            [ #check_stmt(ident, "if") kc_if_statement:>_
            | #check_stmt(ident, "for") kc_for_statement:>_
            | #check_stmt(ident, "while") kc_while_statement:>_
            | #check_stmt(ident, "switch") kc_switch_statement:>_
            | #check_stmt(ident, "do") kc_do_statement:>_
            | #check_stmt(ident, "return") kc_return_statement:>_
            | #check_stmt(ident, "goto") kc_goto_statement:>_
            | #check_stmt(ident, "case") kc_case_statement:>_
            | #check_stmt(ident, "break") ';' #new_break(_)
            | #check_stmt(ident, "continue") ';' #new_continue(_)
            | ':' #new_label(_, ident)
            ]
        ]

        kc_if_statement = [
            '(' kc_expression:cond ')'
            kc_single_statement:then
            __scope__:else
            [
                "else"
                kc_single_statement:>else
            ]?
            #new_if(_, cond, then, else)
        ]

        kc_for_statement = [
            '('
                kc_expression_statement:init
                kc_expression_statement:cond
                kc_expression?:inc
            ')'
            kc_single_statement:body
            #new_for(_, init, cond, inc, body)
        ]

        kc_while_statement = [
            '('
                kc_expression:cond
            ')'
            kc_single_statement:body
            #new_while(_, cond, body)
        ]

        kc_switch_statement = [
            '(' kc_expression:cond ')'
            kc_single_statement:body
            #new_switch(_, cond, body)
        ]

        kc_do_statement = [
            kc_single_statement:body
            "while" '(' kc_expression:cond ')' ';'
            #new_do(_, cond, body)
        ]

        kc_return_statement = [
            kc_expression?:e ';'
            #new_return(_, e)
        ]

        kc_goto_statement = [
            kc_expression:e ';'
            #new_goto(_, e)
        ]

        kc_range_expression = [
            kc_constant_expression:>_
            [
                "..."
                kc_constant_expression:r
                #new_range(_, r)
            ]?
        ]

        kc_case_statement = [
            kc_range_expression:e #new_case(_, e)
            ':'
        ]

        kc_expression_statement = [
            [kc_expression:e #new_expr(_, e)]?
            ';'
        ]

    """
