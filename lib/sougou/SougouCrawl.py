#coding=utf-8
#baidu crawl
import time

from lib.FatherCrawl import FatherCrawl


class SougouCrawl(FatherCrawl):   #整个活动都是这一个对象，所以可以维持这样一个变量
    def __repr__(self):
        return '这儿是sougou关键词排位爬虫的类'

    def __init__(self):
        super().__init__("sougou") #如果还有新增加的属性直接后面再添加就可以了,所以以后改的话，改这儿就可以了
        # print(self.result20)
        # print(self.proxyAdress)  这儿是默认是没使用代理的


    def getWordRank(self,keyword) -> str : #这个的意思就是
        # time.sleep(0.5)

        urlsogou = "https://www.sogou.com/web?query=" + keyword
        flag = True
        pageNumber = 1
        while (flag):
            soup = self.cooker.makesoup(urlsogou, "sougou", self.proxyAdress)  # 一页页面的url应该是没错的,
            result = soup.find_all("a", attrs={"target": "_blank", "href": True, "cachestrategy": True})
            # print(result)  # 这个是显示

            if result==None:  #切换代理ip，这儿
                time.sleep(1)

                print("找不到有链接是怎么回事")
                print(soup.prettify())
                if self.proxyAdress==None:
                    self.proxyAdress=self.setProxy(self.setRandomProxy())  #这儿就切换一下
                else :
                    self.proxyAdress =None #这儿这样就是代理ip和本机互相切换

            for i in result:  # 这儿是输出这一页中找到的内容的
                tempUrl = i['href']  # 这儿是输出找到的url
                # print("找到的url是：" + tempUrl)
                if tempUrl.find("/link?url=") == 0:  # 这儿是爬到的相对连接，要补回去
                    tempUrl = "https://www.sogou.com" + tempUrl  # 之后再去爬取第一个这种东西
                    # print("补回去这部分的url")
                elif tempUrl.find("/link?url=") != -1: #这个是遇到那种情况的时候
                    pass

                tempUrl = self.extractUrl.getRealurl(tempUrl)
                if tempUrl != "":
                    # print(tempUrl)
                    self.result20.append(tempUrl)
                    # print(tempUrl)
                if (len(self.result20) == 20):  # 调试中,这个应该是按顺序的，
                    flag = False  # 这个是跳出for还是跳出while
                    break
            urlsogou = "https://www.sogou.com/web?amp%3Bpage=2&query=" + keyword + "&%3Bie=utf8&ie=utf8" + "&page=" + str(
                pageNumber)
            pageNumber = pageNumber + 1  # 这样翻页就可以了
        #
        # for a_tag in range(len(self.result20)):
        #     print(str(a_tag + 1) + "  " + keyword + "  " + self.result20[a_tag])
        #     number = str(a_tag + 1)


        tempList = self.result20
        self.result20=[]
        print("sougou")
        print(len((tempList)))

        return tempList

if __name__ == '__main__':
    spiderFather = SougouCrawl()
    print(spiderFather.getWordRank("python"))


