
from pyrser.grammar import Grammar
from cnorm.parsing.expression import Expression
from KoocGrammar.K_Expression import K_Expression
from pyrser import meta
from pyrser.parsing.node import Node
import knodes

# class KC_Expression(Grammar, Expression, K_Expression):
#     entry = "unary_expression"
#     grammar = """
#    §     kc_expression = [ Expression.expression:>_ ]
#    §     kc_assignement_expression = [ Expression.assignement_expression:>_ ]
#    §     unary_expression = [ Expression.unary_expression:>_ ]
#   §      primary_expression = [
#   §          '(' expression:expr ')' #new_paren(_, expr)
#   §          | [ Literal.literal | identifier | kc_primary_expression]:>_
#    §     ]
#    §     kc_primary_expression = [ K_Expression.k_primary_expression:>_ ]

#     """


class KC_Expression(Grammar, Expression, K_Expression):
    """
        interaction with other CNORM PART:

    """
    entry = "kc_expression"
    grammar = """

        /*
            Comment works as in C/C++
        */

        kc_dummy_with_brace = [ @ignore('null')
            [
            '{' kc_dummy_with_brace* '}'
            | Base.string
            | Base.char
            | Base.read_char:c #check_not_brace(c)
            ]
        ]

        kc_dummy_with_paren = [ @ignore('null')
            [
            '(' kc_dummy_with_paren* ')'
            | Base.string
            | Base.char
            | Base.read_char:c #check_not_paren(c)
            ]
        ]

        kc_expression = [
            kc_assignement_expression:>_
            [
                ',':op #new_raw(op, op)
                kc_assignement_expression:param
                #new_binary(_, op, param)
            ]*
        ]

        kc_assign_op = [
            @ignore('null')
            [
                '=' !'='
                | "+="
                | "-"
                | "*="
                | "/="
                | "%="
                | "<<="
                | ">>="
                | "&="
                | "^="
                | "|="
            ]:op
            #new_raw(_, op)
        ]
        kc_assignement_expression = [
            kc_conditional_expression:>_
            [
                kc_assign_op:op
                kc_assignement_expression:param
                #new_binary(_, op, param)
            ]*
        ]

        kc_constant_expression = [ kc_conditional_expression:>_ ]

        kc_conditional_expression = [
            kc_logical_or_expression:>_
            [
                '?'
                kc_expression?:then
                ':'
                kc_assignement_expression?:else
                #new_ternary(_, then, else)
            ]?
        ]

        kc_logical_or_op = [ @ignore('null') ["||"]:op #new_raw(_, op) ]
        kc_logical_or_expression = [
            kc_logical_and_expression:>_
            [
                kc_logical_or_op:op
                kc_logical_and_expression:param
                #new_binary(_, op, param)
            ]*
        ]

        kc_logical_and_op = [ @ignore('null') ["&&"]:op #new_raw(_, op) ]
        kc_logical_and_expression = [
            kc_or_expression:>_
            [
                kc_logical_and_op:op
                kc_or_expression:param
                #new_binary(_, op, param)
            ]*
        ]

        kc_or_op = [ @ignore('null') ["|" !["|"|"="]]:op #new_raw(_, op) ]
        kc_or_expression = [
            kc_xor_expression:>_
            [
                kc_or_op:op
                kc_xor_expression:param
                #new_binary(_, op, param)
            ]*
        ]

        kc_xor_op = [ @ignore('null') ["^" !"="]:op #new_raw(_, op) ]
        kc_xor_expression = [
            kc_and_expression:>_
            [
                kc_xor_op:op
                kc_and_expression:param
                #new_binary(_, op, param)
            ]*
        ]

        kc_and_op = [ @ignore('null') ["&" !["&"|"="]]:op #new_raw(_, op) ]
        kc_and_expression = [
            kc_equality_expression:>_
            [
                kc_and_op:op
                kc_equality_expression:param
                #new_binary(_, op, param)
            ]*
        ]

        kc_eqneq_op = [ @ignore('null') ["==" | "!="]:op #new_raw(_, op) ]
        kc_equality_expression = [
            kc_relational_expression:>_
            [
                kc_eqneq_op:op
                kc_relational_expression:param
                #new_binary(_, op, param)
            ]*
        ]

        kc_cmp_op = [
            @ignore('null')
            [
                "<="
                | ">="
                | '<' !'<'
                | '>' !'>'
            ]:op
            #new_raw(_, op)
        ]
        kc_relational_expression = [
            kc_shift_expression:>_
            [
                kc_cmp_op:op
                kc_shift_expression:param
                #new_binary(_, op, param)
            ]*
        ]

        kc_shift_op = [
            @ignore('null')
            [
                "<<" !"="
                | ">>" !"="
            ]:op
            #new_raw(_, op)
        ]
        kc_shift_expression = [
            kc_additive_expression:>_
            [
                kc_shift_op:op
                kc_additive_expression:param
                #new_binary(_, op, param)
            ]*
        ]

        kc_add_op = [
            @ignore('null')
            [
                '+' !['+'|'=']
                | '-' !['-'|'='|'>']
            ]:op
            #new_raw(_, op)
        ]
        kc_additive_expression = [
            kc_multiplicative_expression:>_
            [
                kc_add_op:op
                kc_multiplicative_expression:param
                #new_binary(_, op, param)
            ]*
        ]

        kc_mul_op = [ @ignore('null') [['*'|'/'|'%']:op !'='] #new_raw(_, op) ]
        kc_multiplicative_expression = [
            kc_unary_expression:>_
            [
                kc_mul_op:op
                kc_unary_expression:param
                #new_binary(_, op, param)
            ]*
        ]

        kc_unary_op = [ @ignore('null')
            ["++"
            |"--"
            |"&&"
            | '&' !'='
            | '*' !'='
            | '~' !'='
            | '!' !'='
            | '+' !'='
            | '-' !['>'|'=']
            ]:op #new_raw(_, op)
        ]
        kc_unary_expression =
        [
                kc_postfix_expression:>_
            |
                __scope__:op
                [   kc_unary_op:>op
                |   Base.id:i
                    #is_raw(op, i)
                ]
                kc_unary_expression:expr
                #new_unary(_, op, expr)
        ]

        kc_postfix_expression = [
            #echo("heho")
            kc_primary_expression:>_
            [
            #echo("je suis un connard")
                __scope__:pres
                [
                '[' kc_expression:expr ']' #new_array_call(pres, _, expr)
                | '(' kc_func_arg_list?:args ')' #new_func_call(pres, _, args)
                | '.' kc_identifier:i #new_dot(pres, _, i)
                | "->" kc_identifier:i #new_arrow(pres, _, i)
                | ["++"|"--"]:op #new_raw(op, op) #new_post(pres, op, _)
                ]
                #bind('_', pres)
            ]*
        ]

        kc_func_arg_list = [
            kc_assignement_expression:a #new_arg(_, a)
            [   ','
                kc_assignement_expression:a #new_arg(_, a)
            ]*
        ]

        kc_primary_expression = [
            [ K_Expression.k_primary_expression | Literal.literal | kc_identifier ]:>_
            |
            '(' kc_expression:expr ')' #new_paren(_, expr)
        ]

        kc_identifier = [
            @ignore('null')
            [
                kc_rootidentifier:id
                #check_is_id(id)
                #new_id(_, id)
            ]
        ]

        kc_rootidentifier = [ Base.id ]

        /////// OVERLOADS ///////
        K_Expression.assmt_expr_overide = [ KC_Expression.kc_assignement_expression:>_ ]

    """

@meta.hook(KC_Expression)
def new_ternary(self, ast, then_expr, else_expr):
    cond = Node()
    cond.set(ast)
    ast.set(knodes.KTernary([], [cond, then_expr, else_expr]))
    return True


@meta.hook(KC_Expression)
def new_binary(self, ast, op, param):
    left = Node()
    left.set(ast)
    ast.set(knodes.KBinary(op, [left, param]))
    return True


@meta.hook(KC_Expression)
def is_raw(self, op, ident):
    ident_value = self.value(ident)
    if ident_value in Idset and Idset[ident_value] == "unary":
        op.set(knodes.KRaw(ident_value + " "))
        return True
    return False


@meta.hook(KC_Expression)
def new_unary(self, ast, op, param):
    opu = Node()
    opu.set(op)
    p = Node()
    p.set(param)
    ast.set(knodes.KUnary(opu, [p]))
    return True


@meta.hook(KC_Expression)
def new_paren(self, ast, expr):
    ast.set(knodes.KParen("()", [expr]))
    return True


@meta.hook(KC_Expression)
def new_post(self, ast, op, param):
    ast.set(knodes.KPost(op, [param]))
    return True


@meta.hook(KC_Expression)
def new_arg(self, ast, arg):
    if not hasattr(ast, 'list'):
        ast.list = []
    ast.list.append(arg)
    return True


@meta.hook(KC_Expression)
def new_array_call(self, ast, call, index):
    ast.set(knodes.KArray(call, [index]))
    return True


@meta.hook(KC_Expression)
def new_dot(self, ast, call, field):
    ast.set(knodes.KDot(call, [field]))
    return True


@meta.hook(KC_Expression)
def new_arrow(self, ast, call, field):
    ast.set(knodes.KArrow(call, [field]))
    return True


@meta.hook(KC_Expression)
def new_func_call(self, ast, call, args):
    if hasattr(args, 'list'):
        ast.set(knodes.KFunc(call, args.list))
    else:
        ast.set(knodes.KFunc(call, []))
    return True


@meta.hook(KC_Expression)
def new_raw(self, ast, data):
    ast.set(knodes.KRaw(self.value(data)))
    return True


@meta.hook(KC_Expression)
def new_id(self, ast, identifier):
    ast.set(knodes.KId(self.value(identifier)))
    return True


@meta.hook(KC_Expression)
def check_not_brace(self, c):
    c_value = self.value(c)
    return c_value != "{" and c_value != "}" \
        and c_value != "'" and c_value != '"'


@meta.hook(KC_Expression)
def check_not_paren(self, c):
    c_value = self.value(c)
    return c_value != "(" and c_value != ")" \
        and c_value != "'" and c_value != '"'


@meta.hook(KC_Expression)
def check_is_id(self, identifier):
    return self.value(identifier) not in Idset
