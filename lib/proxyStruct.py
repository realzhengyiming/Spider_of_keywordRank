#coding=utf-8
from lib.tools.ProxyHelper import ProxyHelper


class ProxyStruct(object):  #卡住的时候 才来使用代理来进行请求,那什么时候才切换回默认的进行请求呢(速度快)
    def __init__(self):
        self.proxyHelper = ProxyHelper()  # 这个类是每个对象独自可以拥有的东西，直接用就可以了
        self.proxyAdress = None  # 默认是用自己的，然后如果发现不行了后，
        self.switchToLocal = False   #如果是true那就切换回本机ip进行爬取

    def setProxy(self,proxyAdress):  # 默认有，但是再次进行修改，如果是这样的话，直接写入父类把 ，三个都可以直接使用了
        self.proxyAdress = proxyAdress  # 再赋值一个给它，然后继续爬取就可以了，会不会重复呢，有这个可能

    def setRandomProxy(self):
        return self.proxyHelper.getRandom()

    # def autoSwitchByTime(self):