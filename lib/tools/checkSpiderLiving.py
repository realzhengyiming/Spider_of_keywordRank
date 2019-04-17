#coding=utf-8
import os
import time
from multiprocessing import Process #这种方式是都可以使用的

from lib.tools.QQemailSent import EMail
from lib.tools.checkSpiderResult import checkSpiderResult

'''
@author: Jacobpc
#这个是 检查进程是否还在运行的检查程序，如果爬虫掉线了，爬虫就应该发邮件告诉我它掉了，
并且把一些信息数据发送给我，我可以提前分析起来，这样就不错诶，要把那些错误都抛出来才可以统一处理的对吧
'''
import os
import sys
import subprocess

class CheckSpiderLiving(object): #顾名思义，检查程序是否活着
    def get_process_id(name):
        child = subprocess.Popen(["ps aux | grep" +name+'| grep -v grep'], stdout=subprocess.PIPE, shell=False)
        print(child)
        print(type(child))
        response = child.communicate()[0]
        return response


    def isRunning(self,process_name):
        try:
            process = len(os.popen('ps aux | grep "' + process_name + '" | grep -v grep').readlines())
            if process >= 1:
                return True
            else:
                return False
        except:
            print("Check process ERROR!!!")

            return False





if __name__=="__main__":
    checkResult = checkSpiderResult()
    checkWorker = CheckSpiderLiving()

    countNumber = 1
    while(1):
        if checkWorker.isRunning("python3 everyCrawl.py"):
            # print("现在正常工作一天啦"+str(countNumber))
            # time.sleep(60*60*12)  #每半天检查一下是否还在运行，如果没在运行的话就发邮箱,
            # todo 先把这儿检查程序是否运行的这个调试好来，这个可以有的，运行情况和结果都会给自己汇报起来的
            baidu,sougou,so = checkResult.checkCount() # 统计一下基本的数据
            checkResult.sendEverydayReport(baidu,sougou,so) #把日常的这个日志发送到邮件中
            print("运行正常")
            time.sleep(60*60*4) #每四个小时就休眠一次

        else:

            baidu, sougou, so = checkResult.checkCount()  # 统计一下基本的数据
            text0 = "今天 " + time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 获取当前日期,每次执行操作的时候都这样

            text1 = text0 + "\n baidu 提取的爬虫数量为 " + str(baidu) + "\n sougou 提取的爬虫数量为" + str(
                sougou) + "\n 360 提取的爬虫为 " + str(so)

            text = "😱你的服务器爬虫dead了，请检查一下你的内容哪儿出问题了，目前为止的\n"+text1
            email = EMail()

            email.SendEmail(1, text)
            print("已发送")
            time.sleep(60 * 60 * 4)  # 每四个小时就休眠一次
