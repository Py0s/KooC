from cnorm.nodes import Signs

S = Signs.map

"""
Method = 'method name'  '__' 'qual' 'classname' 'params'

Primitive types:
int, long, short, char, long long = 'i', 'l', 's', 'c', 'x'
if unsigned = prefixed 'U'
signed char = 'Sc'
float, double = 'f', 'd'
bool = 'b'
wchar_t = 'w'

Simple Name:
class, package, template, namespace name = 'len(name)' 'name'

Pointer = 'P' 'type mangling'
Reference = 'R' 'type mangling'

Qualified Name = 'Q' '# of parts in qualified name'
if 9 or less: No delimiters
Else: '_' before and after count

Foo::bar(int, long) const is mangled as `bar__C3Fooil

TODO:
Unicode support
http://www.ofb.net/gnu/gcc/gxxint_15.html
"""

VARS = {
        'char':'c',
        'short':'s',
        'int':'i',
        'long':'l',
        'long long':'x'
        }

class Mangle:

    def __init__(self):
        pass

    # def Function(name, qual = "", namespace = "", params: list):
    #   return name + '__' + qual + namename + "".join(params)

    # def Name(name: str) -> 'return mangled name':
    #     return '_' + 'Z'

    # def Type(name: str):

    #     return name

    def var(name: str, typ: str, sign = S['AUTO']: 'enum'):
        res = ''
        if sign == S['SIGNED'] and typ == 'char':
            res = 'S'
        else if sign == S['UNSIGNED']
            res = 'U'
        res += VARS[typ] + str(len(name)) + name
        return res