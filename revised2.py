import requests
from bs4 import BeautifulSoup
import re
from pandas import DataFrame , concat
from numpy import nan
from hashlib import sha256
from time import sleep


def urladd_digest(input_text):
    return sha256(str(input_text).encode('utf-8')).hexdigest()

base_url = 'https://divar.ir/s/'
query_where_what = 'nasimshahr/buy-apartment?'
query_string = 'price=750000000-1300000000&sort=sort_date'
url = base_url + query_where_what + query_string # 'https://divar.ir/s/nasimshahr/buy-apartment?price=750000000-1300000000&sort=sort_date'

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
   
    ### remained items
    # [#] 1. extarct URL of item
    # [#] 2. extarct next pages
    next_page = soup.find('link',"href") #attrs={"class": "kt-post-card__body"})
   
    # 3.remove duplicates ? use hash URL
    for tag in results:
       
        up = tag.parent # soup.find('div',attrs={"class": "kt-post-card__body"}).parent
        
        # to manage change in Divar
        # up = up.parent
        item_url = 'https://divar.ir' + up.attrs.get('href')
        if True:#re.findall(r'ÊæÇÝÞE,tag.text) == []:
            #print(tag.tag, tag.text)
            temp_txt =  ''
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
           
            temp_list1.append(item_url)
            temp_list1.append(urladd_digest(item_url))

            df = df.append([temp_list1])
            temp_list.append(temp_txt)

df.reset_index(inplace=True)
del df['index']

temp_df = df.copy()

file_name = query_where_what.replace(r'/', ' ').replace('?', ' ')
temp_df.to_csv(f'Divar_{file_name}.csv',index= False, encoding="utf8")
