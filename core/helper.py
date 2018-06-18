import random
import re
import requests

from .useragents import USERAGENTS
from django.http import JsonResponse


class Crawling:

    def __init__(self, url, depth):
        self.next_level = []
        self.current_level = [url]
        self.depth = depth
        self.global_scrapped_list = []
        self.scrapped_data = []
        self.headers = {}
        self.temp_store = {}

    def get_headers(self):
        # get headers
        user_agent = random.choice(USERAGENTS)
        self.headers =  {'User-Agent': user_agent}
        return

    def get_proxy():
        # get proxy
        pass
    
    def get_images(self):
        # get images logic
        # json -> images self.temp_store
        data = []
        images = re.findall('img src="([^"]+)"', self.temp_store)
        collective_image = []
        try:
            hosturl = self.host.replace('https://', '').replace('http://', '').split('/')[0]
        except:
            hosturl = ''
        for image in images:
            if image.startswith("/"):
                collective_image.append(f'https://{hosturl}{image}')
            else:
                collective_image.append(image)
        return collective_image
    
    def get_host_port(self, url):
        # return host and port
        if url.startswith("http://") or url.startswith("https://"):
            self.host = url
        else:
            return
    
    def requester(self):
        # url request
        self.get_headers()
        print('requesting data...')
        print('------------------------------------------------')
        print(f'{self.host} - depth {self.depth}')
        print('------------------------------------------------')
        res = requests.get(url = self.host, headers = self.headers)
        img = []
        if res.status_code == 200:
            self.temp_store = res.text
            img = self.get_images()
        else:
            print ("error response")
        self.global_scrapped_list.append(self.host)
        return img
    
    def bifrost(self):
        for url in self.current_level:
            self.host = None
            level = []
            images = []
            nxt = []
            self.get_host_port(url)
            if self.host:
                data = self.requester()
                nxt = re.findall('href="(.*?)"', self.temp_store)
            [images.append(dat) for dat in data]
            [level.append(ni) for ni in nxt]
        unique_nxt = list(set(level))
        unique_img = list(set(images))
        self.scrapped_data.append({'level': self.depth, 'images': unique_img })
        print (f'remaining :{len(unique_nxt)}')
        for link in unique_nxt:
            if link not in self.global_scrapped_list and 'http' in link:
                self.next_level.append(link)
        self.current_level = self.next_level if self.next_level else []
        self.next_level = []
        self.depth = self.depth - 1
        if self.depth and self.current_level:
            print (f'depth version {self.depth}')
            self.bifrost()
        else:
            print ('Done scraping')
            return self.scrapped_data
        
    
    