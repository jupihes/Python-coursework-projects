# -*- coding: utf-8 -*-
"""
@author: Jupihes
"""
import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.truecar.com/used-cars-for-sale/listings/cadillac/ats/year-2016-max/?trim=standard'

webpage = requests.get(url)
soup = BeautifulSoup(webpage.text, 'html.parser')
del webpage

# results = soup.find_all('div')#('div.kt-post-card__body')
# for tag in soup.find_all('a'):
#     print(tag.name,tag.attrs,tag.text)
    
# results = soup.find_all('a')
# # for item in results:
# #     class="kt-post-card kt-post-card--outlined"


#results = soup.find_all('div',"vehicleCardPricingBlockPrice")


'''
<div class="padding-left-3 padding-left-lg-2 vehicle-card-bottom-pricing-secondary vehicle-card-bottom-max-50">
<div data-test="vehicleListingPriceAmount">
<div class="heading-3 margin-y-1 font-weight-bold" data-qa="Heading" data-test="vehicleCardPricingBlockPrice">$28,892</div></div></div>


<div class="font-size-1 text-truncate" data-test="vehicleMileage">
<svg viewBox="0 0 24 24" class="icon icon-before vehicle-card-icon icon-color-default" style="width: 16px; height: 16px; stroke-width: 1.5;">
<path d="M.28 15.67l2.68.19M1.04 12.26l2.59 1M2.77 9.22l2.24 1.76M5.32 6.82l1.57 2.26M8.47 5.28l3.21 10.58M11.92 4.74l.02 2.9M15.38 5.23l-.83 2.79M18.55 6.73l-1.62 2.41M21.13 9.09l-2.24 1.81M22.91 12.1l-2.64 1.06M23.72 15.5l-2.8.24">
</path>
<circle cx="11.92" cy="16.64" r=".87"></circle>
</svg>
31,182 miles</div>

'''
'''
<div data-test="cardContent" class="card-content vehicle-card-body order-3">
<div class="vehicle-card-top">
<h3 class="heading-base" data-qa="Heading" data-test="vehicleListingCardTitle">
<div data-test="vehicleCardYearMakeModel" class="vehicle-card-header w-100"><span class="font-size-1 margin-right-1 font-weight-bold">Sponsored</span><span class="vehicle-card-year font-size-1">2018</span> <span class="vehicle-header-make-model text-truncate">Cadillac ATS</span></div><div class="font-size-1 text-truncate" data-test="vehicleCardTrim">Coupe 2.0T RWD</div></h3></div><div class="vehicle-card-bottom vehicle-card-bottom-top-spacing"><div class="d-flex w-100 vehicle-card-bottom-pricing justify-content-between" style="min-height: 43px;"><div class="padding-right-3 vehicle-card-bottom-pricing-primary"><div><div class=""><div class="vehicle-card-price-rating-label-container"><div class="graph-icon-container graph-icon-bucket-two vehicle-card-price-rating-label-icon-container" style="height: 1rem; width: 1rem;"><svg viewBox="0 0 24 24" class="icon graph-icon undefined icon-fill-default" style="width: 8px; height: 8px; stroke-width: 3;"><path d="M12 20L24 6H0z" fill-rule="evenodd"></path></svg></div><span data-test="graphIconLabel" class="graph-icon-title margin-left-1 vehicle-card-price-rating-label text-truncate font-weight-bold">Great Price</span></div></div><div class="font-size-1 text-truncate">$105 off avg. list price</div></div></div><div class="padding-left-3 padding-left-lg-2 vehicle-card-bottom-pricing-secondary vehicle-card-bottom-max-50"><div data-test="vehicleListingPriceAmount"><div class="heading-3 margin-y-1 font-weight-bold" data-qa="Heading" data-test="vehicleCardPricingBlockPrice">$28,892</div></div></div></div></div><div class="margin-top-2_5 padding-top-2_5 border-top w-100"><div class="d-flex w-100 justify-content-between"><div class="font-size-1 text-truncate" data-test="vehicleMileage"><svg viewBox="0 0 24 24" class="icon icon-before vehicle-card-icon icon-color-default" style="width: 16px; height: 16px; stroke-width: 1.5;"><path d="M.28 15.67l2.68.19M1.04 12.26l2.59 1M2.77 9.22l2.24 1.76M5.32 6.82l1.57 2.26M8.47 5.28l3.21 10.58M11.92 4.74l.02 2.9M15.38 5.23l-.83 2.79M18.55 6.73l-1.62 2.41M21.13 9.09l-2.24 1.81M22.91 12.1l-2.64 1.06M23.72 15.5l-2.8.24"></path><circle cx="11.92" cy="16.64" r=".87"></circle></svg>31,182 miles</div></div><div class="vehicle-card-location font-size-1 margin-top-1" data-test="vehicleCardLocation"><svg viewBox="0 0 24 24" class="icon icon-before vehicle-card-icon icon-color-default" style="width: 16px; height: 16px; stroke-width: 1.5;"><circle cx="12.03" cy="9.02" r="3.5"></circle><path d="M20.53 9c0 6.5-8 14.5-8.5 14.5s-8.5-8-8.5-14.5a8.5 8.5 0 0117 0z"></path></svg>Pembroke Pines, FL</div><div class="vehicle-card-location font-size-1 margin-top-1 text-truncate" data-test="vehicleCardColors"><svg viewBox="0 0 24 24" class="icon icon-before vehicle-card-icon icon-color-default" style="width: 16px; height: 16px; stroke-width: 1.5;"><path d="M18.45 18.94l2.13-3.61 2.16 3.65"></path><path d="M22.67 18.86a2.54 2.54 0 01.46 1.33v.13a2.55 2.55 0 11-5.1 0v-.23a2.54 2.54 0 01.46-1.24"></path><circle cx="14.5" cy="9.5" r="1"></circle><path d="M20.42 12.26L10.33 22.35 1.3 13.31 11.39 3.22M14.5 9V1M10.64 2.09l10.84 10.84"></path></svg>Black exterior, Black interior</div></div><div class="vehicle-card-location font-size-1 margin-top-1" data-test="vehicleCardCondition"><svg viewBox="0 0 24 24" class="icon icon-before vehicle-card-icon icon-color-default" style="width: 16px; height: 16px; stroke-width: 1.5;"><path d="M22 13.13v6.23a.7.7 0 01-.68.72h-2.71a.69.69 0 01-.65-.72v-1.28H6v1.28a.69.69 0 01-.65.72H2.64a.7.7 0 01-.64-.72v-5.91a2.84 2.84 0 01.34-1.35l2.09-4A3.76 3.76 0 017.6 6.08H17a3.79 3.79 0 013.4 2.47L21.75 12a2.93 2.93 0 01.25 1.13z"></path><path d="M7.96 14.08h-3"></path><path d="M2.83 11.08H.46M23.46 11.08h-2.09M18.46 11.08h-13"></path><path d="M18.96 14.08h-3"></path></svg>No accidents, 1 Owner, Personal use</div><div class="font-size-1 margin-top-1" data-test="vehicleCardCpo"><svg viewBox="0 0 24 24" class="icon icon-before vehicle-card-icon icon-color-default" style="width: 16px; height: 16px; stroke-width: 1.5;"><path d="M19.11 6.81a7.53 7.53 0 11-1.39-3.32l.34.48"></path><path d="M17.17 13v9.75l-5.39-4.09-5.61 4.09V13M8.02 6.65l3.96 3.96 8.59-9.39"></path></svg>Certified Pre-Owned</div></div>
'''

sample_text = 'Sponsored2018 Cadillac ATSCoupe 2.0T RWDGreat Price$105 off avg. list price$28,89231,182 milesPembroke Pines, FLBlack exterior, Black interiorNo accidents, 1 Owner, Personal useCertified Pre-Owned'
re.findall(r'(\$\d+) off avg. list price(\$\d{1,3}),(\d{3})(\$\d{1,3}),(\d{3}) miles', sample_text)
numbers = re.findall(r'((\$\d{1,3}),(\d{3}))((\d{1,3}),(\d{3}) miles)', sample_text)

#'Sponsored2018 Cadillac ATS'
year_model = re.findall(r'([Sponsored?]\d{4}) Cadillac ATS', sample_text)


results = soup.find_all('div',"card-content vehicle-card-body order-3")

number_list = []
for tag in results:
    # for i in tag.findChildren('div',"heading-3 margin-y-1 font-weight-bold"):
    #     print(i.text)
    
    if tag.findChildren('div',"font-size-1 text-truncate"):
        #print(tag.text,sep='  ******  ')
        numbers = re.findall(r'((\$\d{1,3}),(\d{3}))((\d{1,3}),(\d{3}) miles)', tag.text)
        #re.sub(r'\$','', ,count=1)
        print(numbers[0][0], numbers[0][3])
        number_list.append([numbers[0][0].replace('$','').replace(',',''), numbers[0][3].replace(' miles','').replace(',','')])

##############     Writing to DB     ##############
import mysql.connector

cnx = mysql.connector.connect(user='...',password='...', database='learndb')
cursor = cnx.cursor()

##############     Table creation     ##############
#  
# query = ('''CREATE TABLE truecar_table (record_num  int, price int, miles int)''')
# 
# cursor.execute(query)
# 
####################################################

##############     INSERT into DB     ##############

add_record = ("INSERT INTO truecar_table "
               "(record_num, price, miles) "
               "VALUES (%s, %s, %s)")

for n,item in enumerate(number_list):
    #print(n, int(item[0]), int(item[1]))
    data_record = (int(n+1), int(item[0]), int(item[1]))
    # print(data_record)
    ####### Insert new record
    cursor.execute(add_record, data_record)
    
cnx.commit()

# print('Here is what we have in table:\n')
# select_query = ('''SELECT * 
#                 FROM truecar_table''')
# cursor.execute(select_query)
# for (record_num, price, miles) in cursor:
#   print("{}, {}, {}".format(
#     record_num, price, miles))

cursor.close()
cnx.close()
