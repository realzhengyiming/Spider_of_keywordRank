#coding = utf-8
#这个类是用来和那个开源的ip代理的东西结合使用的，还得使用请求的东西，还真是。
'''

1.发出请求，然后解析获得的json数据，然后解析数据，然后获得其中一个有用的

2.自动切换代理和还原回原来直接连接的东西，这个按时间分类来操作一下咯
'''
import json
import random

import requests



class ProxyHelper(object):
    #这个类维持三个记录时间的变量，


    def __init__(self):
        self.getProxyUrl ="http://173.255.210.215:8000/"
        self.baiduProxySwitch=None
        #todo 这儿存的是时间，自动增加的时间，然后每隔一段时间后再看这个标志符来进行
        #todo 来看是使用本地的ip地址发出请求还是使用提取到的代理ip的地址来访问这些站点
        self.sougouProxySwitch=None
        self.soProxySwitch=None
        pass

    def getGoodProxy(self):
        html = requests.get(self.getProxyUrl, allow_redirects=True)  # 不
        # content = cooker.makesoup(url,"getProxy",None)
        JsonData = html.json()
        # print(type(JsonData) )
        addressList = []
        # print(type(addressList))
        for address in JsonData:  #这个是list类型的
            if address[2]>9:
                if type(address=='list'):
                    addressList.append(address)  # 把这个添加进去这个代理地址的列表中

                    # print(addressList)

        # print(addressList)
        oneProxyAdress = random.sample(addressList, 1)[0]
        # print(oneProxyAdress)
        return oneProxyAdress

        # return addressList

    def getRandom(self):    #这个就有调用上面的那个的
        listObject= self.getGoodProxy()
        # print(listObject)
        proxyAddress = "http://"+listObject[0]+":"+str(listObject[1])
        return proxyAddress



if __name__=="__main__":
    proxyHelper = ProxyHelper()  #这个可以默认配置好的
    address = proxyHelper.getRandom()  #其实这儿是打错了名字 ，减少了调用的参数
    print(address)