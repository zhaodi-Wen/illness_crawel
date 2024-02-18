#!/usr/bin/evn python
# -*-coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib import request
import logging
import os
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor

# from saveContent import saveContent

# reload(sys)
# sys.setdefaultencoding('utf-8')
'''这两句是为了避免 UnicodeDecodeError: 'ascii' codec can't decode byte 0x?? in position 1: ordinal not in range(128), 的错误'''
'''这是因为 python没办法处理非ascii编码的，此时需要自己设置将python的默认编码，一般设置为utf8的编码格式。'''


class ContentItem(object):
    """docstring for DouBanItem"""
    fold_letter = None
    name = None
    link = None
    content = None
    title = None
    subTitle = None
    author = None


class GetContent(object):
    """docstring for GetDouBanMovie"""

    def __init__(self):
        self.urls = OrderedDict()
        self.second_urls = []
        self.third_urls = OrderedDict()
        self.definition = OrderedDict()
        self.direction = './data/'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        self.get_urls()
        print(u'begin to save the data to folder...\r\n')
        # self.save_content()
        print(u'already saved the data to folder...\r\n')

    def get_urls(self):
        ch = [chr(i) for i in range(65, 91)]  ##获取所有的大写字母
        ch.append('0')
        # ch = ['0']
        # 一级
        base_url = r'https://www.orpha.net/consor/cgi-bin/Disease_Search_List.php?lng=EN&TAG='
        self.second_urls = [base_url + x for x in ch]
        # 三级URL
        self.get_third_url(self.second_urls)
        # 四级URL
        self.spider()

    def get_third_url(self, urls):

        for url in urls:
            req = request.Request(url=url, headers=self.headers)
            response = request.urlopen(req)
            html_content = response.read()

            soup = BeautifulSoup(html_content, 'lxml')
            tags = soup.find('div', id='content').find('div', id="result-box")
            if tags:
                lis = tags.find_all('li')
                if lis:
                    for li in lis:
                        next_url = "https://www.orpha.net/consor/cgi-bin/" + li.a['href']
                        name = li.a.text  # 3级
                        self.third_urls[name] = next_url
                        print(u'add URL：%s successfully \r\n' % next_url)
        print(self.third_urls)

    def fetch_url_and_save_content(self, name, url):
        req = request.Request(url=url, headers=self.headers)
        response = request.urlopen(req)
        html_content = response.read()

        soup = BeautifulSoup(html_content, 'lxml')
        tags = soup.find('div', {"class": "definition"})
        if tags:
            p_tags = tags.find_all('p')
            if p_tags:
                for p in p_tags:
                    self.definition[name] = p.text
                    self.save_content(name, p.text)

    def spider(self):
        print("starting thread pool")
        with ThreadPoolExecutor(max_workers=20) as executor:
            for name, url in self.third_urls.items():
                executor.submit(self.fetch_url_and_save_content, name, url)

        print(self.definition)

    def save_content(self, name, definition):
        name = name.replace('/', '-')
        print("starting save {}.txt".format(name))
        filename = self.direction + name + ".txt"
        directory = os.path.dirname(filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(filename, 'w', encoding='utf-8') as fp:
            fp.write(definition)
            logging.info(u'save file %s successfully' % filename)


if __name__ == '__main__':
    content = GetContent()
