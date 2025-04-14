# -*- coding: utf-8 -*-
"""
Created on Dec 20 2021

@author: Jupihes
"""
import requests
from bs4 import BeautifulSoup
#from lxml import etree
import re
from pandas import DataFrame , concat
from numpy import nan
from hashlib import sha256
from time import sleep

##############     Divar     #####################
def urladd_digest(input_text):
    return sha256(str(input_text).encode('utf-8')).hexdigest()

url = 'https://divar.ir/s/nasimshahr/buy-apartment?price=750000000-1300000000&sort=sort_date'
df = DataFrame()
temp_list = []
for i in range(22):
    print(i, df.shape)
    if i == 0:
        url_in_use = url #'https://divar.ir/s/tehran/car/pride'
    else:
        url_in_use = url +'?page='+str(i+1)  # 'https://divar.ir/s/tehran/car/pride'+'?page='+str(i+1)
   
    webpage = requests.get(url_in_use)
   
    soup = BeautifulSoup(webpage.text, 'html.parser')
    del webpage
   
    #### we need to pause for 60 second after 7 requests
    if (i%7 == 0 and i!=0): #'\n\n\nToo many requests\n\n\n429 Too many requests\nYou can have 7 requests every 60 seconds\n\n'
        sleep(60)
        print('Pause for 60 second so that to Divar allow us to continue!')
   
    results = soup.find_all('div',attrs={"class": "kt-post-card__body"}) #results = soup.find_all('div',"kt-post-card__body")
   
    '''
    <div class="kt-post-card__body">
    <div class="kt-post-card__title">æûLER ÂÑ ÓÝúë ÓÞÝ ÞÑãÒ ÕÝÑ // ãÏE1400</div>
    <div class="kt-post-card__description">? íáæãÊÑ
    ÊæÇÝÞE/div><div class="kt-post-card__bottom">
    <span class="kt-post-card__bottom-description kt-text-truncate" title="äãÇúðÇEÏÑ ÊæÍúë">äãÇúðÇEÏÑ ÊæÍúë</span>
    </div>54
    </div>
    '''
    ### remained items
   
    # [#] 1. extarct URL of item
   
    ####### find parent
    # <a class="kt-post-card kt-post-card--outlined kt-post-card--has-chat"
    #
    # try:
    #     up = soup.find('div',attrs={"class": "kt-post-card__body"}).parent
    # except AttributeError:
    #     # no <i> element
    #     pass
   
    # up = soup.find('div',attrs={"class": "kt-post-card__body"}).parent
   
    # item_url = 'https://divar.ir' + up.attrs.get('href') # Work and try to learn more!!!!!!!!!!!!  up.find('a', "href")
   
    # [#] 2. extarct next pages
   
    '''
   
    <link data-react-helmet="true" rel="apple-touch-icon" href="https://s100.divarcdn.com/static/thewall-assets/android-chrome-512x512.png"/><link data-react-helmet="true" rel="android-touch-icon" href="https://s100.divarcdn.com/static/thewall-assets/android-chrome-512x512.png"/><link data-react-helmet="true" href="https://s100.divarcdn.com/statics/2021/12/IRANSansWeb.cdb118d6.woff2" type="font/woff2" as="font" rel="preload" crossorigin="anonymous"/><link data-react-helmet="true" href="https://s100.divarcdn.com/statics/2021/12/IRANSansWeb_Medium.9f338149.woff2" type="font/woff2" as="font" rel="preload" crossorigin="anonymous"/><link data-react-helmet="true" rel="canonical" href="https://divar.ir/s/tehran/car/pride"/><link data-react-helmet="true" rel="next" href="https://divar.ir/s/tehran/car/pride?page=2"/>
   
   
    <link data-react-helmet="true" rel="next" href="https://divar.ir/s/tehran/car/pride?page=2"/>
    '''
    next_page = soup.find('link',"href") #attrs={"class": "kt-post-card__body"})
   

    # 3.remove duplicates ? use hash URL
    #import hashlib

    # def urladd_digest(input_text):
    #     hash_object = sha256(str(input_text).encode('utf-8'))#hashlib.sha256
    #     #print(string_to_hash, ' Hash is ', hash_object.hexdigest())
    #     #hash_map[hash_object.hexdigest()] = str(string_to_hash)
       
    #     # def dehash(hashed_value):
    #     #     return int(hash_map.get(hashed_value))
    #     return hash_object.hexdigest()


    for tag in results:
       
        up = tag.parent # soup.find('div',attrs={"class": "kt-post-card__body"}).parent
        
        # to manage change in Divar
        up = up.parent
        item_url = 'https://divar.ir' + up.attrs.get('href')
        if True:#re.findall(r'ÊæÇÝÞE,tag.text) == []:
            #print(tag.tag, tag.text)
            temp_txt =  ''
            #print('-----    -----')
            temp_list1 = []
            for i in tag.findChildren():
                #print(i.tag, i.attrs, i.text,sep='\n')
               
                temp_list1.append(i.text)
                #if re.findall(r'ÊæÇÝÞE,i.text) != []:
                # print(re.sub(r'[\n-?-u"\u200C"]',' ', i.text), sep=',')
                extracted_text =  re.sub(r'[\n]',' ', i.text) #-u"\u200C"? '?'
                # print(i.text.replace('u\u200c', ''))
                #extracted_text = re.sub(r'ÊæÇÝÞE,'ÊæÇÝÞE', extracted_text)
                temp_txt = temp_txt + ',' + extracted_text.strip()
                #print('---------------')
           
            temp_list1.append(item_url)
            temp_list1.append(urladd_digest(item_url))

            df = df.append([temp_list1])
            #print((temp_list1))
            #print(temp_txt)
            # print('------!!!!-----')
            #print(temp_txt.split(','))
            temp_list.append(temp_txt)
   


#df = DataFrame(temp_list1)

df.reset_index(inplace=True)
del df['index']

temp_df = df.copy()
#df = temp_df
temp_df.to_csv('Divar_Nasimshahr.csv',index= False, encoding="utf8")
