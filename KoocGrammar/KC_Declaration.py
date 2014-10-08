
from pyrser.grammar import Grammar
from cnorm.parsing.declaration import Declaration
from KoocGrammar.K_Declaration import K_Declaration
from cnorm import nodes

class KC_Declaration(Grammar, Declaration, K_Declaration):
    entry = "translation_unit"
    grammar = """
    	Declaration.declaration = [ kc_declaration ]

        kc_declaration = [
    	';' // garbage single comma
            |
            c_decl
            |
            preproc_decl
            |
            asm_decl
            |
            K_Declaration.k_declaration
    	]

        Declaration.unary_expression = [
            // CAST
            '(' type_name:t ')'
            [
                // simple cast
                unary_expression
                |
                // compound literal
                initializer_block
            ]:>_
            #to_cast(_, t)
            | // SIZEOF
            Base.id:i #sizeof(i)
            __scope__:n
            [
                '(' type_name:>n ')'
                | KC_Expression.unary_expression:>n
            ]
            #new_sizeof(_, i, n)
            | KC_Expression.unary_expression:>_
        ]


        Declaration.primary_expression = [
            "({"
                __scope__:current_block
                #new_blockexpr(_, current_block)
                [
                    line_of_code
                ]*
            "})"
            | // TODO: create special node for that
                "__builtin_offsetof"
                '(' [type_name ',' postfix_expression]:bof ')'
                #new_builtoffset(_, bof)
            |
            KC_Expression.primary_expression:>_
        ]

    """

        ## Declaration.line_of_code = [ kc_line_of_code ]

        ## kc_line_of_code = [
        ##             kc_declaration
        ##         |
        ##             KC_Statement.single_statement:line
        ##             #end_loc(current_block, line)
        ## ]

        ## Declaration.for_statement = [ KC_Declaration.kc_for_statement ]

        ## kc_for_statement = [
        ##     '('
        ##         __scope__:init
        ##         [
        ##             __scope__:current_block
        ##             #for_decl_begin(current_block)
        ##             kc_declaration
        ##             #for_decl_end(init, current_block)
        ##         |
        ##             KC_Statement.expression_statement:>init
        ##         ]
        ##         KC_Statement.expression_statement:cond
        ##         KC_Expression.expression?:inc
        ##     ')'
        ##     KC_Statement.single_statement:body
        ##     #new_for(_, init, cond, inc, body)
        ## ]
