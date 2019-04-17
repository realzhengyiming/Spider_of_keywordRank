#coding=utf-8
#这个是用来从搜索引擎结果链接中提取真实的url
'''
# (已修复完成）这三个提取的还得再看看怎么回事，。逐个花时间来调试一下才可以哇
'''

import random
import re
import time

from lib.tools.setTimeDoit import clock  #因为查找路径是从那儿开始的



import requests,lxml
from bs4 import BeautifulSoup
from lxml import etree

from lib.proxyStruct import ProxyStruct
from lib.tools.CookSoup import CookSoup

#目前这儿好像全都使用了代理
class ExtractUrl(ProxyStruct) :  #只是为了继承它的  代理的部分而已。。。这样用也许不太好，再封装出来？
    def __init__(self): #暂时是这几个header
        super().__init__() #如果还有新增加的属性直接后面再添加就可以了,所以以后改的话，改这儿就可以了

        my_headers = [
            'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30',
            'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)',
            'Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)']

        self.headers = {"User-Agent": random.choice(my_headers)}  #是常量的话应该放在这儿才对


    #这儿也是可以设置代理ip地址的，设置了个超时处理，循环try，应该没问题
    # @clock
    def getRealurl(self,tempUrl) ->str: #返回的这个也是realurl才对，这个是没代理的，所以要小心一点儿
        time.sleep(1) #这儿也设置了1秒的超时时间
        # print(self.setRandomProxy())
        self.setProxy(self.setRandomProxy())  # 每次都使用不同的代理
        # print(self.proxyAdress)
        # self.proxyAdress = None # 不用代理
        proxies = {'http':self.proxyAdress,"https":self.proxyAdress}  #, 'https': 'http://localhost:8888'

        if ((tempUrl.find("http://www.so.com/link?") != -1) or (
                tempUrl.find("https://www.so.com/link?") != -1)):  # 提取360的真实url
            print("提取360的真实url中")

            response = None
            while(response==None): #如果确实是空那就反复切换代理，知道提取出真实的链接
                print("尝试提取中360")
                try:
                    # print("进行第一次情")  #设置超时时间 30s
                    response = requests.get(tempUrl, headers=self.headers, allow_redirects=True,proxies=proxies,timeout=30)  #360这个比较特殊，跳转两次才可以的
                except Exception as e:
                    # time.sleep(1)  #需要设置这个时间吗
                    print("请求失败")
                    print(tempUrl)
                    # todo 这个会不会改链接哦
                    self.setProxy(self.setRandomProxy()) #切换一下代理然后继续跑
                    proxies = {'http': self.proxyAdress, "https": self.proxyAdress}  # , 'https': 'http://localhost:8888'
                    # response = requests.get(tempUrl, headers=self.headers, allow_redirects=True,proxies=proxies)  #360这个比较特殊，跳转两次才可以的

            if (response.status_code == 200):
                # print("200")
                html = etree.HTML(response.text)  # 200的时候可以抓出来那个网址
                tempUrl = html.xpath('/html/head/script/text()')[0]
                tempUrl = tempUrl.split('"')[1]
                return tempUrl
            elif (response.status_code == 302):
                # print(302)
                # print(response.text)
                realUrl = response.headers.get('location')
                # return realUrl
                return realUrl

        elif (tempUrl.find("https://www.baidu.com") != -1 or tempUrl.find(
                "http://www.baidu.com") != -1):  # 这儿是百度的提取真实链接
            response=None
            while(response==None):
                try:
                    response = requests.get(tempUrl, headers=self.headers, allow_redirects=False,proxies=proxies,timeout=30)
                except Exception as e:
                    print(e)
                    self.setProxy(self.setRandomProxy()) #切换一下代理然后继续跑
                    proxies = {'http': self.proxyAdress, "https": self.proxyAdress} #然后就循环回去try，没问题了，这样
                    # response = requests.get(tempUrl, headers=self.headers, allow_redirects=False,proxies=proxies)


            if response.status_code == 200:  # 解析部分
                realUrl = re.search(r'URL=\'(.*?)\'', response.text.encode('utf-8'), re.S)  # 直接找到那个页面
                return realUrl
            elif response.status_code == 302:  # 302是重定向
                realUrl = response.headers.get('location')
                return realUrl
            else:
                print('No URL found!!')
                return "No URL found!!"

        elif (tempUrl.find("https://www.sogou.com/") != -1 or tempUrl.find("http://www.sogou.com/") != -1):

            response = None
            while(response==None):
                try:
                    response = requests.get(tempUrl, headers=self.headers, allow_redirects=False,proxies=proxies,timeout=30)  # 这个再次封装一下 ，体育课的时候
                except Exception as e:
                    print(e)
                    self.setProxy(self.setRandomProxy()) #切换一下代理然后继续跑
                    proxies = {'http': self.proxyAdress, "https": self.proxyAdress}  #切换代理
                    # response = requests.get(tempUrl, headers=self.headers, allow_redirects=False,proxies=proxies)  # 这个再次封装一下 ，体育课的时候


            if response.status_code == 200:  # 这个就是进入成功个
                # print(200)
                html = etree.HTML(response.text)  # 200的时候可以抓出来那个网址
                realUrl = html.xpath('//noscript/META/@content')  # sogou有两种跳转页面，结构偶尔是第一种偶尔是第二种于是这样解决了
                if len(realUrl) == 0:
                    realUrl = html.xpath('//script/text()')[0]
                    realUrl = realUrl.split('"')[1]
                if realUrl == "redirect_url":
                    realUrl = html.xpath('//a[@id="redirect_url"]/@href')[0]

                # realUrl = realUrl.split('"')[1]
                return realUrl
            elif response.status_code == 302:  # 302是重定向,也算是修复完毕了
                # print(302)
                # print(tempUrl.content)
                # cooker.makesoup(tempUrl,"sougou",None)

                url = response.headers.get('location')
                html = requests.get(url, allow_redirects=False,proxies=proxies).text
                # print(html)
                soup = BeautifulSoup(html, "lxml")
                realUrl = soup.find("script").text.split('"')[1]

                return realUrl
            else:
                pass
                print('No URL found!!')
            pass
        else:
            return tempUrl  #都没有的话就直接返回这个tempUrl

@clock
def testTime():
    rawUrl = "https://www.baidu.com/link?url=JfdUQP5Y6tg3LYAQgNAbaqwTBqQouaOjkQcjQlj6OR_9Ld88AGHSF5tgerCGd000xxUorZV6X10EpccTIj6JCa&amp;wd=&amp;eqid=fcca4ab4000108fd000000065b9bb859"  # 百度的，<a data-click="{
    rawUrl = "https://www.sogou.com/link?url=DOb0bgH2eKjRiy6S-EyBciCDFRTZxEJg7ZfH5mjf_xlIK9ahPqNmMGJBCCZgvz6_EjM3Qz2A_5Y."  # 搜过的
    rawUrl = "http://www.so.com/link?m=aBQ7avNa3NRS%2F1mmMMER%2FjrB0ypp9pqluBezA9Yg9BM6enLo%2BjntfllTcaS%2F%2FA1FtG8mCcivMvV%2FVRqxolp6kOVqytDG06IZB%2F5wnVo1oP04lTTB3"  # 360的
    ex = ExtractUrl()
    urllist = []
    for i in range(1000):
        print()
        print(i)
        realUrl = ex.getRealurl(rawUrl)
        if (realUrl != None):
            print(realUrl)
            urllist.append(realUrl)
    print("结束了,总数量有")
    print(len(urllist))
    print(ex.getRealurl(rawUrl))
    print(ex.proxyAdress)

if __name__=="__main__":
    # todo 需不需要增加timeout的设定呢

    # response = requests.get(rawUrl,allow_redirects=True)
    #
    #
    # print(response.text)
    # print(response.headers.get("location"))
    #这个ip地址的大概5-600个这样就会停下来，真是的出现

    # rawUrl = "https://www.baidu.com/link?url=JfdUQP5Y6tg3LYAQgNAbaqwTBqQouaOjkQcjQlj6OR_9Ld88AGHSF5tgerCGd000xxUorZV6X10EpccTIj6JCa&amp;wd=&amp;eqid=fcca4ab4000108fd000000065b9bb859"  # 百度的，<a data-click="{
    rawUrl = "https://www.sogou.com/link?url=DOb0bgH2eKjRiy6S-EyBciCDFRTZxEJg7ZfH5mjf_xlIK9ahPqNmMGJBCCZgvz6_EjM3Qz2A_5Y."  # 搜过的
    # rawUrl = "http://www.so.com/link?m=aBQ7avNa3NRS%2F1mmMMER%2FjrB0ypp9pqluBezA9Yg9BM6enLo%2BjntfllTcaS%2F%2FA1FtG8mCcivMvV%2FVRqxolp6kOVqytDG06IZB%2F5wnVo1oP04lTTB3"  # 360的
    ex = ExtractUrl()
    urllist = []
    for i in range(1000):
        print()
        print(i)
        realUrl = ex.getRealurl(rawUrl)
        if (realUrl != None):
            print(realUrl)
            urllist.append(realUrl)
    print("结束了,总数量有")
    print(len(urllist))
    print(ex.getRealurl(rawUrl))
    print(ex.proxyAdress)