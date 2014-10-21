from cnorm.nodes import Signs

S = Signs.map

"""
Method = 'method ident'  '__' 'qual' 'classident' 'params'

Primitive types:
int, long, short, char, long long = 'i', 'l', 's', 'c', 'x'
if unsigned = prefixed 'U'
signed char = 'Sc'
float, double = 'f', 'd'
bool = 'b'
wchar_t = 'w'

Simple ident:
class, template, identspace ident = 'len(ident)' 'ident'

Pointer = 'P' 'type mangling'
Reference = 'R' 'type mangling'

Qualified ident = 'Q' '# of parts in qualified ident'
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
   'bool':'b',
   'long':'l',
   'long long':'x',
   'signed char':'Sc'
}

QUAL = {
   'const':'C'
   }

def identifier(ident: str):
     return str(len(ident)) + ident

def var(ident: str, typ: str, qual: str, sign = S['SIGNED']):
  if typ not in VARS:
     raise IndexError('Mangling type not recognised')
  res = ''
  if sign == S['UNSIGNED']:
     res = 'U'
  res += VARS[typ] + Mangle.ident(ident)
  return res

def function(ident: str, scope: str = '', qual: str = '', params: list = None):
   return  '__' + qual + self.ident(ident) + ''.join(params)