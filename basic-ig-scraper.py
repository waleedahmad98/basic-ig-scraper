#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup as Soup
import json, random, re, requests, time
import urllib.request as url
import os
from shutil import rmtree as removeDIR
from tqdm.auto import tqdm
import PySimpleGUI as sg


# In[10]:


class instagramProfileFetch:
    def __init__(self, username, password, window):
        self.username = username
        self.password = password
        self.base_url = 'https://www.instagram.com/'
        self.login_url = self.base_url + 'accounts/login/ajax/'
        self.session = requests.Session()
        self.session.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36' }
        self.session.headers.update({'Referer': self.base_url})
        self.all_posts = []
        self.count = 0
        self.window = window
        
    def login(self):
        self.window['-OUTPUT-'].update('Logging in...')
        self.window.refresh()
        req = self.session.get(self.base_url)    
        soup = Soup(req.content, 'html.parser')

        string_script =  [str(s) for s in soup.findAll('script') if 'window._sharedData' in str(s)][0]
        parsed = "".join(string_script.split(' = ')[1:]).strip(';</script>')

        data = json.loads(parsed)
        csrf = data['config'].get('csrf_token')

        payload = {
            'username': f'{self.username}',
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{self.password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        with self.session as s:
            r = s.post(self.login_url,data=payload,headers={
                "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
                "referer": "https://www.instagram.com/accounts/login/",
                "x-csrftoken":csrf
            })
        
    def start(self):
        try:
            removeDIR("images")
            removeDIR("videos")
        except:
            pass

        os.mkdir("images")
        os.mkdir("videos")

        resp = self.session.get(self.base_url + self.username)
        soup = Soup(resp.text, 'html.parser')
        string_script =  [str(s) for s in soup.findAll('script') if 'window._sharedData' in str(s)][0]
        parsed = "".join(string_script.split(' = ')[1:]).strip(';</script>')
        data = json.loads(parsed)
        self.firstLoop(data)
        
    def firstLoop(self, data):
        self.window['-OUTPUT-'].update('Fetching posts... ')
        self.window.refresh()
        posts = data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
        for post in posts:
            self.all_posts.append(post)
            
        self.user_id = data['entry_data']['ProfilePage'][0]['graphql']['user']['id']
        self.has_next = data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
        self.end_cursor = data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        self.fullLoop()
        
    def fullLoop(self):
        while self.has_next == True:
            resp = self.session.get('https://www.instagram.com/graphql/query/?query_hash=02e14f6a7812a876f7d133c9555b1151&variables={"id":"' + self.user_id + '","first":12,"after":"' + self.end_cursor + '"}')
            data = json.loads(resp.text)
            posts = data['data']['user']['edge_owner_to_timeline_media']['edges']
            for post in posts:
                self.all_posts.append(post)

            self.has_next = data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
            self.end_cursor = data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        self.downloadAllPosts()
    
    def downloadAllPosts(self):
        self.count_img = 0
        self.count_video = 0

        self.updated_all_posts = []

        for i in self.all_posts:
            self.updated_all_posts.append(i)

        for item in self.all_posts:
            if item['node']['__typename'] == 'GraphSidecar':
                for e in item['node']['edge_sidecar_to_children']['edges']:
                    self.updated_all_posts.append(e)

        if len(self.updated_all_posts) == 0:
            self.window['-OUTPUT-'].update('No posts found! Is login correct?')
            self.window.refresh()


        for item in self.updated_all_posts:
            self.window['-OUTPUT-'].update(f'Downloading {self.count_img + self.count_video} / {len(self.updated_all_posts)}...')
            self.window.refresh()
            if item['node']['__typename'] == 'GraphImage':
                url.urlretrieve(item['node']['display_url'], 'images/'+str(self.count_img)+".jpg")
                self.count_img += 1
            if item['node']['__typename'] == 'GraphVideo':
                url.urlretrieve(item['node']['video_url'], 'videos/'+str(self.count_video)+".mp4")
                self.count_video += 1
        self.window['-OUTPUT-'].update('Finished!')
        self.window.refresh()
        self.window.close()
        


# In[11]:


class GUI:
    def __init__(self):
        self.layout = [[sg.Text('Enter Instagram Username:')],      
                 [sg.InputText(key='-USRN-')],
          [sg.Text('Enter Instagram Password:')],      
                 [sg.InputText(key='-PSWD-')],
                 [sg.Button("Start"), sg.Button("Quit")],[sg.Text('Please enter correct credentials!', key='-OUTPUT-')]]      
        self.window = sg.Window('IG Fetch by Waleed Ahmad', self.layout)    
        
        while True:
            event, values = self.window.read() 
            if event == sg.WIN_CLOSED or event == 'Quit': 
                self.window.close()
                break
            if event == 'Start':
                self.username = values['-USRN-']
                self.password = values['-PSWD-']
                main(self.username, self.password, self.window)
            
        


# In[12]:


def main(username, password, window):
    fetcher = instagramProfileFetch(username, password, window)
    fetcher.login()
    fetcher.start()


# In[13]:


if __name__ == '__main__':
    gui = GUI()

