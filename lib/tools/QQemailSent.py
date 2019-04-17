#!/user/bin/env python3

import smtplib
from email.mime.text import MIMEText

from config import EmailAdress



class EMail(object):
    def __init__(self):
        self.fromAdd = EmailAdress['fromAdd']  # 你的邮箱   发件地址
        # to_ = input('Please input Recipient:')  # 收件地址
        self.toAdd = EmailAdress['toAdd']
        # subject = input('Please input title:')  # 邮件标题
        # self.subject = "服务器 新闻爬虫运行终端报告"

        self.pwd = EmailAdress['pwd']  # 授权码  nkijfhnodibbiifb  smtp tmap
        self.ordernaryReport = EmailAdress['ordernaryReport']  #日常报告的主题常量
        self.ordernaryDeadlyReport = EmailAdress['ordernaryDeadlyReport']   #死亡的时候就要这个主题了


    def SendEmail(self,subjectLevel,text):  #发送的主题还有发送的内容，就可以啦
        if subjectLevel==1:
            subject = self.ordernaryReport
        elif subjectLevel==2:
            subject = self.ordernaryDeadlyReport

        # print(text)
        msg = MIMEText(text)
        msg["Subject"] = subject
        msg["From"] = self.fromAdd
        msg["To"] = self.toAdd
        try:
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
            s.login(self.fromAdd, self.pwd)
            s.sendmail(self.fromAdd, self.toAdd, msg.as_string())
            s.quit()
            print("Success!")
        except smtplib.SMTPException:
            print('Falied!')


if __name__ == '__main__':

    # text = input('Please input Content:')  # 邮件内容

    text = "😍成功了拉，以后自动检测后就可以定时的向手机汇报程序中断了的消息拉"
    subject="服务器 爬虫阵亡状态报告...😥"
    email = EMail()

    email.SendEmail(1, text)
