#!/usr/bin/evn python
# -*-coding: utf-8 -*-
'''
Created on 2019.08.17
@author: 温钊迪
英文版
'''

from bs4 import BeautifulSoup
from urllib import request
from mylog import MyLog as mylog
import sys
from importlib import reload
import re
import os
# from saveContent import saveContent

reload(sys)
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
        self.urls = []
        self.log = mylog()
        self.getUrls()
        self.items = self.spider(self.urls)
        print('piplines开始')
        # self.piplines(self.items)
        self.log.info(u'begin to save the data to folder...\r\n')
        # saveContent(self.items)
        # self.log.info(u'already saved the data to folder...\r\n')

    def getUrls(self):
        # ch = [chr(i) for i in range(65,66)]##获取所有的大写字母
        ch = [chr(i) for i in range(65,85)]##获取所有的大写字母

        base_url = r'https://www.mayoclinic.org/diseases-conditions/index?letter='
        for i in ch:
            url = base_url+i
            self.urls.append(url)
            self.log.info(u'添加URL：%s成功 \r\n' % url)


    def getResponseContent(self, url):
        try:
            response = request.urlopen(url)
        except:
            self.log.error(u'获取urL:%s失败\r\n' % url)
        else:
            self.log.info(u'获取urL:%s成功\r\n' % url)
            return response.read()

    def spider(self, urls):
        print("in urls")
        items = []
        print(urls)
        for url in urls:
            htmlcontent = self.getResponseContent(url)

            # print(htmlcontent)
            soup = BeautifulSoup(htmlcontent, 'lxml')
            tags = soup.find_all('div',class_='index')##找到每个子链接

            if tags:
                for tag in tags:
                    # print("tag 是",tag)
                    lis = tag.find_all('li')
                    for li in lis:
                        if li.a['href']!=None:
                            item = ContentItem()
                            href = li.a['href']
                            link = 'https://www.mayoclinic.org'+href
                            print(link)
                            content = self.getSubUrl(link)
                            if content:
                                name = re.sub('(|)','',link.split('/')[-3])
                                item.link = link+'/'+name
                                item.name = name
                                item.fold_letter = url[-1]
                                print(item.name)
                                item.content = content
                                # item.author, item.content = self.getSingleContent(item.link)
                                # items.append(item)
                                self.piplines(item)
                                items.append(item)
                            else:
                                print("link是",link)
                                item.link = link
                                item.name = href.split('/')[-1]
                                item.author,item.content = self.getSingleContent(item.link)
                                if item.content!=None and item.author!=None:
                                    items.append(item)
                        # self.log.info(self.log.info(u'获取名字为%s 数据成功' % (item.name)))
        return items
    def getSubUrl(self,url):
        htmlcontent = self.getResponseContent(url)
        subUrl = []
        content = ""
        if htmlcontent != None:
            print("进入子程序")
            soup = BeautifulSoup(htmlcontent, 'lxml')
            # print(soup.find('div',class_='chapter__main'))
            # print("soup ",soup)
            patt = re.compile(r'<p>(.*?)</p>|<li>(.*?)</li>|<h2>(.*?)</h2>|<h3>(.*?)</h3>|<strong>(.*?)</strong>', re.S)
            patt2 = re.compile('<[^>]*>')#获取标签后的内容，6666
            chapter_mains = soup.find('div',class_="content")
            chapter_mains = patt.findall(str(chapter_mains))
            # chapter_columns = soup.find_all('div',class_='chapter__column')
            if chapter_mains:
                for chapter_main in chapter_mains:

                    chapter_main = "".join(chapter_main)
                    chapter_main = patt2.sub("",chapter_main)
                    # print(chapter_main)
                    content+=chapter_main
                    content+='\n'
        return content
    def getSingleContent(self,url):
        htmlcontent = self.getResponseContent(url)
        content = []
        author = None
        if htmlcontent!=None:
            # print(htmlcontent)
            soup = BeautifulSoup(htmlcontent, 'lxml')
            h3 = soup.find()
            author = soup.find('strong',attrs={'class':'topic__label topic__label--author'})
            if author!=None:
                author = author.get_text()
            # soup.find('strong', attrs={'class': 'topic__label topic__label--author'}).a.get_text()
            tags = soup.find_all('p')##找到每个段落
            for tag in tags:
                # print('内容是 ',tag.get_text())
                content.append(tag.get_text())
        return author,content


    def piplines(self, item):
        folder = r'F:\\大学项目\\illness\\English\\'+item.fold_letter+'\\'##保存路径
        if not os.path.exists(folder):
            os.mkdir(folder)
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