#这儿是整合的开始三个爬虫进行爬取任务的  #研究反爬虫策略,这儿只当成是主函数就可以了
from dbhelper.SqlHelper import SqlHelper

dbhelper =SqlHelper()
wordlist  = dbhelper.keyWord_select()
