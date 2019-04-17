#coding=utf-8
#清点到底有多少个关键字了
import time

from dbhelper.SqlHelper import SqlHelper

sqlhelper = SqlHelper()
sqlhelper.checkDateKeyword()
nowDate = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))  # 获取当前日期,每次执行操作的时候都这样
print(nowDate)

#todo 还是没研究透，其实是因为什么，而让他们不提示错误，然后却又没有爬取到1000个关键词这样的情况的东西，
# 怎么个回事呢