from cnorm.nodes import Signs, Qualifiers
S = Signs.map
Q = Qualifiers.rmap
#Sp = Specifiers.map

VARS = {
   'char':'c',
   'float':'f',
   'double':'d',
   'short':'s',
   'int':'i',
   'bool':'b',
   'long':'l',
   'long long':'x',
   'signed char':'Sc',
   'void': 'v'
}

def id_m(ident: str):
    return str(len(ident)) + ident

def type_m(typ: str, sign = S['SIGNED']):
  if typ not in VARS:
    #return typ #Activate for class support debug
    raise IndexError('Mangling type not recognised : %s' %typ)
  res = ''
  if sign == S['UNSIGNED']:
     res = 'U'
  res += VARS[typ]
  return res

def qual_m(qual: 'enum'):
    if qual >= len(Q):
        raise IndexError('Qualifier #%d Not known' %qual)
    return Q[qual][0].upper() + '_'
