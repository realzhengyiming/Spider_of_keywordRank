# coding:utf8
import datetime
import time, timeit


def doSth():
    # 把爬虫程序放在这个类里
    print(u'这个程序要开始疯狂的运转啦')


# 一般网站都是1:00点更新数据，所以每天凌晨一点启动
def main(h=1, m=0):
    while True:
        now = datetime.datetime.now()
        # print(now.hour, now.minute)
        if now.hour == h and now.minute == m:
            break
        # 每隔60秒检测一次
        time.sleep(60)
    doSth()





def clock(func):
    def clocked(*args):
        t0 = timeit.default_timer()
        result = func(*args)
        elapsed = timeit.default_timer() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result

    return clocked


@clock
def run(seconds):
    time.sleep(seconds)
    return time




# if __name__=="__main__":
#     main(10,50)
if __name__ == '__main__':
    run(4)