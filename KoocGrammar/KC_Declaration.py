
from pyrser.grammar import Grammar
from cnorm.parsing.declaration import Declaration
from KoocGrammar.K_Declaration import K_Declaration
from cnorm import nodes

## class KC_Declaration(Grammar, Declaration, K_Declaration):
##     entry = "translation_unit"
##     grammar = """
##     	Declaration.declaration = [ kc_declaration ]

##         kc_declaration = [
##     	';' // garbage single comma
##             |
##             c_decl
##             |
##             preproc_decl
##             |
##             asm_decl
##             |
##             K_Declaration.k_declaration
##     	]

##         Declaration.unary_expression = [
##             // CAST
##             '(' type_name:t ')'
##             [
##                 // simple cast
##                 unary_expression
##                 |
##                 // compound literal
##                 initializer_block
##             ]:>_
##             #to_cast(_, t)
##             | // SIZEOF
##             Base.id:i #sizeof(i)
##             __scope__:n
##             [
##                 '(' type_name:>n ')'
##                 | KC_Expression.unary_expression:>n
##             ]
##             #new_sizeof(_, i, n)
##             | KC_Expression.unary_expression:>_
##         ]


##         Declaration.primary_expression = [
##             "({"
##                 __scope__:current_block
##                 #new_blockexpr(_, current_block)
##                 [
##                     line_of_code
##                 ]*
##             "})"
##             | // TODO: create special node for that
##                 "__builtin_offsetof"
##                 '(' [type_name ',' postfix_expression]:bof ')'
##                 #new_builtoffset(_, bof)
##             |
##             KC_Expression.primary_expression:>_
##         ]

##     """

##         ## Declaration.line_of_code = [ kc_line_of_code ]

##         ## kc_line_of_code = [
##         ##             kc_declaration
##         ##         |
##         ##             KC_Statement.single_statement:line
##         ##             #end_loc(current_block, line)
##         ## ]

##         ## Declaration.for_statement = [ KC_Declaration.kc_for_statement ]

##         ## kc_for_statement = [
##         ##     '('
##         ##         __scope__:init
##         ##         [
##         ##             __scope__:current_block
##         ##             #for_decl_begin(current_block)
##         ##             kc_declaration
##         ##             #for_decl_end(init, current_block)
##         ##         |
##         ##             KC_Statement.expression_statement:>init
##         ##         ]
##         ##         KC_Statement.expression_statement:cond
##         ##         KC_Expression.expression?:inc
##         ##     ')'
##         ##     KC_Statement.single_statement:body
##         ##     #new_for(_, init, cond, inc, body)
##         ## ]

class KC_Declaration(Grammar, Declaration, K_Declaration):	
    """
        interaction with other CNORM PART:
    """
    #: entry point for C programming language
    entry = "kc_translation_unit"

    #: complete C declaration grammar
    grammar = """

        kc_translation_unit = [
            @ignore("C/C++")
            [
                __scope__:current_block
                #new_root(_, current_block)
                [
                    kc_declaration
                ]*
            ]
            Base.eof
        ]

        kc_declaration = [
            ';' // garbage single comma
            |
            kc_c_decl
            |
            kc_preproc_decl
            |
            kc_asm_decl
        ]

        kc_preproc_decl = [
            ['#' kc_preproc_directive ]:decl
            #raw_decl(decl)
            #end_decl(current_block, decl)
        ]

        kc_asm_decl = [
            [
            Base.id:i
            #check_asm(i)
            [
                Base.id:i
                #check_quali(i)
            ]?
            kc_attr_asm_decl_follow
            ';'?
            ]:decl
            #raw_decl(decl)
            #end_decl(current_block, decl)
        ]

        kc_attr_asm_decl = [
            [
                Base.id:i
                #check_asmattr(i)
                kc_attr_asm_decl_follow
            ]
        ]

        kc_attr_asm_decl_follow = [
            '(' kc_dummy_with_paren* ')'
            | '{' kc_dummy_with_brace* '}'
            | '__extension__'
        ]

        kc_c_decl = [
            __scope__:local_specifier
            #create_ctype(local_specifier)
            kc_declaration_specifier*:dsp
            kc_init_declarator:decl
            #not_empty(current_block, dsp, decl)
            #end_decl(current_block, decl)
            [
                ','
                #copy_ctype(local_specifier, decl)
                kc_init_declarator:decl
                #end_decl(current_block, decl)
            ]*
            [
                ';'
                |
                KC_Statement.kc_compound_statement:b
                #add_body(decl, b)
            ]
        ]

        kc_declaration_specifier = [
            Base.id:i
            #new_decl_spec(local_specifier, i, current_block)
            [
                #is_composed(local_specifier)
                kc_composed_type_specifier
                |
                #is_enum(local_specifier)
                kc_enum_specifier
                |
                #is_typeof(i)
                kc_typeof_expr
            ]?
            |
            kc_attr_asm_decl:attr
            #add_attr_specifier(local_specifier, attr)
        ]

        kc_type_qualifier = [
            Base.id:i
            #add_qual(local_specifier, i)
            |
            kc_attr_asm_decl:attr
            #add_attr_specifier(local_specifier, attr)
        ]

        kc_name_of_composed_type = [ Base.id ]
        kc_composed_type_specifier = [
            [
                kc_attr_asm_decl:attr
                #add_attr_composed(local_specifier, attr)
            ]?
            kc_name_of_composed_type?:n
            kc_composed_fields?:body
            #add_composed(local_specifier, n, body)
        ]

        kc_composed_fields = [
            '{'
                __scope__:current_block
                #new_composed(_, current_block)
                kc_declaration*
            '}'
        ]

        kc_enum_name = [ Base.id ]
        kc_enum_specifier = [
            kc_enum_name?:n
            kc_enumerator_list?:body
            #add_enum(local_specifier, n, body)
        ]

        kc_enumerator_list = [
            '{'
                kc_enumerator:e
                #add_enumerator(_, e)
                [
                    ',' kc_enumerator:e
                    #add_enumerator(_, e)
                ]*
                ','? // trailing comma
            '}'
        ]

        kc_enumerator = [
            kc_identifier:i
            __scope__:c
            ['=' kc_constant_expression:>c]?
            #new_enumerator(_, i, c)
        ]

        kc_typeof_expr = [
            // TODO: split inside typeof
            ['('
                [
                    kc_type_name !!')'
                    | kc_expression
                ]
            ')']:tof
            #add_typeof(local_specifier, tof)
        ]

        kc_init_declarator = [
            kc_declarator:>_
            [
                ':'
                kc_constant_expression:cexpr
                #colon_expr(_, cexpr)
            ]?
            [
                kc_attr_asm_decl:attr
                #add_attr_decl(_, attr)
            ]*
            [
                '='
                kc_initializer:aexpr
                #assign_expr(_, aexpr)
            ]?
            !![','|';'|'{']
        ]

        kc_declarator = [
            [
                "*"
                #first_pointer(local_specifier)
                kc_declarator_recurs:>_
                |
                kc_absolute_declarator:>_
            ]
            #commit_declarator(_, local_specifier)
        ]

        kc_declarator_recurs = [
            kc_pointer kc_absolute_declarator:>_
        ]

        kc_pointer = [
            [
                "*" #add_pointer(local_specifier)
                | kc_type_qualifier
            ]*
        ]

        kc_f_or_v_id = [ kc_identifier ]
        kc_absolute_declarator = [
                [
                    '('
                        #add_paren(local_specifier)
                        kc_type_qualifier?
                        kc_declarator_recurs:>_
                        #close_paren(local_specifier)
                    ')'
                    |
                    kc_f_or_v_id?:name
                    #name_absdecl(local_specifier, name)
                ]
                kc_direct_absolute_declarator?
        ]

        kc_direct_absolute_declarator = [
            [
                '['
                    // TODO: handle c99 qual for trees
                    "static"?
                    ["const"|"volatile"]?
                    "static"?
                    __scope__:expr
                    [
                        kc_assignement_expression:>expr
                        | '*':star #new_raw(expr, star)
                    ]?
                    #add_ary(local_specifier, expr)
                ']'
            ]+
            |
                '('
                #open_params(local_specifier)
                [
                    //kc_kr_parameter_type_list
                    //|
                    kc_parameter_type_list
                ]?
                ')'
            /*
            [ // K&R STYLE
                !![';'|','|'{'|'('|')']
                | kc_declaration*
            ]
            */
        ]

        kc_kr_parameter_type_list = [
            kc_identifier [',' kc_identifier]* !!')'
        ]

        kc_parameter_type_list = [
            [kc_type_name ';']*
            [
                kc_parameter_list
            ]?
            ','?
            ["..." #add_ellipsis(local_specifier)]?
        ]

        kc_parameter_list = [
            kc_parameter_declaration:p
            #add_param(local_specifier, p)
            [','
                kc_parameter_declaration:p
                #add_param(local_specifier, p)
            ]*
        ]

        kc_parameter_declaration = [ kc_type_name:>_ ]

        kc_initializer = [ [ kc_initializer_block | kc_assignement_expression ]:>_ ]

        kc_initializer_block = [
            '{'
                __scope__:init_list
                #new_blockinit(init_list)
                [kc_initializer_list]?
                ','? // trailing comma
                #bind('_', init_list)
            '}'
        ]

        kc_initializer_list = [
            kc_designation?:dsign
            kc_initializer:init
            #add_init(init_list, init, dsign)
            [
                ','
                kc_designation?:dsign
                kc_initializer:init
                #add_init(init_list, init, dsign)
            ]*
        ]

        kc_designation = [
            kc_designation_list+ '='?
            | kc_identifier ':'
        ]

        kc_designation_list = [
            '['
                kc_range_expression
            ']'
            | dot kc_identifier
        ]

        kc_type_name = [
            __scope__:local_specifier
            #create_ctype(local_specifier)
            kc_declaration_specifier+ kc_declarator:>_
        ]

        ///////// OVERLOAD OF STATEMENT
        // add declaration in block
        kc_line_of_code = [
                    kc_declaration
                |
                    kc_single_statement:line
                    #end_loc(current_block, line)
        ]

        kc_for_statement = [
            '('
                __scope__:init
                [
                    __scope__:current_block
                    #for_decl_begin(current_block)
                    kc_declaration
                    #for_decl_end(init, current_block)
                |
                    kc_expression_statement:>init
                ]
                kc_expression_statement:cond
                kc_expression?:inc
            ')'
            kc_single_statement:body
            #new_for(_, init, cond, inc, body)
        ]

        ///////// OVERLOAD OF EXPRESSION
        // add cast / sizeof
        kc_unary_expression = [
            // CAST
            '(' kc_type_name:t ')'
            [
                // simple cast
                kc_unary_expression
                |
                // compound literal
                kc_initializer_block
            ]:>_
            #to_cast(_, t)
            | // SIZEOF
            Base.id:i #sizeof(i)
            __scope__:n
            [
                '(' kc_type_name:>n ')'
                | KC_Expression.unary_expression:>n
            ]
            #new_sizeof(_, i, n)
            | KC_Expression.unary_expression:>_
        ]

        // ({}) and __builtin_offsetof
        kc_primary_expression = [
            "({"
                __scope__:current_block
                #new_blockexpr(_, current_block)
                [
                    kc_line_of_code
                ]*
            "})"
            | // TODO: create special node for that
                "__builtin_offsetof"
                '(' [kc_type_name ',' kc_postfix_expression]:bof ')'
                #new_builtoffset(_, bof)
            |
            
            KC_Expression.kc_primary_expression:>_
        ]

    """
