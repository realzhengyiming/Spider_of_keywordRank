#coding=utf-8
#baidu crawl
import time

from dbhelper.SqlHelper import SqlHelper
from lib.FatherCrawl import FatherCrawl


class BaiduCrawl(FatherCrawl):
    def __repr__(self):
        return '这儿是百度关键词排位爬虫的类'

    def __init__(self):
        super().__init__("Baidu") #如果还有新增加的属性直接后面再添加就可以了



    def getWordRank(self,keyword) -> list: #这个的意思就是
        # time.sleep(0.5)

        urlbaidunext = "https://www.baidu.com/s?wd=" + keyword + "&rn=30"  # 直接提取出前30条，然后去掉重复的，得到前20个的排位
        soup = self.cooker.makesoup(urlbaidunext, self.fromWhere, None)  # 暂时没有设置代理
        result = soup.find_all("a", attrs={'target': "_blank", "class": "c-showurl", "href": True,
                                           "style": "text-decoration:none;"})

        if result == None:
            if self.proxyAdress == None:
                self.proxyAdress = self.setProxy(self.setRandomProxy())  # 这儿就切换一下
            else:
                self.proxyAdress = None  # 这儿这样就是代理ip和本机互相切换

        for a_tag in result:  # 每一页中的这个提取出来
            tempUrl = a_tag["href"]
            realUrl = self.extractUrl.getRealurl(tempUrl)  # 提取真实的链接
            if realUrl in self.result20:  # 这个是去重处理，让记录没有相同的，看要求加或者不加
                pass
            else:
                if realUrl != None:
                    self.result20.append(realUrl)  # 有20条那就跳出这个for,这个的意  统一这儿添加
                    if len(self.result20) == 20:
                        breakFlag = False
                        break

        # for a_tag in range(len(self.result20)):
        #     print(str(a_tag + 1) + "  " + keyword + "  " + self.result20[a_tag])
        #     number = str(a_tag + 1)

        tempList = self.result20
        self.result20=[]

        print("baidu")
        return tempList  #有个提示而已


if __name__ == '__main__':
    spiderFather = BaiduCrawl()
    tempList=spiderFather.getWordRank("python")
    print(tempList)


