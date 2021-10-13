#./venv/bin/python3
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import random 
import time
from fake_useragent import UserAgent
import csv
from datetime import datetime

UserAgent().chrome
unprocessed_links = open('links.txt', 'r')

selected_parameters_list=['Общая площадь','Количество комнат','Отделка', 'Ремонт', 'Этаж','Тип дома','Срок сдачи','Год постройки', 'Корпус, строение','Адрес','Цена','Ссылка']
finishing_set=set(['чистовая', 'черновая','без отделки'])
type_of_house_set=set(['монолитный', 'кирпичный','панельный','блочный'])
type_of_renovation=set(['дизайнерский','требует ремонта','косметический','евро'])
procesed_links_set=set()
current_datetime = datetime.now()
result_file = open('results/'+str(current_datetime)+'.csv', 'w')
writer = csv.writer(result_file)
title_row=[]
for param in selected_parameters_list:
    title_row.append(param)
writer.writerow(title_row)

procesed_links_file = open('procesed_links.txt', 'r')
procesed_links=procesed_links_file.readlines()
procesed_links_file.close()

procesed_links_file = open('procesed_links.txt', 'a')
procesed_links_file.write('')

for link in procesed_links:
    procesed_links_set.add(link)
print(procesed_links_set)

for i in range(1,300):
    print(i)   
    flat_param_dict={}
    curr_url = unprocessed_links.readline()  
    url="https://www.avito.ru"+curr_url
    #url="https://www.avito.ru/sankt-peterburg/kvartiry/5-k._kvartira_83m_55et._2241014671"
    print(url)
    if url  not in procesed_links_set:
        headers = { 'User-Agent' : UserAgent().random }
        req = Request(url)
        try:
            page = urlopen(req)
        except HTTPError as e:
            # do something
            print('Error code: ', e.code)
            if e.code==429:
                result_file.close()
                procesed_links_file.close()
        except URLError as e:
            # do something
            print('Reason: ', e.reason)
        else:    
            flat_param_dict['url']=url
            flat_param_dict['Ссылка']=url            
            soup = BeautifulSoup(page,"html.parser")
            if(page.getcode()==200) and soup.find('span',class_="item-closed-warning__content")==None:#Провкрка что объявление не снято
                elements=soup.find_all('li',class_="item-params-list-item")
                for el in elements:
                    param=el.text.split(":")[0]
                    value=el.text.split(":")[1]
                    param=(' '.join(param.split()))
                    value=(' '.join(value.split()))
                    if param in selected_parameters_list:
                        if(param=='Этаж'):
                            curr_floor=(value.split()[0])
                            max_floor=(value.split()[-1])
                            value=(curr_floor+'/'+max_floor)
                        elif(param=='Общая площадь'):
                            value=(value.split()[0])
                        elif(param=='Количество комнат'):
                            if value=='студия':
                                value=0
                            elif value=='многокомнатная':
                                value=10
                            else: 
                                value=int(value)
                        elif(param=='Отделка') and (value not in finishing_set):
                            print('Not in finishing set ',value)                           
                        elif(param=='Тип дома') and (value not in type_of_house_set):
                            print('Not in type of hous set ',value)
                        elif(param=='Ремонт') and (value not in type_of_renovation):
                            print('Not in type of renovation ',value)
                            print (value)
                            print (el.text.split())
                        flat_param_dict[param]=value
                                                       
                elements=soup.find_all('span',class_="item-address__string")
                if elements !=[]:
                    adress=elements[0].text
                    print(adress)
                    elements=soup.find('span',class_="js-item-price")
                    price=int(elements.get_attribute_list('content')[0])
                    flat_param_dict['Адрес']=adress
                    flat_param_dict['Цена']=price
                    #print(flat_param_dict.values())
                    flat_param_row=[]           
                    for param in selected_parameters_list:
                        flat_param_row.append(flat_param_dict.get(param,' '))                    
                    writer.writerow(flat_param_row)
                    procesed_links_file.write(url)
                    procesed_links_set.add(url)
                    time.sleep(random.randint(0, 12))                
result_file.close()
unprocessed_links.close()
procesed_links_file.close()
print(flat_param_dict)