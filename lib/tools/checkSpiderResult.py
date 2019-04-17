#coding=utf-8
#清点到底有多少个关键字了
import time

from dbhelper.SqlHelper import SqlHelper
from lib.tools.QQemailSent import EMail


class checkSpiderResult(object):
    def checkCount(self):
        sqlhelper = SqlHelper()

        return sqlhelper.checkDateKeyword()  #返回数好了的  爬取到的关键词的数量

    def sendReport(self,baidu,sougou,so):  #这个是爬虫工作完成后发的爬虫的数据
        text0 = "今日的爬虫爬取完毕，结果为 "+  time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))  # 获取当前日期,每次执行操作的时候都这样

        text = text0 + "\n baidu 提取的爬虫数量为 "+ str(baidu) + "\n sougou 提取的爬虫数量为" +str(sougou)+ "\n 360 提取的爬虫为 "+ str(so)
        email = EMail()

        email.SendEmail(1, text)

    def sendEverydayReport(self,baidu,sougou,so):  #这两个的参数是一样的，但是要分开来才可以
        text0 = "目前的常规检查4h/次 "+  time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))  # 获取当前日期,每次执行操作的时候都这样

        text = text0 + "\n baidu 提取的爬虫数量为 "+ str(baidu) + "\n sougou 提取的爬虫数量为" +str(sougou)+ "\n 360 提取的爬虫为 "+ str(so)
        email = EMail()

        email.SendEmail(1, text)



    def main(self):
        # checkResult = checkSpiderResult()
        baidu, sougou, so = self.checkCount()
        self.sendReport(baidu, sougou, so)

if __name__=="__main__":
    checkResult = checkSpiderResult()
    checkResult.main()