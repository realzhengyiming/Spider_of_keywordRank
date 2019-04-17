import random
import lxml
import requests
from bs4 import BeautifulSoup
from lib.proxyStruct import ProxyStruct


class CookSoup(ProxyStruct):  #继承这个的属性，那么代理这个东西就它自己管了，减少耦合性
    def makesoup(self,url, fromWhere, proxyAdress):  # 这个代理的留着备用，不用的使用装入 None  就可以了
        """
        获取网站的soup对象，#看看还能不能增加代理的东西，进来
        有两个请求头的自定义，但是，为什么要分开来呢

        """
        my_headers = [
            'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30',
            'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)',
            'Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)']

        diyHeader = {}

        if (fromWhere == "baidu"):  #模拟的浏览器的
            # 多个字典，然后合并就可以了。
            diyHeader = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding": 'gbk, utf-8',
                "Accept-Language": "zh-CN,zh;q=0.9",

            }

        if (fromWhere == "360"):  # 360
            diyHeader = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding": "gbk, utf-8",
                "Accept-Language": "zh-CN,zh;q=0.9",
            }

        # if (fromWhere == ""):  # 360
        #     diyHeader = {
        #         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        #         "Accept-Encoding": "gbk, utf-8",
        #         "Accept-Language": "zh-CN,zh;q=0.9",
        #     }

        address = proxyAdress  # 传进来有一个代理的地址
        if (address!=None):
            proxies = {'http': address, "https": address}  # , 'https': 'http://localhost:8888'
            headers = {"User-Agent": random.choice(my_headers)}
            headers.update(diyHeader)  # 这儿是合并两个字典diyheader,这儿可能会出现问题的需要使用try
            html=None
            while(html):
                try:  #并且输出为200才可以
                    html = requests.get(url, headers=headers, allow_redirects=True,proxies=proxies,timeout=30).text  # 不允许你跳转，就访问这个就是了，改成request后就是这个样子
                except Exception as e:
                    print(e)
                    address = self.setRandomProxy()    #修改一下的代理
                    proxies = {'http': address, "https": address}  # , 'https': 'http://localhost:8888'
                    headers = {"User-Agent": random.choice(my_headers)}
                    headers.update(diyHeader)  # 这儿是合并两个字典diyheader,这儿可能会出现问题的需要使用try

            soup = BeautifulSoup(html, 'lxml')
            return soup
        else: #没有就不用代理咯
            headers = {"User-Agent": random.choice(my_headers)}
            headers.update(diyHeader)  # 这儿是合并两个字典diyheader
            try:
                html = requests.get(url, headers=headers, allow_redirects=True,timeout=30).text  # 不允许你跳转，就访问这个就是了，改成request后就是这个样子
                soup = BeautifulSoup(html, 'lxml')
            except Exception as e:
                print(e)
                # soup = None #打不开就跳过这个链接啦
            return soup


#抱歉哦
if __name__=="__main__":
    url = "https://ip.cn/"
    # BS = CookSoup().makesoup(url, "sougou", None)
    # print(BS)
    cook = CookSoup()



    soup = cook.makesoup(url,"sdsf","http://217.182.119.131:3128")  #这个是查看访问的ip的，看样子还是可以用的，这个ip地址
    print(soup)

