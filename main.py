from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyautogui
browser = webdriver.Firefox(executable_path=r'/usr/local/bin/geckodriver')



pages =range(1,10)
base_url = 'https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&p='
for page in pages:
    url = 'https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&p='+str(page)
    sada = browser.get(url)
    time.sleep(3)
    source = browser.page_source
    soup = BeautifulSoup(source, 'html.parser')
    ActionChains(browser).context_click().perform()
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('down')
    if page!=1:
        pyautogui.press('down')
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.write('p'+str(page), interval=0.25)  
    pyautogui.press('enter')





'''

url = 'https://www.google.co.il/search?q=eminem+twitter'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
# header variable
headers = { 'User-Agent' : user_agent }
# creating request
req = urllib2.Request(url, None, headers)
# getting html
html = urllib2.urlopen(req).read()





#with open("index.html", encoding="utf-8") as fp:
#    soup = BeautifulSoup(fp,"html.parser")

#r = requests.get("https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1")
##session = requests.Session()
##r = requests.get("https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&p=2")

#r = urllib.request.urlopen("https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&p=2")

soup = BeautifulSoup(html.content,"html.parser")
print(soup)
elements=soup.find_all('li',class_="item-params-list-item")

for el in elements:
    print(el.text)
'''