from selenium import webdriver

from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import re
driver = webdriver.Firefox(executable_path=r'/usr/local/bin/geckodriver')
pages =range(1,20)
#save pages from main url
base_url = 'https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&p='
for page in pages:
    url = 'https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&p='+str(page)
    driver.get(url)
    f = open('pages/p'+str(page)+'.txt', 'w')
    f.write(driver.page_source)
    f.close()
#extract flat links from pages
links_set=set()
f = open('links.txt', 'w')
for page in pages:
    fd = open('pages/p'+str(page)+'.txt', 'r')
    data = fd.read()
    fd.close()
    soup = BeautifulSoup(data,"html.parser")
    for link in soup.find_all(href=re.compile("kvartira")):
        link_str=str(link.get('href'))
        if(link_str not in links_set):
            f.write(link_str)
            f.write('\n')
            links_set.add(link_str)
f.close()