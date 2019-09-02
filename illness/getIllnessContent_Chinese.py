#!/usr/bin/evn python
# -*-coding: utf-8 -*-
'''
Created on 2019.08.20
@author: 温钊迪
中文版
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
        self.getUrls()
        self.spider(self.urls)
        self.log.info(u'begin to save the data to folder...\r\n')
        # saveContent(self.items)
        # self.log.info(u'already saved the data to folder...\r\n')

    def getUrls(self):
        # ch = [chr(i) for i in range(65,66)]##获取所有的大写字母
        ch = [r"传染病", r"儿科学", r"耳鼻咽喉疾病", r"肺部疾病", r"妇产科学",
              r"肝脏及胆道疾病", r"肌肉骨骼及结缔组织疾病", r"急救医学",
              r"精神疾病", r"口腔疾病", r"老年病学", r"临床药理学", r"泌尿生殖系统疾病",
              r"免疫学; 过敏性疾病", r"内分泌及代谢紊乱", r"皮肤科疾病", r"神经系统疾病",
              r"损伤; 中毒", r"胃肠功能紊乱", r"心血管疾病", r"血液病学及肿瘤病学", r"眼部疾病", r"营养失调", r"专题"]##获取所有的大写字母

        self.base_url = r'https://www.msdmanuals.com/zh/%E4%B8%93%E4%B8%9A/'
        for i in ch:
            i = urllib.parse.quote(i)
            url = self.base_url+i
            self.urls.append(url)
            # self.log.info(u'添加URL：%s成功 \r\n' % url)

    def getResponseContent(self, url):
        try:
            response = request.urlopen(url)
        except:
            self.log.error(u'获取urL:%s失败\r\n' % url)
        else:
            self.log.info(u'获取urL:%s成功\r\n' % url)
            return response.read()

    def spider(self, urls):
        items = []
        for url in urls:
            results = []
            htmlcontent = self.getResponseContent(url)
            soup = BeautifulSoup(htmlcontent)

            tags = soup.find_all('div',class_='list-view collapsable')##找到每个子链接
            tag = tags[0].find_all('h')
            p = tags[0].find_all('p')
            results.extend(tag)
            results.extend(p)
            for result in results:
                result = BeautifulSoup(str(result), 'lxml')
                result = result.p.a['href']
                if '#' not in result:
                    item = ContentItem()
                    result = result.split('/')
                    item.link = self.base_url+urllib.parse.quote(result[-3])+'/'+urllib.parse.quote(result[-2])+'/'+urllib.parse.quote(result[-1])
                    item.name = result[-3]+'-'+result[-2]+'-'+result[-1]
                    item.content = self.getSingleContent(item.link)
                    self.piplines(item)
        # return items

    def getSingleContent(self,url):
        htmlcontent = self.getResponseContent(url)
        content = []
        if htmlcontent!=None:
            soup = BeautifulSoup(htmlcontent, 'lxml')
            tags = soup.find_all('p')##找到每个段落
            for tag in tags:
                content.append(tag.get_text())
        return content


    def piplines(self, item):
        folder = r'F:\\大学项目\\illness\\chinese\\'##保存路径
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