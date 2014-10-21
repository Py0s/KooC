from cnorm.nodes import Signs
S = Signs.map

VARS = {
   'char':'c',
   'short':'s',
   'int':'i',
   'bool':'b',
   'long':'l',
   'long long':'x',
   'signed char':'Sc'
}

def id_m(ident: str):
    return str(len(ident)) + ident

def type_m(typ: str, sign = S['SIGNED']):
  if typ not in VARS:
     raise IndexError('Mangling type not recognised')
  res = ''
  if sign == S['UNSIGNED']:
     res = 'U'
  res += VARS[typ]
  return res

def qual_m(qual: str):
  if qual == '':
    raise IndexError('Qual size should not be empty')
  return qual[0].upper() + '_'