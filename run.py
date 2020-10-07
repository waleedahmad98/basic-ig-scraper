#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup as Soup
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
import urllib.request as url
import os

def scrapeIG(USERNAME, PASSWORD):
    os.mkdir("images")
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path=r'PATH_TO_GECKO', )
    driver.get(f'https://www.instagram.com/accounts/login/?next=%2F{USERNAME}%2F&source=desktop_nav')
    sleep(1)
    driver.find_element_by_name("username").send_keys(USERNAME)
    driver.find_element_by_name("password").send_keys(PASSWORD)
    driver.find_element_by_xpath("/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div/div[3]/button/div").click()
    sleep(10)
    driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div/div/button").click()

    links = []
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(10)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

        soup = Soup(driver.page_source, "html.parser")
        for x in soup.findAll('a'):
            if x['href'] not in links and '/p/' in x['href']:
                links.append(x['href'])
    
    content = []
    for link in links:
        driver.get(f'http://www.instagram.com{link}')
        sleep(1)
        soup = Soup(driver.page_source, 'html.parser')
        vids = soup.findAll('video')
        if len(vids) > 0:
            content.append(vids[0]['src'])
        else:
            content.append(soup.findAll('img')[1]['src'])
        
    for en, c in enumerate(content):
        url.urlretrieve(c, 'images/'+str(en)+"."+getType(c))
    
def getType(text):
    return text.split("?")[0].split(".")[-1]
    


# In[ ]:


if __name__=="__main__":

    USERNAME=input("enter your IG username: ")
    PASSWORD=input("enter your IG password (trust me its safe): ")
    print("fetching.. this may take a while!")
    
   # try:
    photos = scrapeIG(USERNAME, PASSWORD)
    print("Completed!")
    except:
        print("Oh oh, we ran into an error. Please check your credentials.")
    


# In[ ]:




