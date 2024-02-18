# illness_crawel
## 2019.08.19
爬取网站https://www.msdmanuals.com 的中文版，英文版和法语版内容</br>
使用了scrapy框架和selenium框架</br>

## 2020.02.2
添加网页r'https://medlineplus.gov/ency/ 的爬取</br>
## 2020.04.23
添加了一个网页的https://reference.medscape.com/drug/ 的爬取</br>
本来打算使用dict将所有的网页的路径(保存在本地)和他的url形成一个字典,然后最后遍历这整个大dict下载文本</br>
后面发现整个大的dict全部添加完要比较长的时间，需要进行4个大的for循环，</br>
最后决定不保留dict,使用tuple记录每个路径和url,然后下载文本。
## 2024.02.18
添加了一个网页的https://www.orpha.net/consor/cgi-bin/Disease_Search_List.php?lng=EN 的爬取</br>
将所有的子url爬取后，使用dict保存 name 和 url,方便下载的时候以 name 为文件名保存爬取内容。使用线程池,边爬取边下载。

## 小tips
爬取网页按照顺序爬取的一个特别好的写法是
```
patt1 = re.compile(r'<p>(.*?)</p>|<li>(.*?)</li>|<h3>(.*?)</h3>|<h4>(.*?)</h4>', re.S)
subcontent = patt1.findall(str(subDiv))

```
原理是先用正则表达式将所要爬取的内容的tags全部先complile设置好,</br>
然后使用findall查找已经解析出来的网页部分,这样获得的就是按照顺序的文本。
