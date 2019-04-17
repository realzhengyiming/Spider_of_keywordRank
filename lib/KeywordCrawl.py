#这个是用来爬取关键字的
#爬取关键字的站点是百度的风云榜单那儿地址是：
#coding=utf-8
# coding=utf-8
import random
import time
import pymysql  # 导入 pymysql
import re
import requests
from bs4 import BeautifulSoup
from lxml import etree
import requests  # 后面这儿可以换成ai什么的东西
import pymysql  # 导入 pymysql
import time


# 打开数据库连接


def makesoup(url):  # 这儿是按页来打开的
    """
    获取网站的soup对象，#看看还能不能增加代理的东西，进来
    """
    my_headers = [
        'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30',
        'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)',
        'Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)']
    headers = {"User-Agent": random.choice(my_headers)}
    html = requests.get(url, headers=headers, allow_redirects=True)
    # html =  html.text  # 不允许你跳转，就访问这个就是了，改成request后就是这个样子

    html.encoding = 'gb2312'
    # print(html)
    # html.encoding="utf-8"
    soup = BeautifulSoup(html.text, "html.parser")  # 原来是lxml 缓存的问题吗，就缺少了那些东西
    time.sleep(1)  # 推迟2s
    return soup


def run(url):

    db = pymysql.connect(host="localhost", user="root", passwd="1314520Zym@!", db="spiderInfo", port=3306,
                         charset="utf8")
    # 使用cursor()方法获取操作游标
    cur = db.cursor()
    soup = makesoup(url)  # 这儿是爬取的url的地方
    # print (soup)
    # print(soup.title.encode('utf-8'))
    # print (soup)
    alll = soup.find_all("a", attrs={"class": "list-title", "target": "_blank", "href": True})
    for i in alll:
        # print(i.text)  #输出的是unicode
        # print(i)

        word = i.text
        # print(type(word))
        sql = "insert into Keyword (word) values ('%s');" % i.text
        try:
            cur.execute(sql)  # 执行sql语句
            print("插入成功" + sql)
        except Exception as e:
            print(e)
    #
    print (len(soup.find_all("a", attrs={"class": "list-title", "target": "_blank", "href": True})))
    #
    db.commit()  # 全部搞定后再提交
    db.close()
    print(len(alll))
    # time.sleep(60 * 60 * 1)  # 每两小时更新一次把

# 1.查询操作
# 编写sql 查询语句  user 对应我的表名
# sql = "select * from Keyword"
# insert_sql= "insert into Keyword values ("+word+");"
# 关闭连接    先来实现增删查改
if __name__=="__main__":
    urlList = [
        'http://top.baidu.com/buzz?b=341&c=513&fr=topbuzz_b1_c513',
        # 'http://top.baidu.com/buzz?b=42&c=513&fr=topbuzz_b341_c513',
        # 'http://top.baidu.com/buzz?b=342&c=513&fr=topbuzz_b42_c513',
        # 'http://top.baidu.com/buzz?b=344&c=513&fr=topbuzz_b342_c513',
        # 'http://top.baidu.com/buzz?b=11&c=513&fr=topbuzz_b344_c513',
        # 'http://top.baidu.com/buzz?b=260&c=9&fr=topcategory_c9',
        # 'http://top.baidu.com/buzz?b=1566&fr=topindex',
        # 'http://top.baidu.com/buzz?b=1627&c=15&fr=topbuzz_b1566',
        # 'http://top.baidu.com/buzz?b=26&c=1&fr=topcategory_c1',
        # 'http://top.baidu.com/buzz?b=339&c=1&fr=topbuzz_b340_c1',
        # 'http://top.baidu.com/buzz?b=442&c=5&fr=topcategory_c5',
        # 'http://top.baidu.com/buzz?b=443&c=5&fr=topbuzz_b442_c5',
        # 'http://top.baidu.com/buzz?b=446&c=5&fr=topbuzz_b443_c5',
        # 'http://top.baidu.com/buzz?b=447&c=5&fr=topbuzz_b446_c5',
        # 'http://top.baidu.com/buzz?b=1579&c=11&fr=topcategory_c11',
        # 'http://top.baidu.com/buzz?b=24&c=11&fr=topbuzz_b1579_c11',
        # 'http://top.baidu.com/category?c=16&fr=topbuzz_b444_c5',
        # 'http://top.baidu.com/buzz?b=451&c=16&fr=topbuzz_b524_c16',
        # 'http://top.baidu.com/buzz?b=450&fr=topboards',
        'http://top.baidu.com/buzz?b=12&c=11&fr=topbuzz_b270_c11'
        'http://top.baidu.com/buzz?b=270&c=11&fr=topbuzz_b12_c11',
        'http://top.baidu.com/buzz?b=1434&c=11&fr=topbuzz_b270_c11',
        'http://top.baidu.com/buzz?b=1540&c=18&fr=topcategory_c18',
        'http://top.baidu.com/buzz?b=1543&c=18&fr=topbuzz_b1540_c18',
        'http://top.baidu.com/buzz?b=1544&c=18&fr=topbuzz_b1543_c18',
        'http://top.baidu.com/buzz?b=1541&c=18&fr=topbuzz_b1544_c18',
        'http://top.baidu.com/buzz?b=1545&c=18&fr=topbuzz_b1541_c18',
        'http://top.baidu.com/buzz?b=454&fr=topbuzz_b1545_c18',
        'http://top.baidu.com/buzz?b=257&fr=topbuzz_b454',
        'http://top.baidu.com/buzz?b=1570&fr=topbuzz_b257',
        'http://top.baidu.com/buzz?b=1569&c=9&fr=topbuzz_b1570'






    ]
    for url in urlList:
        run(url)


