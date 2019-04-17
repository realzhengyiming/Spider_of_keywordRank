#coding=utf-8
#三个针对性爬虫的父类，用来减少代码重复,继承和多态，子类覆写
from lib.proxyStruct import ProxyStruct
from lib.tools.CookSoup import CookSoup
from lib.tools.ExtractUrl import ExtractUrl
# from lib.tools.ProxyHelper import ProxyHelper


class FatherCrawl(ProxyStruct):
    def __repr__(self):

        return '这儿是单个爬虫的父类'

    def __init__(self,fromWhere): #这个是配置是属于哪个的爬虫
        super().__init__()

        self.fromWhere = fromWhere
        # self.proxyHelper = ProxyHelper()  #这个类是每个对象独自可以拥有的东西，直接用就可以了
        # self.proxyAdress = self.proxyHelper.getRandom()   #默认给他们一个
        self.extractUrl = ExtractUrl()
        self.cooker = CookSoup()  # 统一直接使用这几个对象来操作就可以了
        self.result20 = []  #这儿是装那前20 个排位的


    def getWordRank(self,keyword): #这儿的话每个爬虫
        print("you should write your unique crawl method here")
        pass


if __name__ == '__main__':
    spiderFather = FatherCrawl("baidu")
    spiderFather.getWordRank("python")