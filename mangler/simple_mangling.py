from cnorm.nodes import Signs, Qualifiers
S = Signs.map
Q = Qualifiers.map
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
   'void': 'v' #should not be here
}

def id_m(ident: str):
    return str(len(ident)) + ident

def type_m(typ: str, sign = S['SIGNED']):
  if typ not in VARS:
    return typ
    # raise IndexError('Mangling type not recognised : %s' %typ)
  res = ''
  if sign == S['UNSIGNED']:
     res = 'U'
  res += VARS[typ]
  return res

def qual_m(qual: str):
    if len(qual) == 0:
        return ''
    if qual.upper() not in Q:
        print('Warning: should not be unknown')
        return ''
    return qual[0].upper() + '_'
