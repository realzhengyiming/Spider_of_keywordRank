#这个是配置文件
'''
目前有需要的设置
1.数据库的配置设置

'''

mysqlInfo = {
    "host": '127.0.0.1',
    "user": 'root',
    "passwd": 'xxxx',
    "dbhelper": 'spiderInfo',
    "port": 3306,
    "charset": 'utf8'  #这个是数据库的配置文件
}

serverName  = "测试用爬虫服务器"

#这儿目前只支持QQ邮箱，授权码这个config自己手动的设置就可以了，自动化的配置的文件都在这儿了
EmailAdress ={
        'fromAdd' : "xxxx@xxx.com",  # 你的邮箱   发件地址
        # to_ = input('Please input Recipient:')  # 收件地址
        'toAdd' : "xxxx@xxx.com",
        # subject = input('Please input title:')  # 邮件标题

        'pwd' : "xxxxxxx",  # 授权码  nkijfhnodibbiifb  smtp tmap

        #报告的主题分级
        'serverName':'测试用爬虫服务器',

        'ordernaryReport':serverName+"-"+"服务器爬虫日常数据汇报" , #这个是用来发送平时的每日数据汇报的情况的
        'ordernaryDeadlyReport': serverName+"-"+"服务器爬虫崩溃检修报告" ,#这个用于日常的服务器中爬虫死亡了提供崩溃信息还有数据汇报总结




}
