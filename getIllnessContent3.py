#!/usr/bin/evn python
# -*-coding: utf-8 -*-
'''
Created on 2020.4.21
@author: 温钊迪
网站3
'''

from bs4 import BeautifulSoup
from urllib import request
from mylog import MyLog as mylog
import sys
from importlib import reload
import re
import os
from collections import OrderedDict
from HTMLParser import HTMLParseError
import requests
from itertools import chain

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



# detail = None

class GetContent(object):
    """docstring for GetDouBanMovie"""

    def __init__(self):
        self.urls = OrderedDict()
        self.log = mylog()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        self.getUrls()
        self.items = self.spider(self.urls)
        # print('piplines开始')
        # self.piplines(self.items)
        # self.log.info(u'begin to save the data to folder...\r\n')
        # saveContent(self.items)
        # self.log.info(u'already saved the data to folder...\r\n')


    def getUrls(self):
        # ch = [chr(i) for i in range(65,66)]##获取所有的大写字母
        ch = [chr(i) for i in range(65,85)]##获取所有的大写字母

        #一级
        base_url = r'https://reference.medscape.com/drugs/'
        req = request.Request(url=base_url, headers=self.headers)

        response = request.urlopen(req)
        htmlcontent = response.read()

        soup = BeautifulSoup(htmlcontent, 'lxml')
        tags = soup.find('div', id='drugdbmain2')
        # print(tags)
        if tags:
            lis = tags.find_all('li')
        # print(lis)
        ##二级URL
        secondURL = OrderedDict()

        if lis:
            for li in lis:
                url = li.a['href']
                name = url.split('/')[-1]
                self.log.info(u'添加URL：%s成功 \r\n' % url)
                self.getSubURL((name,url))##2级
                # secondURL[name] = url
                # self.log.info(u'添加URL：%s成功 \r\n' % url)
        # print(secondURL)

        ##三级URL
        # thirdURL = self.getSubURL(secondURL)
        #四级URL
        # forthURL = self.getURLandSpider(thirdURL)


        # self.urls = forthURL
    def getSubURL(self,urls):
        URL = OrderedDict()
        # print(urls)
        dir = urls[0]
        url = urls[1]

        req = request.Request(url=url, headers=self.headers)
        response = request.urlopen(req)
        htmlcontent = response.read()

        soup = BeautifulSoup(htmlcontent, 'lxml')
        tags = soup.find('div', id='drugdbmain2')
        # print(tags)
        if tags:
            lis = tags.find_all('li')
            if lis:
                for li in lis:
                    nextUrl = li.a['href']
                    nextDir = dir+'/'+nextUrl.split('/')[-1]#3级
                    self.log.info(u'添加URL：%s成功 \r\n' % nextUrl)
                    self.getURLandSpider((nextDir,nextUrl))

        return URL
    def getURLandSpider(self,urls):
        dir = urls[0]
        url = urls[1]
        # for dir,url in urls.items():
        req = request.Request(url=url, headers=self.headers)
        response = request.urlopen(req)
        htmlcontent = response.read()

        soup = BeautifulSoup(htmlcontent, 'lxml')
        tags = soup.find('div', id='drugdbmain2')
        # print(tags)
        if tags:
            lis = tags.find_all('li')
            if lis:
                for li in lis:
                    nextUrl = li.a['href']
                    nextDir = dir+'/'+nextUrl.split('/')[-1]
                    # URL[dir+'/'+nextDir] = nextUrl
                    self.log.info(u'添加URL：%s成功 \r\n' % nextUrl)
                    self.spider((nextDir,nextUrl))

    def getResponseContent(self, url):
        try:
            req = request.Request(url=url, headers=self.headers)

            response = request.urlopen(req)
        except:
            self.log.error(u'获取urL:%s失败\r\n' % url)
        else:
            self.log.info(u'获取urL:%s成功\r\n' % url)
            return response.read()

    def spider(self, urls):
        print("in urls")
        dir = urls[0]
        url = urls[1]
        item = ContentItem()

        first_dir = dir.split('/')[0]
        second_dir = dir.split('/')[1]
        third_dir = '-'.join(dir.split('/')[2].split('-')[:-1])

        first_directory = '../medscape/'+first_dir
        if not os.path.exists(first_directory):
            os.mkdir(first_directory)

        second_directory = first_directory+'/'+second_dir
        if not os.path.exists(second_directory):
            os.mkdir(second_directory)

        filename = second_directory+'/'+third_dir+'.txt'
        item.name = filename


        htmlcontent = self.getResponseContent(url)

        if htmlcontent:
            soup = BeautifulSoup(htmlcontent, 'lxml')

            content = soup.find('div', class_ = 'article-content')##找到每个子链接
            # print(content)

        #找到子标题
            menus = content.find('div',class_ = 'sections-nav').find_all('li')
            topDiv = content.find('div',class_ = 'drugdbsectioncontent drug')
            newcontent = []

            patt1 = re.compile(r'<p>(.*?)</p>|<li>(.*?)</li>|<h3>(.*?)</h3>|<h4>(.*?)</h4>', re.S)
            for i in range(1,len(menus)):
                id = 'content_'+menus[i].a['href'][1:]
                subDiv = topDiv.find('div',id = id)
                subcontent = patt1.findall(str(subDiv))
                signs = {'&lt;':'<','&gt;':'>','&amp;':'&'}
                for x in subcontent:
                    x = "".join(x)+'\n'
                    for css_sign,sign in signs.items():
                        x = x.replace(css_sign,sign)
                    newcontent.append(x)

            item.content =  newcontent
            self.piplines(item)
        # except HTMLParseError:
        #     print("访问错误,无法找到对应tag")
        #     pass
        # except requests.exceptions.RequestException as e:  # This is the correct syntax
        #     print("网络问题 "+e)
        #     pass



    def piplines(self, item):
        # folder = r'F:\\大学项目\\illness\\medscape\\'+item.+'\\'##保存路径
        # if not os.path.exists(folder):
        #     os.mkdir(folder)
        print("开始写入文件")


        # print(item.name)
        filename = item.name
        with open(filename, 'w',encoding='utf-8') as fp:
            # fp.write(item.name)
            for x in item.content:
                fp.write(x)
            self.log.info(u'保存文件%s成功' % (item.name))


if __name__ == '__main__':
    content = GetContent()
