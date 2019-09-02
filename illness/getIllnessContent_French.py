#!/usr/bin/evn python
# -*-coding: utf-8 -*-
'''
Created on 2019.08.25 00:19
@author: 温钊迪
法语版
'''
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
#!/usr/bin/evn python
# -*-coding: utf-8 -*-
'''
Created on 2017Äê8ÔÂ17ÈÕ
@author: WZD06
'''

from bs4 import BeautifulSoup
from urllib import request
from mylog import MyLog as mylog
import sys
import urllib.parse
from importlib import reload
import re
# from saveContent import saveContent

reload(sys)
# sys.setdefaultencoding('utf-8')
'''这两句是为了避免 UnicodeDecodeError: 'ascii' codec can't decode byte 0x?? in position 1: ordinal not in range(128), 的错误'''
'''这是因为 python没办法处理非ascii编码的，此时需要自己设置将python的默认编码，一般设置为utf8的编码格式。'''


class ContentItem(object):
    """docstring for DouBanItem"""

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
        self.urls = []
        self.log = mylog()
        self.get_url_selenium()
        # self.spider(self.urls)
        self.log.info(u'begin to save the data to folder...\r\n')
        # saveContent(self.items)
        # self.log.info(u'already saved the data to folder...\r\n')
    def get_url_selenium(self):
        option = webdriver.FirefoxOptions()
        option.set_headless()
        br = webdriver.Firefox(firefox_options=option)
        self.base_url = "https://www.msdmanuals.com/fr/professional"
        wb = webdriver.Firefox()
        wb.get(self.base_url)
        for i in range(1,31):
            print("第{}个链接".format(i))
            try:
                wb.find_element_by_xpath("/html/body/div[1]/div[4]/section/div[2]/div[{}]/a".format(i)).click()
                wb.current_window_handle
                time.sleep(2)
                p = wb.find_element_by_xpath('/html/body/div[1]/div[4]/section/div[2]/div[1]')
                p = wb.find_elements_by_class_name('modalspine__toplevel')
                if p:
                    for x in p:
                        item = ContentItem()
                        item.link = wb.find_element_by_link_text(x.text).get_attribute('href')
                        item.name = x.text
                        item.content = self.getSingleContent(item.link)
                        # self.piplines(item)
                        self.spider(item)##进入里面解析


            except:
                continue

    def getResponseContent(self, url):
        try:
            response = request.urlopen(url)
        except:
            self.log.error(u'获取urL:%s失败\r\n' % url)

        else:
            self.log.info(u'获取urL:%s成功\r\n' % url)
            return response.read()

    def spider(self, item):
        results = []
        htmlcontent = self.getResponseContent(item.link)
        soup = BeautifulSoup(htmlcontent)
        tags = soup.find_all('div',class_='chapter__column')##找到每个子链接
        tags.extend(soup.find_all('li',class_='chapter__link'))
        if tags:
            for tag in tags:
                A = tag.find_all('li', class_='chapter__link')  ##找到每个子链接
                B = tag.find_all('li',class_='chapter__link--single')
                results.extend(A)
                results.extend(B)
            for result in results:
                # tag = result.find_all('href')
                # p = tags[0].find_all('p')
                # results.extend(tag)
                # results.extend(p)
                # print("result s  ",result)
                # result = BeautifulSoup(str(result), 'lxml')
                href = result.a['href']
                # print("result ",href)
                if '#' not in href:
                    item = ContentItem()
                    result = href.split('/')
                    item.link = 'https://www.msdmanuals.com/fr/professional/'+urllib.parse.quote(result[-3])+'/'+urllib.parse.quote(result[-2])+'/'+urllib.parse.quote(result[-1])
                    item.name = result[-2]+'-'+result[-1]
                    item.content = self.getSingleContent(item.link)
                    self.piplines(item)
        else:
            self.piplines(item)

        # return items

    def getSingleContent(self,url):
        htmlcontent = self.getResponseContent(url)
        content = []
        if htmlcontent!=None:
            soup = BeautifulSoup(htmlcontent, 'lxml')
            tags = soup.find_all('div',class_="para")##找到每个段落
            tags = soup.find_all('p')##找到每个段落

            for tag in tags:
                content.append(tag.get_text())
        return content


    def piplines(self, item):
        folder = r'F:\\大学项目\\illness\\French\\'##保存路径
        print("开始写入文件")
        print(item.name)
        filename = folder+item.name+'.txt'
        with open(filename, 'w',encoding='utf-8') as fp:
            fp.write(item.name)
            for x in item.content:
                fp.write(x)
            self.log.info(u'保存文件%s成功' % (item.name))


if __name__ == '__main__':
    content = GetContent()
