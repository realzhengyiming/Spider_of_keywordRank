#coding=utf-8
#这个是每日的关键字爬取的东西，写好后用来测试每天的爬取的数量的100 ，1000 ，10000个关键字，这个怎么去突破，这个要思考。
'''
先实现，实现了后再去思考如何加速和更加高效
1.这儿要做的是把关键词找出来，然后开始循环遍历一个一个的进行爬取，可以写三个线程来同时进行爬取，io密集型的爬虫
2.可以改成3个不同的进程，因为是不同的搜索引擎，所以问题不大，
3.然后还要加延迟，或者是代理之类的，来提防一下反爬的机制
4。把三个  搜索引擎的东西改成协程的方式来组织到一起，每当有io阻塞就跳另外一个继续请求，协程应该比现在的单线程快一点
'''
# import Queue  #j
import sys
import threading #多线程版本
from typing import Optional, Callable, Any, Iterable, Mapping

from lib.tools.checkSpiderResult import checkSpiderResult

sys.path.append('/root/BigData')



import time

from dbhelper.SqlHelper import SqlHelper
from lib.baidu.BaiduCrawl import BaiduCrawl
from lib.so.SoCrawl import SoCrawl
from lib.sougou.SougouCrawl import SougouCrawl




# number1 = 0
# number2 = 0
# number3 = 0

# todo 今天晚上先暂时不使用 三个线程，明天再来测试3个线程的
def threadBaidu(wordlist):  #这个是百度的run  线程执行的东西
    # print(wordlist)
    count=1
    baiduCrawl = BaiduCrawl()
    print("百度线程开启")
    for keywordDic in wordlist:

        # number1+=1
        # print(keywordDic)  这儿配置代理吗
        if (count%50 and baiduCrawl.proxyAdress==None) : #每50个关键词换一个ip地址
            baiduCrawl.setProxy(baiduCrawl.setRandomProxy())  #给它设置一个默认的代理放进去使用
        if (count%100 and baiduCrawl.proxyAdress!=None) : #每50个关键词换一个ip地址
            baiduCrawl.proxyAdress=None  #给它设置一个默认的代理放进去使用
        count+=1
        keyword = keywordDic['word']

        # print(keyword)

        date = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 获取当前日期,每次执行操作的时候都这样
        urlList = baiduCrawl.getWordRank(keyword)
        dbhelper.integrate_result_insert(keyword, urlList, date, baiduCrawl.fromWhere)
        print("")
        pass


def threadSougou(wordlist):  # 这个是百度的run  线程执行的东西
    print("sougou线程开启")
    sogouCrawl = SougouCrawl()
    count = 1
    for keywordDic in wordlist:
        keyword = keywordDic['word']
        if (count%50 and sogouCrawl.proxyAdress==None) : #每50个关键词换一个ip地址
            sogouCrawl.setProxy(sogouCrawl.setRandomProxy())  #给它设置一个默认的代理放进去使用
        if (count%100 and sogouCrawl.proxyAdress!=None) : #每50个关键词换一个ip地址
            sogouCrawl.proxyAdress=None  #给它设置一个默认的代理放进去使用
        count+=1
        date = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 获取当前日期,每次执行操作的时候都这样
        urlList = sogouCrawl.getWordRank(keyword)  #
        dbhelper.integrate_result_insert(keyword, urlList, date, sogouCrawl.fromWhere) #每次插入查到的一个关键词的 列表返回去
        pass


def threadSo(wordlist):  # 这个是百度的run  线程执行的东西
    soCrawl = SoCrawl()  # 可以同时使用一个对象，然后爬过一定的关键词后就切换ip大概100个关键词就切换一个ip地址把
    print("So线程开启")
    count = 1
    for keywordDic in wordlist:

        keyword = keywordDic['word']
        if (count%40 and soCrawl.proxyAdress==None) : #每50个关键词换一个ip地址
            soCrawl.setProxy(soCrawl.setRandomProxy())  #给它设置一个默认的代理放进去使用
        if (count%100 and soCrawl.proxyAdress!=None) : #每50个关键词换一个ip地址
            soCrawl.proxyAdress=None  #给它设置一个默认的代理放进去使用
        count+=1

        date = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 获取当前日期,每次执行操作的时候都这样
        urlList = soCrawl.getWordRank(keyword)
        if urlList!=None:  #如果为空那就不要这个关键词了
            dbhelper.integrate_result_insert(keyword, urlList, date, soCrawl.fromWhere)
        pass





if __name__=="__main__":
    dbhelper = SqlHelper()
    wordlist = dbhelper.keyWord_select(1000)  #设置爬取的关键词的数量在这儿。
    print(len(wordlist))
# todo 写一个多线程把，这儿写上三个线程就可以了 ,这儿直接启动三个线程来进行爬取
#     qBaidu = Queue()
#     qSougou = Queue()
#     qSo = Queue()
    # todo 内部出现了异常的话，统一网上抛出raise ，然后统一提取出来吗
    while(1):
        # baidu = threading.Thread(target=threadBaidu,args=(wordlist,))   #比如这样的列表的参数需要用括号括起来才可以的
        # sougou = threading.Thread(target=threadSougou,args=(wordlist,))
        so= threading.Thread(target=threadSo,args=(wordlist,))  #360的怎么回事，卡住了

        # baidu.start()
        # sougou.start()
        so.start()
        # baidu.join()
        # sougou.joi n()
        so.join()   

        print("三个插入完毕")
# todo 自从改了那个代理的，全部都开始变得不行了，代理那个也是很慢，还可能不能用，真是辣鸡啊
        #todo 先逐个进行检查吧，没办法哦
        #todo 前三个不开代理，都能够完成关键词的爬取。  所以要配置检查好代理的东西是怎么回事才可以
        checkResult = checkSpiderResult()
        checkResult.main()
        print("今天的"+str(len(wordlist))+"个关键词写完了")
        time.sleep(60*60*24)   #先是一天爬一次，这样先





    # opm = SqlHelper()
    # opm.checkDateKeyword()




