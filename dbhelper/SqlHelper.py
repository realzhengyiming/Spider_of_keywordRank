#coding=utf-8
import time
import pymysql
from DBUtils.PooledDB import PooledDB
from config import mysqlInfo


class SqlHelper:
    __pool = None   #这个也是静态的属性

    # def __init__(self):
    #     pass
        # 构造函数，创建数据库连接、游标
        # self.coon = SqlHelper.getmysqlconn()  #这个是默认创建出来的东西
        # self.cur = self.coon.cursor(cursor=pymysql.cursors.DictCursor)

    # 数据库连接池连接
    @staticmethod   #这个是静态的方法可以直接调用的
    def getmysqlconn():  #从连接池里面获得一个连接
        if SqlHelper.__pool is None:
            __pool = PooledDB(creator=pymysql, mincached=1, maxcached=20, host=mysqlInfo['host'],
                                  user=mysqlInfo['user'], passwd=mysqlInfo['passwd'], db=mysqlInfo['dbhelper'],
                                  port=mysqlInfo['port'], charset=mysqlInfo['charset'])
            # print(__pool)
        return __pool.connection()

        # 释放资源
    # def dispose(self): #这儿只能断默认初始化的那个连接
    #     self.coon.close()
    #     self.cur.close()

    def integrate_result_insert(self,keword,urlList,date,fromWhere) :
        '''
        :param rankResultList:  传入keyword的按排位顺序的url 链接列表
        :return:  insert into dbhelper  整合插入排位进数据库
        '''
        rankNumber = 1
        # print(fromWhere)
        # print(urlList)
        for url in urlList: # 传入一个列表，遍历后插入进去
            self.result_insert(rankNumber,keword,url,date,fromWhere)
            rankNumber+=1 #往后的累加，因为urllist每个都是20个，所以只到20
            if (rankNumber>20):
                break
        print("20记录插入成功来自于"+fromWhere)


    def result_insert(self,rank,keyword ,url,date,fromWhere): #排位记录插入表中，逢20个结果1~20 插入一次
        '''
        :param keyword:
        :param rank:
        :param url:
        :param date:
        :param fromWhere:
        :return:  insert_State
        '''
        # print(rank)
        # print(keyword)
        # print(url)
        # print(date)
        # print(fromWhere)
        sql_insert = "insert into spiderResult(ranking,keyword,url,spiderDate,spiderEngine) values('" + str(rank) + "','" + keyword +  "','"  + url + "','" + date + "','"+fromWhere+"')"  # 分别是数字，字符串，字符串
        # sql_insert = "insert into spiderResult(ranking,keyword,url,spiderDate,spiderEngine) values('%s,','%s'"  + url + "','" + date + "','"+fromWhere+"')"
        # print(sql_insert)
        coon =SqlHelper.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            cur.execute(sql_insert)
            # 提交
            coon.commit()
            # print("插入" + fromWhere + "完毕")
        except Exception as e:
            # 错误回滚
            print(e)
            coon.rollback()
        finally:

            coon.close()
            cur.close()  #把连接断开


    def keyWord_select(self,number): #返回关键词的列表,可选择输出的关键词的数量
        coon = SqlHelper.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "SELECT word FROM Keyword limit 0,%d;"%number
        wordlist = []
        print("关键词连接成功")
        try:
            # 执行SQL语句
            cur.execute(sql)
            # 获取所有记录列表
            wordlist = cur.fetchall()
        except Exception as e:
            raise e
            print("Error: unable to fetch data")
        finally:
            # 关闭数据库连接
            cur.close()
            coon.close()
        print(type(wordlist))
        return wordlist



        # 插入\更新\删除sql
    def op_insert(self, sql):  #插入一条数据到数据库（三个都是插入同一个表，所以公用同一个）
        print('op_insert', sql)
        coon = SqlHelper.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

        insert_num = cur.execute(sql)
        # print('mysql sucess ', insert_num)  #把内容打印出来了，这儿
        coon.commit() #提交事务
        return insert_num

        # 查询
    def op_select(self, sql):
        coon = SqlHelper.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)
        # print('op_select', sql)
        cur.execute(sql)  # 执行sql
        select_res = cur.fetchall()  # 返回结果为字典
        # print('op_select', select_res)
        print(select_res)
        return select_res



    #这下面的是用来辅助运维的数据库操作
    def countKeyword(self,list):
        return len(list) #返回记录的条数


    def checkDateKeyword(self): #用来返回当天爬取到了多少个关键字的，3个搜索引擎属于不同的诶，速度也不同，那就分开来计数
        # coon = SqlHelper.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        # cur = coon.cursor(cursor=pymysql.cursors.DictCursor) #这个是查询的date时间，是不可以这样的
        nowDate = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 获取当前日期,每次执行操作的时候都这样

        sqlbaidu="select * from spiderResult where spiderEngine='baidu' and  spiderDate='%s' ;"%nowDate
        sqlSougou = "select * from spiderResult where spiderEngine='Sougou' and  spiderDate='%s' ;"%nowDate
        sql360 = "select * from spiderResult where spiderEngine='360'and spiderDate='%s' ;"%nowDate

        # print(sqlbaidu)
        # print(sqlSougou)
        # print(sql360)

        numberBaidu = self.countKeyword(self.op_select(sqlbaidu))
        numberSogou = self.countKeyword(self.op_select(sqlSougou))
        number360 =self.countKeyword(self.op_select(sql360))

        print("各记录的数量")

        # print(numberBaidu)
        # print(numberSogou)
        # print(number360)
        print("各执行关键词的数量")
        baiduKeyword = numberBaidu/20
        sougouKeyword =numberSogou/20
        soKeyword = number360/20
        # print(numberBaidu/20)
        # print(numberSogou/20)
        # print(number360/20)
        return baiduKeyword,sougouKeyword,soKeyword  #把统计的这个数字的结果汇总起来







if __name__ == '__main__':
    #申请资源


    # sql = "select * from Keyword  "
    # res = opm.op_select(sql)
    # print(res)
    # print(len(opm.keyWord_select(1)))

    #释放资源




    # ccc = SqlHelper()  #直接创建对象，连接，然后释放就可以了1，2.两个流程连接池可以操作
    # res = ccc.op_select("select * from testdb where name = 'b'")
    # print(res)
    opm = SqlHelper()
    # opm.checkDateKeyword()

    baidu,Sogou,So = opm.checkDateKeyword()
    print(baidu)
    print(Sogou)
    print(So)