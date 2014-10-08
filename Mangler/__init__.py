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
class, template, namespace name = 'len(name)' 'name'

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
   'signed char':'Sc',
   'short':'s',
   'int':'i',
   'bool':'b',
   'long':'l',
   'long long':'x'
}

QUAL = {
   'const'
}

class Mangle:

   def name(name: str):
         return str(len(name)) + name

   def var(name: str, typ: str, sign = S['SIGNED']):
      if typ not in VARS:
         raise IndexError('Mangling type not recognised')
      res = ''
      if sign == S['UNSIGNED']:
         res = 'U'
      res += VARS[typ] + Mangle.name(name)
      return res

   def function(func_name: str, scope: str = '', qual: str = '', params: list = None):
       return self.name(func_name) + '__' + qual + Mangle.name(scope) + "".join(params)