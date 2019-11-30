#!/usr/bin/env python

import sys
import requests
from lxml import etree
from datetime import date
import oxford

try:
    date = sys.argv[1]
except:
    date = str(date.today())

print(date)

folder = '/Users/AnhVu/Study/English/laban_api'
with open(folder + '/daily_vocab/{}.txt'.format(date)) as f:
    content = f.readlines()

words = [x.strip() for x in content]

f = open(folder + '/to_anki/vocab_{}.csv'.format(date), 'a+', encoding='utf8')

word = words[-1]

print(word)
s = '"' + word + '","'

oxford.Word.get(word)
definitions = oxford.Word.definitions()

s = s + "\n - ".join(definitions) + '"\n'

f.write(s)

f.close()
