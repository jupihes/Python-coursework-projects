# -*- coding: utf-8 -*-
"""
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

url = 'https://divar.ir/s/tehran/car' #'https://divar.ir/s/tehran/car/pride'
df = DataFrame()
temp_list = []
for i in range(220):
    print(i, df.shape)
    if i == 0:
        url_in_use = url #'https://divar.ir/s/tehran/car/pride' 
    else:
        url_in_use = 'https://divar.ir/s/tehran/car/pride'+'?page='+str(i+1)
    
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
    <div class="kt-post-card__title">کوییک R آر سفید سقف قرمز صفر // مدل 1400</div>
    <div class="kt-post-card__description">۰ کیلومتر
    توافقی</div><div class="kt-post-card__bottom">
    <span class="kt-post-card__bottom-description kt-text-truncate" title="نمایشگاه در توحید">نمایشگاه در توحید</span>
    </div>
    </div>
    '''
    
    '''
    
    <link data-react-helmet="true" rel="apple-touch-icon" href="https://s100.divarcdn.com/static/thewall-assets/android-chrome-512x512.png"/><link data-react-helmet="true" rel="android-touch-icon" href="https://s100.divarcdn.com/static/thewall-assets/android-chrome-512x512.png"/><link data-react-helmet="true" href="https://s100.divarcdn.com/statics/2021/12/IRANSansWeb.cdb118d6.woff2" type="font/woff2" as="font" rel="preload" crossorigin="anonymous"/><link data-react-helmet="true" href="https://s100.divarcdn.com/statics/2021/12/IRANSansWeb_Medium.9f338149.woff2" type="font/woff2" as="font" rel="preload" crossorigin="anonymous"/><link data-react-helmet="true" rel="canonical" href="https://divar.ir/s/tehran/car/pride"/><link data-react-helmet="true" rel="next" href="https://divar.ir/s/tehran/car/pride?page=2"/>
    
    
    <link data-react-helmet="true" rel="next" href="https://divar.ir/s/tehran/car/pride?page=2"/>
    '''
    next_page = soup.find('link',"href") #attrs={"class": "kt-post-card__body"})
    


    for tag in results:
        
        up = tag.parent # soup.find('div',attrs={"class": "kt-post-card__body"}).parent
        item_url = 'https://divar.ir' + up.attrs.get('href')
        if True:#re.findall(r'توافقی',tag.text) == []:
            #print(tag.tag, tag.text)
            temp_txt =  ''
            #print('-----    -----')
            temp_list1 = []
            for i in tag.findChildren():
                #print(i.tag, i.attrs, i.text,sep='\n')
                
                temp_list1.append(i.text)
                #if re.findall(r'توافقی',i.text) != []:
                # print(re.sub(r'[\n-۰-u"\u200C"]',' ', i.text), sep=',')
                extracted_text =  re.sub(r'[\n]',' ', i.text) #-u"\u200C"۰ '۰'
                # print(i.text.replace('u\u200c', ''))
                #extracted_text = re.sub(r'توافقی','توافقی ', extracted_text)
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
temp_df.to_csv('Divar_5200car_sample.csv',index= False, encoding="utf8")

##### condition on number of columns
#check df.info() to see if Null exists

###  case when null
df.loc[(df[7].isna() == True), 'url'] = df[5] #df.loc[(df[6].isna() == True), 'url'] = df[5]
df.loc[(df[6].isna() == True) & (df[7].isna() == True), 'url'] = df[4]#df.loc[(df[5].isna() == True) & (df[6].isna() == True), 'url'] = df[4]
df.loc[(df['url'].isna() == True), 'url'] = df[6] #df.loc[(df['url'].isna() == True), 'url'] = df[6]

# df[4][df[4].isna() == True] = ''
# df[5][df[5].isna() == True] = ''
# df[6][df[6].isna() == True] = ''
# df['url'] =  df[5] + df[6]

# df[df[4].str.contains(r'^در')]   # 'در '
# df[df[4].str.contains(r'^در')]
# df.loc[df[4] != '' , 'url'] = df[4]

df.drop(columns= [3, 4, 5, 6, 7],inplace=True)
    

df.columns = ['YearType','KmPrice','WhereWhen','url']

# df['temp'][df['temp'].isna() == True] = ''

df_year_type = df.YearType.str.split(r'\u060C',expand=True)
df = concat([df, df_year_type], axis=1)
df.drop(columns= ['YearType'],inplace=True)

df_Km_price = df.KmPrice.str.split(r'\n',expand=True)
df = concat([df, df_Km_price], axis=1)
df.drop(columns= ['KmPrice'],inplace=True)
del df_Km_price, df_year_type

#df.columns = ['WhereWhen','url','ModelType','Year','comment','Km','Price']
df.columns = ['WhereWhen','url','ModelType','Year', 'comment','junk','Km','Price']
df.Year = df.Year.str.extract(r'([\u06F0-\u06F9]{2,4})') # Exracting Persian Year :D
df.Year = df.Year.str.strip()

##### replace Arabic and Persian numbers to English numbers #####
# https://stackoverflow.com/questions/11879025/string-maketrans-for-english-and-persian-numbers
intab='۱۲۳۴۵۶۷۸۹۰١٢٣٤٥٦٧٨٩٠'
outtab='12345678901234567890'
translation_table = str.maketrans(intab, outtab)
#output_text = input_text.translate(translation_table)

df.Year = df.Year.str.translate(translation_table)

df_km = df.Km.str.split(r' ',expand=True)
df.Km = df_km[0].str.replace(',','').str.strip()
df.Km = df.Km.str.translate(translation_table)

df_price = df.Price.str.split(r' ',expand=True)
df.Price = df_price[0].str.replace(',','').str.strip()
df.Price = df.Price.str.translate(translation_table)


#df['hash'] = df['url'].apply(urladd_digest)

del df_km, df_price

df = concat([df, df.WhereWhen.str.split(r'پیش در ',expand=True)], axis=1)
del df['WhereWhen']
#df.columns = ['url', 'ModelType', 'Year', 'comment', 'Km', 'Price','hash', 'When', 'Where']
df.columns = ['url', 'ModelType', 'Year', 'comment', 'junk', 'Km', 'Price', 'When', 'Where']
for i in df.columns:
    df[i] = df[i].str.strip()

#####   remove duplicates + divide table into 2 tables   #####
### working to find duplicates
# =============================================================================
# duplicate_items = df_url.hash.value_counts().reset_index()
# duplicate_items.rename({'hash':'count record'},inplace=True, axis='columns')
# duplicate_items['index'][duplicate_items['count record']>1].values
# #df_tmp1.hash.drop_duplicates?
# #df.drop(df.iloc[:, 1:3], inplace = True, axis = 1)
# =============================================================================

df.drop_duplicates('hash',inplace=True)

df['hash'] = df['url'].apply(urladd_digest)

df_url = df[['url', 'hash']] # table 2: mapping URL to items details by indexas unique key
                             # "index", "url", "hash url"

df = concat([df, df.When.str.split(r' در ',expand=True)], axis=1)

df.loc[(df['Where'].isna() == True), 'Where'] = df[1]
df.drop(columns= ['url','junk','When','hash', 1], inplace=True)
df.rename({0:'When'},inplace=True, axis='columns')


#df = df[['ModelType', 'Year', 'Where', 'When','Km', 'Price','url', 'comment', 'hash']]
df = df[['ModelType', 'Year', 'Where', 'When','Km', 'Price']]

## tunning on Model type
df.ModelType = df.ModelType.str.translate(translation_table)

#df.ModelType.str.extract(r"(مدل \d{2,4})")[0].str.replace('مدل','')
df = concat([df, df.ModelType.str.extract(r"(مدل \d{2,4})",expand=True)[0].str.replace('مدل','')], axis=1)
df.ModelType = df.ModelType.str.replace(r"(مدل \d{2,4})", '', regex=True)

#df.loc[(df[0] == '00'), 0] = '1400'

#df_tmp1 = df
# df.loc[136].at[0]
df[0] = df[0].str.strip()
df[0] = df[0].str.replace(r"(^\d{2})$", '13\g<1>', regex=True)


df.loc[(df.Year.isna() == True) & (df[0].isna() != True), 'Year'] = df[0]
del df[0]

df.Price = df.Price.str.replace(r'[غیرقابل|جهت]', '0', regex=True)

# df.loc[20].at['Year'] = '1388'
# df.loc[20].at['ModelType'] = 'پراید '
#df.loc[31].at['Year'] = '1398'

df.dropna(inplace=True)

df.Price = df.Price.str.replace(r'0و0ف00','0', regex=True)


df.Year = df.Year.astype('int32')
df.Price = df.Price.astype('int32')
df.Km = df.Km.astype('int32')


###### remained items ::: to recheck here one ###### !!!!!!!!!!!!!!!!!!!!!!
# extract more features like from ModelType column
# 'بیرنگ'
# 'دوگانه سوز'
#'سالم'
#'نقره‌ای'
# 'ساده'
# 'CNG'
# 'صندوقدار'
# 'گاز سوز'


##################################################
##### 1.  extracting car categories (names)  #####
temp_names = df.ModelType.str.split(' ',expand=True)

temp_names

a = temp_names[0].value_counts()
a = a.reset_index()
a = temp_names[1].value_counts()
a = a.reset_index()

# make mapping dict of Persian to English name

car_mapping = {
'پراید':'Pride',
'نیسان':'Neissan',
'سمند':'Samand',
'پیکاپ':'Pick up',
'تویوتا':'Toyota',
'دنا':'Dena',
'هیوندای':'Honda',
'رنو':'Renoue',
'لیفان':'Lifan',
'پژو':'Pegouet',
'تندر':'Tondar',
'ریو':'Rio',
'کمری':'Camry', 
'سوناتا':'Sonata',
'مورانو':'Morano',
'سورنتو':'Sorento',
'برلیانس':'Berliance',
'تیبا':'Tiba',
'کرولا':'Corola',
'تیگو':'Tigo'
}

#a = df.ModelType.map(car_mapping)

for key, value in car_mapping.items():
    df.loc[df.ModelType.str.contains(key) == True, 'Model'] = value
    # if df.ModelType.str.contains(key).any():#print(key,value)
    #     df['Model'] = value

#####  Encoding car names  #####
class_mapping = {label:idx for idx,label in enumerate(df.Model.unique())}
class_mapping

#####  Mapping car name to number  #####

df['Modelid'] = df.Model.map(class_mapping)

class_mapping.head()


df_clean_ml = df[['Year', 'Km', 'Price', 'Modelid']] ## table 1 : cleaned English records

## table 3 : car mapping Persian to English to modelID
mapping_table = DataFrame({value:key for key, value in car_mapping.items()},\
                             index=['list name']).T

car_mapping_table = DataFrame(class_mapping,index=['Car type id']).T

car_mapping_table = mapping_table.merge(car_mapping_table, how = 'outer',left_index=True, right_index=True)
del mapping_table
## table 4 : Persian records
df_persian = df[['ModelType', 'Where', 'When', 'Model']]

df.reset_index(inplace=True)
df.to_csv('Divar_cleaned_sample.csv', index= False, encoding="utf8")
df_url.reset_index(inplace=True)
df_url.to_csv('Divar_url of samples.csv', index= False, encoding="utf8")
df_clean_ml.reset_index(inplace=True)
df_clean_ml.to_csv('cleaned_ML_input.csv', index= False, encoding="utf8")
car_mapping_table.reset_index(inplace=True)
car_mapping_table.to_csv('car mapping table.csv', index= False, encoding="utf8")

# b = df.ModelType.value_counts()
# b = df.Year.value_counts()

############## Writing to DB #####################
import mysql.connector
from sqlalchemy import create_engine

cnx = mysql.connector.connect(user='...',password='...', database='...')
cursor = cnx.cursor()

# ==================         Table creation         ===========================
## table 1 : cleaned English records
query_divar_clean_car = ("CREATE TABLE `Divarcar` ("
    "  `id` int(10) NOT NULL AUTO_INCREMENT,"
    "  `Year` int(4) NOT NULL,"
    "  `Km` int(10) NOT NULL,"
    "  `Price` int(16) NOT NULL,"
    "  `Modelid` varchar(2), "
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

cursor.execute(query_divar_clean_car)

## table 2: mapping URL to items details by indexas unique key
# "index", "url", "hash url"
'''To make it possibble to write Persian utf8 (4 bytes) to  MYSQL DB
ALTER DATABASE learndb
  CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
'''

query_car_urls = ("CREATE TABLE `carurls` ("
    "  `id` int(10) NOT NULL AUTO_INCREMENT,"
    "  `url`     varchar(100) , "
    "  `hashurl`      varchar(64), "
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")
#char(20) character set utf8 set colates utf8_persian_ci
cursor.execute(query_car_urls)

## table 3 : car mapping Persian to English to modelID
query_car_mapping = ("CREATE TABLE `carmapping` ("
    "  `name` varchar(15) ,"
    "  `persian_name`     varchar(20), "
    "  `car_typeid`      varchar(3), "
    "  PRIMARY KEY (`name`)"
    ") ENGINE=InnoDB")
    
cursor.execute(query_car_mapping)

###################### Writing to Mysql with Pandas to_sql ####################

database_username = '...'
database_password = '...'
database_ip       = '...'
database_name     = '...'
database_connection = create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                      format(database_username, database_password, 
                      database_ip, database_name), pool_recycle=1,
                            encoding='utf8', pool_timeout=57600).connect()
#https://datatofish.com/pandas-dataframe-to-sql/

df_clean_ml.to_sql(name='divarcar', con=database_connection, if_exists='replace', index_label= False)
### solving problem of Persian text 
# https://sebhastian.com/mysql-incorrect-string-value/

df_url.to_sql(name='carurls', con=database_connection, if_exists='replace', index_label= False)
car_mapping_table.to_sql(name='carurls', con=database_connection, if_exists='replace', index_label= False)

database_connection.close()
