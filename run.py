#!/usr/bin/env python
# coding: utf-8

# In[7]:


from bs4 import BeautifulSoup as Soup
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
import urllib.request as url
from validator_collection import checkers
import os

def scrapeIG(USERNAME, PASSWORD):
    os.mkdir("images")
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path=r'C:\Users\walee\Desktop\insta_scraper\geckodriver.exe', )
    driver.get(f'https://www.instagram.com/accounts/login/?next=%2F{USERNAME}%2F&source=desktop_nav')
    sleep(1)
    driver.find_element_by_name("username").send_keys(USERNAME)
    driver.find_element_by_name("password").send_keys(PASSWORD)
    driver.find_element_by_xpath("/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div/div[3]/button/div").click()
    sleep(5)
    driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div/div/button").click()

    photos = []
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
        soup = Soup(driver.page_source, "html.parser")
        for x in soup.findAll('img'):
            if x not in photos:
                photos.append(x)


    count = 1
    for i in photos:
        if(checkers.is_url(i['src'])):
            url.urlretrieve(i['src'], f'images/{count}.jpg')
            count =  count + 1

    
if __name__=="__main__":

    USERNAME=input("enter your IG username: ")
    PASSWORD=input("enter your IG password (trust me its safe): ")
    print("fetching.. this may take a while!")
    
    try:
        scrapeIG(USERNAME, PASSWORD)
    except:
        print("Oh oh, we ran into an error. Please check your credentials.")




# In[ ]:




