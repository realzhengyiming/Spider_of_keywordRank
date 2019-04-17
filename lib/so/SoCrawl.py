#coding=utf-8
#baidu crawl
import time

from lib.FatherCrawl import FatherCrawl


#todo 所以之前看到的，比如百度的爬到某个地方后什么都提取不出来这个应该也是因为爬虫的ip给封了把，所以提取不出来原来要提取的页面，这种时候需要想办法使用代理的ip
'''

虽然这儿没有写入数据库的东西
'''
class SoCrawl(FatherCrawl):  #这儿有一个多重继承的关系啊，看来还是有事才切换成代理的好，默认就用自己的才可以
    def __repr__(self):
        return '这儿是360关键词排位爬虫的类'

    def __init__(self):  #原来是这儿写错了
        super().__init__("360") #如果还有新增加的属性直接后面再添加就可以了,所以以后改的话，改这儿就可以了



    def getWordRank(self,keyword) -> str : #这个的意思就是
        print("360 start")
        # time.sleep(0.5)

        urlso = "https://www.so.com/s?ie=utf-8&fr=none&src=home_www&q=" + keyword
        breakFlag  = 1
        while (breakFlag):  # 这儿这个next只是用来跳出while的标志
            # time.sleep(6)
            # print(urlso)
            soup = self.cooker.makesoup(urlso, "360", self.proxyAdress)
            # print(soup.prettify())
            if soup==None:
                return None  #这种情况说明 ，网页打不开了啊

            result = soup.find_all("a", attrs={"rel": True, "target": "_blank", "data-res": True})
            # print(result)  # 这个是显示
            if result==None:
                if self.proxyAdress==None:
                    print("现在开始使用代理打开搜索结果")
                    self.proxyAdress=self.setProxy(self.setRandomProxy())  #这儿就切换一下
                else :
                    print("现在切换回用本机打开搜索结果")
                    self.proxyAdress =None #这儿这样就是代理ip和本机互相切换
                    continue  #继续进行爬取
            else: #不为空才进行这些东西
                for a_tag in result:  #这儿除了提取url还有就是把下一页的链接找出来
                    tempUrl = a_tag['href']  #直接都把这几个传进去了
                    tempUrl = self.extractUrl.getRealurl(tempUrl)  # 使用这个提取出真的url
                    # print(tempUrl)
                    if tempUrl in self.result20:  # 这个是去重处理，让记录没有相同的，看要求加或者不加
                        pass
                    else:
                        if tempUrl ==None or len(tempUrl) != 0:
                            if tempUrl==None:
                                break
                            if tempUrl.find("http://www.so.com/link?") != -1:  # 那就再来一遍
                                tempUrl = self.extractUrl.getRealurl(tempUrl)
                            self.result20.append(tempUrl)  # 有20条那就跳出这个for
                            # print(tempUrl)
                            if (len(self.result20) == 20):
                                breakFlag = False
                                break
                    #这儿是查找下一页的东西
                nextPage = soup.find_all("a", attrs={"id": "snext", "href": True})  # 这儿是找出下一页然后继续遍历的
                    # print("我在这儿360")
                for a_tag in nextPage:
                    if (a_tag.text == u"下一页"):
                        # print(a_tag.text)
                        urlso = "https://www.so.com" + a_tag["href"]
                        # print (urlso)


        tempList = self.result20
        self.result20=[]
        # print(360)
        print("找到了那么多条")
        print(tempList)

        return tempList


if __name__ == '__main__':   #这儿的测试是没写入数据库的
    spiderFather = SoCrawl()
    print(spiderFather.proxyAdress)
    spiderFather.getWordRank("python")



