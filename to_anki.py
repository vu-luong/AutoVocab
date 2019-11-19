#!/usr/bin/env python

import sys
import requests
from lxml import etree
from google_images_download import google_images_download   #importing the library
from datetime import date

response = google_images_download.googleimagesdownload()   #class instantiation

try:
    date = sys.argv[1]
except:
    date = str(date.today())

print(date)


folder = '/Users/AnhVu/Study/English/laban_api'
with open(folder + '/daily_vocab/{}.txt'.format(date)) as f:
    content = f.readlines()

words = [x.strip() for x in content]

# words = ['bull', 'cat']
f = open(folder + '/to_anki/vocab_{}.csv'.format(date),'a+', encoding='utf8')

# for word in words:

word = words[-1]

print(word)
s = '"' + word + '","'
url = 'https://dict.laban.vn/find?type=1&query={}'.format(word)

res = requests.get(url)

myparser = etree.HTMLParser(encoding="utf-8")
tree = etree.HTML(res.content, parser=myparser)

definition = tree.xpath('/html/body/div[3]/div[2]/div[3]/ul/li[1]/div')
if len(definition) > 0:
    for item in definition[0]:
        if len(list(item)) > 0:
            if 'class' in item.attrib:
                if item.attrib['class'] == 'bg-grey bold font-large m-top20':
                    for item2 in item:
                        pat = "<div style='margin-top: 8px'><span style='font-family: Arial; text-align: left; font-size: 25px; color: black;border:1px solid lightgray; padding: 1px; background-color: lightgray'>{}</span></div>"
                        s = s + pat.format(item2.text)
        else:
            if item.attrib['class'] == 'green bold margin25 m-top15':
                pat = "<div style='margin-top: 3px'><span style='background-color:green; margin-left:1em; margin-right: 4px; display: inline-block; height: 17px'>&nbsp</span>"
                s = s + pat + item.text.replace(word, '***') + '</div>'
    s = s + '","'
    arguments = {"keywords": word, "limit": 2}   #creating list of arguments
#     paths = response.download(arguments)   #passing the arguments to the function
#     print(paths)           # printing absolute paths of the downloaded images

#     try:
#         s = s + "<img src='{}'>".format(paths[0][word][0])
#         s = s + " <img src='{}'>".format(paths[0][word][1])
#     except:
    s = s + "(unknown)"

    s = s + '"\n'
    # print(s)
    f.write(s)


f.close()
