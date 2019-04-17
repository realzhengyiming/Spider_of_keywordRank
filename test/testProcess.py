#coding=utf-8
import os
import time
from multiprocessing import Process #这种方式是都可以使用的

'''
@author: Jacobpc
'''
import os
import sys
import subprocess


def get_process_id(name):
    child = subprocess.Popen(["ps aux | grep" +name+'| grep -v grep'], stdout=subprocess.PIPE, shell=False)
    print(child)
    print(type(child))
    response = child.communicate()[0]
    return response


def isRunning(process_name):
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
    while(1):
        print(isRunning("python3 everyCrawl.py"))
        # time.sleep(60*60*12)  #每半天检查一下是否还在运行，如果没在运行的话就发邮箱,
        # todo 先把这儿检查程序是否运行的这个调试好来，这个可以有的，运行情况和结果都会给自己汇报起来的
        time.sleep(60*60*4) #每四个小时就休眠一次
