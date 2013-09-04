'''
Created on 2011-5-2

@author: edison
'''
import re

class FilterTags(object):
    def __init__(self):
        pass
    
    def filter_tags(self,string):
        re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I)
        re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)
        re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)
        re_br = re.compile('<br\s*?/?>')
        re_h = re.compile('</?\w+[^>]*>')
        re_comment = re.compile('<!--[^>]*-->')
        s = re_cdata.sub('',string)
        s = re_script.sub('',s)
        s = re_style.sub('',s)
        s = re_br.sub('\n',s)
        s = re_h.sub('',s)
        s = re_comment.sub('',s)
        blank_line = re.compile('\n+')
        s = blank_line.sub('\n',s)
        s = self.replace_char_entity(s)
        return s
    
    def replace_char_entity(self,string):
        CHAR_ENTITIES = {'nbsp' : ' ', '160' : ' ',
                         'lt' : '<', '60' : '<',
                         'gt' : '>', '62' : '>',
                         'amp' : '&', '38' : '&',
                         'quot' : '"', '34' : '"'}
   
        re_char_entity = re.compile(r'&#?(?P<name>\w+);')
        sz = re_char_entity.search(string)
        while sz:
            entity = sz.group()#entityȫ�ƣ���&gt;
            key = sz.group('name')#ȥ��&;��entity,��&gt;Ϊgt
            try:
                string = re_char_entity.sub(CHAR_ENTITIES[key], string, 1)
                sz = re_char_entity.search(string)
            except KeyError:
            #�Կմ�����
                string = re_char_entity.sub('', string, 1)
                sz = re_char_entity.search(string)
        return string
