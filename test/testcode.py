#coding:utf-8
'''
f_name为所读xx.txt文件
输出为：文件最后一行
'''

fname = 'test.txt'
with open(fname, 'r') as f:  #打开文件
    first_line = f.readline()  #读第一行
    off = -50      #设置偏移量
    while True:
        f.seek(off, 2) #seek(off, 2)表示文件指针：从文件末尾(2)开始向前50个字符(-50)
        lines = f.readlines() #读取文件指针范围内所有行
        if len(lines)>=2: #判断是否最后至少有两行，这样保证了最后一行是完整的
            last_line = lines[-1] #取最后一行
            break
        #如果off为50时得到的readlines只有一行内容，那么不能保证最后一行是完整的
        #所以off翻倍重新运行，直到readlines不止一行
        off *= 2

    print ('文件' + fname + '第一行为：' + first_line)
    print ('文件' + fname + '最后一行为：'+ last_line)