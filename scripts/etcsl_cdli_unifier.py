# Usage: python3 etcsl_cdli_unifier.py INPUT_ETCSL_FILE

import re
import os
import sys

INPUT_FILE = sys.argv[1]

def is_int(char):
  try:
    int(char)
    return True
  except ValueError:
    return False

class transliteration:

  re_extra_sign = re.compile(r'(( |-|)<<.+>>( |-|))')
  re_extra = re.compile('(\[|\]|\{\?\}|\{\!\}|\\\|/|<|>)')
    
  re_x_index = re.compile(r'(?P<a>[\w])x')
  re_x_sign = re.compile(r'(ₓ\(.+\))')
  re_brc = re.compile(r'(\(.+\))')
  re_source = re.compile(r'(?P<a>.+)(?P<b>\(source:)(?P<c>[^)]+)(?P<d>\))')
  re_index = re.compile(r'(?P<sign>[^\d]+)(?P<index>\d+)')
  re_brc_div = re.compile(r'(?P<a>\([^\)]+)(?P<b>-+)(?P<c>[^\(]+\))')

  vow_lst = ['a', 'A', 'e', 'E', 'i', 'I', 'u', 'U']
  re_last_vow = re.compile(r'(%s)' %('|'.join(vow_lst)))
  re_times = re.compile(r'(?P<a>[\w])x(?P<b>[\w])')

  def __init__(self, translit):
    self.raw_translit = translit
    translit = self.preporcess_translit(translit)
    self.check_defective(translit, 'pre')
    if self.defective==True:
      self.normalization = 'X'
      return None
    self.sign_list = self.get_sign_lst(translit)
    self.check_defective(translit, 'post')
    if self.defective==True:
      self.normalization = 'X'
      return None
    self.get_unicode_index_all()
    self.set_normalizations()
    
  def preporcess_translit(self, translit):
    translit = translit.strip(' ')
    translit = translit.replace('source: ', 'source:')
    if '<<' in translit:
      translit = self.re_extra_sign.sub('', translit)
    translit = self.re_extra.sub('', translit)
    translit = self.standardize_translit(translit)
    translit = self.remove_determinatives(translit)
    self.base_translit = translit
    return translit

  def check_defective(self, translit, step):
    self.defective = False
    if step=="pre":
      if ' ' in translit:
        self.defective = True
      for expt in ['_', '...', 'line', '(X', 'X)', '.X',
                   ' X', 'Xbr','-X', 'ṭ', 'ṣ', 'missing']:
        if expt in translit or expt.lower() in translit.lower():
          self.defective = True
      if translit.lower()!=translit:
        pass
        # ! PROBLEMATIC: TOO MANY SIGNS IGNORED
        # ! CHANGE THIS
  ##      self.defective = True
    elif step=="post":
      for el in self.sign_list:
        if 'x' in el['value'].lower() and '×' not in el['value'].lower():
          self.defective = True
        if '(' in el['value']:
          pass
          print([self.raw_translit, self.base_translit, el['value'],
                 self.sign_list])

  def get_sign_lst(self, translit):
    signs_lst = []
    if self.re_brc_div.search(translit):
      translit = self.re_brc_div.sub(lambda m: m.group().replace('-',"="),
                                translit)    
    for sign_str in list(filter(lambda x: x!='', translit.split('-'))):
      signs_lst.append(self.parse_sign(sign_str))
    return signs_lst

  def parse_sign(self, sign):
    index = ''
    emendation = ''
    value_of = ''
    if self.re_x_index.search(sign):
      sign = self.re_x_index.sub('\g<a>ₓ', sign)
    if 'ₓ(' in sign.lower():
      index='x'
      value_of = self.re_x_sign.search(sign).group().strip('ₓ()')\
                 .replace('=',"-")
      sign = self.re_x_sign.sub('', sign)
    if self.re_brc.search(sign):
      if sign[0]=='(' and sign[-1]==')':
        sign = sign.strip('()')
      else:
        value_of = self.re_brc.search(sign).group().strip('()')\
                   .replace('=',"-")
        sign = self.re_brc.sub('', sign)
    if 'x' in sign.lower() and len(sign)>1:
      pass
    if self.re_source.search(sign):
      emendation = self.re_source.sub(r'\g<c>', sign).replace('=',"-")
      sign = self.re_source.sub(r'\g<a>', sign)
    if self.re_index.search(sign):
      i = 0
      for x in self.re_index.finditer(sign):
        if i==0:
          index = x.groupdict()['index']
          sign = x.groupdict()['sign']
        else:
          pass
          # CHECK FOR POSSIBLE ERRORS
          #print(self.raw_translit, sign, i, x.groupdict()['sign'], x.groupdict()['index'])
        i+=1
    return {'value': sign,
            'index': index,
            'emendation': emendation,
            'value_of': value_of}

  def set_normalizations(self, placeholders=True):
    s_lst = self.sign_list
    norm_flat_lst = [s['value'] for s in s_lst]
    norm_unicode_lst = [s['u_sign'] for s in s_lst]
    if placeholders==True:
      s_lst = self.get_placeholders_lst()
      norm_flat_lst = [s for s in s_lst]
    self.normalization = ''
    self.normalization_u = ''
    i = 0
    while i < len(norm_flat_lst):
      if self.normalization:
        if self.normalization[-1]==norm_flat_lst[i][0]:
          self.normalization+=norm_flat_lst[i][1:]
          self.normalization_u+=norm_unicode_lst[i][1:]
        else:
          self.normalization+=norm_flat_lst[i]
          self.normalization_u+=norm_unicode_lst[i]
      else:
        self.normalization+=norm_flat_lst[i]
        self.normalization_u+=norm_unicode_lst[i]
      i+=1

  def get_placeholders_lst(self):
    """
    Returns a list of rule-based placeholders or values.
    IMPORTANT: ´PLACEHOLDERS´ should contain a full list of possible values.
    """
    placeholders_lst = []
    for s in self.sign_list:
      if is_int(s['value'][0])==True:
        placeholders_lst = self.append_if_not_as_last('NUMB',
                                                      placeholders_lst)
      # ADD HERE RULES FOR PN, DN etc.
      # E.g.:
      # if (s[value], s['index']) in [('lugal', ''), ('lu', '2')]
      # ADD determinatives handling to class!!!
      #  for now they are just deleted
      # NOTE also that PNs can come with cases, e.g. PN-ta 
      else:
        placeholders_lst.append(s['value'])
    return placeholders_lst

  def append_if_not_as_last(self, el, lst):
    if lst==[]:
      return [el]
    if lst[-1]!=el:
      lst.append(el)
    return lst
  
  def standardize_translit(self, translit):
    std_dict = {'š':'c', 'ŋ':'j', '₀':'0', '₁':'1', '₂':'2',
                '₃':'3', '₄':'4', '₅':'5', '₆':'6', '₇':'7',
                '₈':'8', '₉':'9', '+':'-', 'Š':'C', 'Ŋ':'J',
                'sz': 'c', 'SZ': 'C', '·':'', '°':'', '#':'',
                '!':'', '?': ''}
    for key in std_dict.keys():
      translit = translit.replace(key, std_dict[key])
    if self.re_times.search(translit):
      translit = self.re_times.sub('\g<a>×\g<b>', translit)
    return translit

  def get_unicode_index_all(self):
    i = 0
    while i < len(self.sign_list):
      self.sign_list[i] = self.get_unicode_index(self.sign_list[i])
      i+=1

  def get_unicode_index(self, sign_dict):

    sign_dict['u_sign'] = sign_dict['value']
    if sign_dict['index'] not in ['', 'x']:
      val = sign_dict['value']
      try:
        v = self.re_last_vow.findall(val)[-1]
      except:
        print(val, self.raw_translit)
      esc = chr((self.vow_lst.index(v)+1)*1000+int(sign_dict['index']))
      i = val.rfind(v)
      u_sign = '%s%s%s' %(val[:i], esc, val[i+1:])
      sign_dict['u_sign']=u_sign
    return sign_dict    

  def revert_unicode_index(self, u_sign): 
    i = 0
    while i < len(u_sign):
      n = ord(u_sign[i])
      if n > 1000:
        vow_i = int(str(n)[0])-1
        index = int(str(n)[2:])
        return {'value': u_sign[:i]+self.vow_lst[vow_i]+u_sign[i+1:],
                'index': index}
      i+=1

  def remove_determinatives(self, translit):
    det = re.compile('(\{.*?\})')
    return det.sub('', translit)


final_file = [] #Contains the final processed file
with open(INPUT_FILE, 'r') as f, open('temp.out', 'w+') as g:
  for line in f:
    line = line.split()
    temp_tokens = ""
    for token in line:
      unified = transliteration(token)
      if unified.defective == True:
        temp_tokens+= "Defective "
      else:
        temp_tokens= temp_tokens + unified.normalization + " "

    final_file.append(temp_tokens.strip())

  for item in final_file:
    g.write(item)
    g.write('\n')
