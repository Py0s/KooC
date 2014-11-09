from cnorm.parsing.expression import Idset
from weakref import ref
from pyrser.grammar import Grammar
from cnorm.parsing.declaration import Declaration
from KoocGrammar.K_Declaration import K_Declaration
from cnorm import nodes
from pyrser import meta
from pyrser.parsing.node import Node
import knodes

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
            KoocCall.kooc_call :>_
            |
            kc_c_decl
            |
            kc_preproc_decl
            |
            kc_asm_decl
            |
            K_Declaration.k_declaration
        ]

        kc_preproc_decl = [
            ['#' preproc_directive ]:decl
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
                #echo("TODO : si je passe ici c quil y a un problem wesh")
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
            |
            KC_Expression.kc_unary_expression:>_
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

@meta.hook(KC_Declaration)
def check_asm(self, ident):
    ident_value = self.value(ident)
    if ident_value in Idset and Idset[ident_value] == "asm":
        return True
    return False


@meta.hook(KC_Declaration)
def check_quali(self, ident):
    ident_value = self.value(ident)
    if ident_value in Idset and Idset[ident_value] == "qualifier":
        return True
    return False


@meta.hook(KC_Declaration)
def check_asmattr(self, ident):
    ident_value = self.value(ident)
    if ((ident_value in Idset and (Idset[ident_value] == "asm"
         or Idset[ident_value] == "attribute"))):
        return True
    return False


@meta.hook(KC_Declaration)
def new_root(self, ast, current_block):
    type(ast)
    ast.set(knodes.KRootBlockStmt([]))
    current_block.ref = ast
    return True


@meta.rule(KC_Declaration, "preproc_directive")
def preproc_directive(self) -> bool:
    """Consume a preproc directive."""
    self._stream.save_context()
    if self.read_until("\n", '\\'):
        return self._stream.validate_context()
    return self._stream.restore_context()


@meta.hook(KC_Declaration)
def raw_decl(self, decl):
    decl.set(knodes.KRaw(self.value(decl)))
    return True


@meta.hook(KC_Declaration)
def create_ctype(self, lspec):
    lspec.ctype = None
    return True


@meta.hook(KC_Declaration)
def copy_ctype(self, lspec, previous):
    lspec.ctype = previous.ctype.copy()
    return True


@meta.hook(KC_Declaration)
def new_decl_spec(self, lspec, i, current_block):
    idsetval = ""
    i_value = self.value(i)
    if i_value in Idset:
        idsetval = Idset[i_value]
    # don't fuck with reserved keywords
    if idsetval == "reserved":
        return False
    # not for asm or attribute
    if idsetval != "" and idsetval[0] != 'a':
        lspec.ctype = knodes.makeKCType(i_value, lspec.ctype)
        return True
    if ((hasattr(current_block.ref, 'types')
         and i_value in current_block.ref.types)):
        if lspec.ctype is None:
            lspec.ctype = knodes.KPrimaryType(i_value)
        else:
            lspec.ctype._identifier = i_value
        lspec.ctype._identifier = i_value
        return True
    return False


@meta.hook(KC_Declaration)
def add_body(self, ast, body):
    ast.body = body
    return True


@meta.hook(KC_Declaration)
def end_decl(self, current_block, ast):
    current_block.ref.body.append(ast)
    if ((hasattr(ast, 'ctype') and ast._name != ""
         and ast.ctype._storage == nodes.Storages.TYPEDEF)):
        current_block.ref.types[ast._name] = ref(ast)
    return True


@meta.hook(KC_Declaration)
def not_empty(self, current_block, dsp, decl):
    # empty declspec only in global scope
    if type(current_block.ref) is knodes.KBlockStmt and self.value(dsp) == "":
        return False
    return True


@meta.hook(KC_Declaration)
def colon_expr(self, ast, expr):
    ast.colon_expr(expr)
    return True


@meta.hook(KC_Declaration)
def assign_expr(self, ast, expr):
    ast.assign_expr(expr)
    return True


@meta.hook(KC_Declaration)
def is_composed(self, lspec):
    if ((lspec.ctype._specifier == nodes.Specifiers.STRUCT
         or lspec.ctype._specifier == nodes.Specifiers.UNION)):
            return True
    return False


@meta.hook(KC_Declaration)
def is_enum(self, lspec):
    if lspec.ctype._specifier == nodes.Specifiers.ENUM:
        return True
    return False


@meta.hook(KC_Declaration)
def is_typeof(self, i):
    i_value = self.value(i)
    if i_value in Idset and Idset[i_value] == "typeof":
        return True
    return False


@meta.hook(KC_Declaration)
def add_typeof(self, lspec, tof):
    lspec.ctype = knodes.KPrimaryType("typeof" + self.value(tof))
    return True


@meta.hook(KC_Declaration)
def add_qual(self, lspec, qualspec):
    dspec = self.value(qualspec)
    if dspec in Idset and Idset[dspec] == "qualifier":
        cleantxt = dspec.strip("_")
        lspec.ctype.push(
            knodes.KQualType(knodes.KQualifiers.map[cleantxt.upper()])
        )
        return True
    return False


@meta.hook(KC_Declaration)
def add_attr_specifier(self, lspec, attrspec):
    if lspec.ctype is None:
        lspec.ctype = knodes.makeKCType('int', lspec.ctype)
    lspec.ctype.push(knodes.KAttrType(self.value(attrspec)))
    return True


@meta.hook(KC_Declaration)
def add_attr_composed(self, lspec, attrspec):
    if not hasattr(lspec.ctype, '_attr_composed'):
        lspec.ctype._attr_composed = []
    lspec.ctype._attr_composed.append(self.value(attrspec))
    return True


@meta.hook(KC_Declaration)
def add_attr_decl(self, lspec, attrspec):
    if not hasattr(lspec, '_attr_decl'):
        lspec._attr_decl = []
    lspec._attr_decl.append(self.value(attrspec))
    return True


@meta.hook(KC_Declaration)
def add_composed(self, lspec, n, block):
    ctype = knodes.KComposedType(self.value(n))
    if lspec.ctype is not None:
        ctype._storage = lspec.ctype._storage
        ctype._specifier = lspec.ctype._specifier
        if hasattr(lspec.ctype, '_attr_composed'):
            ctype._attr_composed = lspec.ctype._attr_composed
    lspec.ctype = ctype
    if hasattr(block, 'body'):
        lspec.ctype.fields = block.body
    return True


@meta.hook(KC_Declaration)
def add_enum(self, lspec, n, block):
    ctype = knodes.KComposedType(self.value(n))
    if lspec.ctype is not None:
        ctype._storage = lspec.ctype._storage
        ctype._specifier = lspec.ctype._specifier
    lspec.ctype = ctype
    if hasattr(block, 'list'):
        lspec.ctype.enums = block.list
    return True


@meta.hook(KC_Declaration)
def add_enumerator(self, ast, enum):
    if not hasattr(ast, 'list'):
        ast.list = []
    ast.list.append(enum)
    return True


@meta.hook(KC_Declaration)
def new_enumerator(self, ast, ident, constexpr):
    ast.set(knodes.KEnumerator(self.value(ident), constexpr))
    return True


@meta.hook(KC_Declaration)
def new_composed(self, ast, current_block):
    ast.set(knodes.KBlockStmt([]))
    current_block.ref = ast
    parent = self.rule_nodes.parents
    if 'current_block' in parent:
        current_block.ref.types = parent['current_block'].ref.types.new_child()
    return True


@meta.hook(KC_Declaration)
def first_pointer(self, lspec):
    if not hasattr(lspec, 'ctype') or lspec.ctype is None:
        lspec.ctype = knodes.makeKCType('int', lspec.ctype)
    lspec.ctype.push(knodes.KPointerType())
    return True


@meta.hook(KC_Declaration)
def commit_declarator(self, ast, lspec):
    if hasattr(lspec.ctype, '_params'):
        lspec.ctype.__class__ = knodes.KFuncType
    name = ""
    if hasattr(lspec, '_name'):
        name = lspec._name
    ast.set(knodes.KDecl(name, lspec.ctype))
    return True


@meta.hook(KC_Declaration)
def add_pointer(self, lspec):
    if not hasattr(lspec, 'ctype'):
        lspec.ctype = knodes.makeKCType('int', lspec.ctype)
    if not hasattr(lspec.ctype, 'push'):
        return False
    lspec.ctype.push(knodes.KPointerType())
    return True


@meta.hook(KC_Declaration)
def add_paren(self, lspec):
    if not hasattr(lspec, 'ctype') or lspec.ctype is None:
        lspec.ctype = knodes.makeKCType('int')
    paren = knodes.KParenType()
    if not hasattr(lspec, 'cur_paren'):
        lspec.cur_paren = []
        lspec.cur_paren.append(ref(lspec.ctype))
    last = lspec.cur_paren.pop()
    lspec.cur_paren.append(ref(paren))
    lspec.cur_paren.append(last)
    lspec.ctype.push(paren)
    return True


@meta.hook(KC_Declaration)
def add_ary(self, lspec, expr):
    if not hasattr(lspec, 'ctype') or lspec.ctype is None:
        lspec.ctype = knodes.makeKCType('int')
    if not hasattr(lspec, 'cur_paren'):
        lspec.cur_paren = []
        lspec.cur_paren.append(ref(lspec.ctype))
    lspec.cur_paren[-1]().push(knodes.KArrayType(expr))
    return True


@meta.hook(KC_Declaration)
def name_absdecl(self, ast, ident):
    ident_value = self.value(ident)
    if ident_value != "":
        ast._name = ident_value
        ast._could_be_fpointer = True
    return True


@meta.hook(KC_Declaration)
def close_paren(self, lspec):
    lspec.cur_paren.pop()
    return True


@meta.hook(KC_Declaration)
def open_params(self, lspec):
    if lspec.ctype is None:
        lspec.ctype = knodes.makeKCType('int')
    if not hasattr(lspec, 'cur_paren'):
        lspec.cur_paren = []
        lspec.cur_paren.append(ref(lspec.ctype))
    if not hasattr(lspec.cur_paren[-1](), '_params'):
        lspec.cur_paren[-1]()._params = []
    return True


@meta.hook(KC_Declaration)
def add_param(self, lspec, param):
    lspec.cur_paren[-1]()._params.append(param)
    return True


@meta.hook(KC_Declaration)
def add_ellipsis(self, lspec):
    lspec.cur_paren[-1]()._ellipsis = True
    return True


@meta.hook(KC_Declaration)
def new_blockinit(self, init_list):
    init_list.set(knodes.KBlockInit([]))
    return True


@meta.hook(KC_Declaration)
def new_blockexpr(self, ast, current_block):
    ast.set(knodes.KBlockExpr([]))
    current_block.ref = ast
    parent = self.rule_nodes.parents
    if 'current_block' in parent:
        current_block.ref.types = parent['current_block'].ref.types.new_child()
    return True


@meta.hook(KC_Declaration)
def add_init(self, ast, expr, designation):
    ast.body.append(expr)
    dvalue = self.value(designation)
    if dvalue != "":
        ast.body[-1].designation = dvalue
    return True


@meta.hook(KC_Declaration)
def for_decl_begin(self, current_block):
    current_block.ref = Node()
    current_block.ref.body = []
    # new to link this fake body to other block
    parent = self.rule_nodes.parents
    if 'current_block' in parent:
        current_block.ref.types = parent['current_block'].ref.types.new_child()
    return True


@meta.hook(KC_Declaration)
def for_decl_end(self, init, current_block):
    if len(current_block.ref.body) > 0:
        init.set(current_block.ref.body[0])
    return True


@meta.hook(KC_Declaration)
def to_cast(self, ast, typename):
    expr = Node()
    expr.set(ast)
    ast.set(knodes.KCast(knodes.KRaw('()'), [typename.ctype, expr]))
    return True


@meta.hook(KC_Declaration)
def sizeof(self, ident):
    ident_value = self.value(ident)
    if ident_value in Idset and Idset[ident_value] == "sizeof":
        return True
    return False


@meta.hook(KC_Declaration)
def new_sizeof(self, ast, i, n):
    thing = n
    if isinstance(thing, knodes.KDecl):
        thing = n.ctype
    ast.set(knodes.KSizeof(knodes.KRaw(self.value(i)), [thing]))
    return True


@meta.hook(KC_Declaration)
def new_builtoffset(self, ast, bof):
    ast.set(knodes.KRaw("__builtin_offsetof(" + self.value(bof) + ")"))
    return True
