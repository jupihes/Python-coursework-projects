# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 10:38:47 2021

@author: H.Mohammadhosseini
"""
import requests
from bs4 import BeautifulSoup
import re
from pandas import DataFrame
 
url = 'https://divar.ir/s/tehran'#'https://divar.ir/s/tehran/vehicles'

#https://divar.ir/s/tehran/rent-apartment/khani-abad?size=-65&elevator=true&parking=true

webpage = requests.get(url)

soup = BeautifulSoup(webpage.text, 'html.parser')

# results = soup.find_all('div')#('div.kt-post-card__body')
# for tag in soup.find_all('a'):
#     print(tag.name,tag.attrs,tag.text)
    
# results = soup.find_all('a')
# # for item in results:
# #     class="kt-post-card kt-post-card--outlined"

# results = soup.find_all('div',"kt-post-card__body")#"kt-post-card kt-post-card--outlined")#
# for tag in results:
#     #if re.findall(r'توافقی',tag) != []:
#     print(tag.name, tag.attrs, tag.text)
#     input()


results = soup.find_all('div',"kt-post-card__body")

'''
<div class="kt-post-card__body">
<div class="kt-post-card__title">کوییک R آر سفید سقف قرمز صفر // مدل 1400</div>
<div class="kt-post-card__description">۰ کیلومتر
توافقی</div><div class="kt-post-card__bottom">
<span class="kt-post-card__bottom-description kt-text-truncate" title="نمایشگاه در توحید">نمایشگاه در توحید</span>
</div>
</div>
'''
temp_list = []
for tag in results:
    if re.findall(r'توافقی',tag.text) != []:
        #print(tag.text)
        temp_txt =  ''
        #print('-----    -----')
        for i in tag.findChildren():
            #print(i.tag, i.attrs, i.text,sep='\n')
            #if re.findall(r'توافقی',i.text) != []:
            # print(re.sub(r'[\n-۰-u"\u200C"]',' ', i.text), sep=',')
            extracted_text =  re.sub(r'[\n]',' ', i.text) #-u"\u200C"۰ '۰'
            # print(i.text.replace('u\u200c', ''))
            #extracted_text = re.sub(r'توافقی','توافقی ', extracted_text)
            temp_txt = temp_txt + ',' + extracted_text.strip()
        # print('---------------')
        print(temp_txt)
        # print('------!!!!-----')
        #print(temp_txt.split(','))
        temp_list.append(temp_txt)

# df = DataFrame(temp_list,columns=['header'])
# df.to_csv('sample_output.csv',index= False, encoding="utf8")
# =============================================================================

# ###########################################################
# # https://beautiful-soup-4.readthedocs.io/en/latest/index.html?highlight=find_all#find-all
# html_doc = """
# <html><head><title>The Dormouse's story</title></head>
# <body>
# <p class="title"><b>The Dormouse's story</b></p>
# 
# <p class="story">Once upon a time there were three little sisters; and their names were
# <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
# <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
# <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
# and they lived at the bottom of a well.</p>
# 
# <p class="story">...</p>
# """
# from bs4 import BeautifulSoup
# import re
# 
# soup_sample = BeautifulSoup(html_doc, 'html.parser')
# 
# for tag in soup.find_all(re.compile("^b")):
#     print(tag.name)
# 
# 
# for tag in soup_sample.find_all('a'):
#     print(tag.name, tag.attrs, tag.text)
# 
# # a {'href': 'http://example.com/elsie', 'class': ['sister'], 'id': 'link1'} Elsie
# # a {'href': 'http://example.com/lacie', 'class': ['sister'], 'id': 'link2'} Lacie
# # a {'href': 'http://example.com/tillie', 'class': ['sister'], 'id': 'link3'} Tillie
# 
# def has_class_but_no_id(tag):
#     return tag.has_attr('class') and not tag.has_attr('id')
# 
# soup_sample.find_all(has_class_but_no_id) # not like link!!!!?
# # [<p class="title"><b>The Dormouse's story</b></p>,
# #  <p class="story">Once upon a time there were three little sisters; and their names were
# #  <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
# #  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
# #  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;
# #  and they lived at the bottom of a well.</p>,
# #  <p class="story">...</p>]
# 
# def has_no_id(tag):
#     return not tag.has_attr('id')
# 
# soup_sample.find_all(has_no_id)
# Out[128]: 
# [<html><head><title>The Dormouse's story</title></head>
#  <body>
#  <p class="title"><b>The Dormouse's story</b></p>
#  <p class="story">Once upon a time there were three little sisters; and their names were
#  <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;
#  and they lived at the bottom of a well.</p>
#  <p class="story">...</p>
#  </body></html>,
#  <head><title>The Dormouse's story</title></head>,
#  <title>The Dormouse's story</title>,
#  <body>
#  <p class="title"><b>The Dormouse's story</b></p>
#  <p class="story">Once upon a time there were three little 
# 
# from bs4 import NavigableString
# def surrounded_by_strings(tag):
#     return (isinstance(tag.next_element, NavigableString)
#             and isinstance(tag.previous_element, NavigableString))
# 
# for tag in soup_sample.find_all(surrounded_by_strings):
#     print(tag.name)
# =============================================================================
