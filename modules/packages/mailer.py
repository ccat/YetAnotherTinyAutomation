# coding:utf-8

from .. import interfaces

import smtplib

from email import Encoders
from email.Utils import formatdate
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.mime.application import MIMEApplication


class Mailer(interfaces.Package):
    def __init__(self,packageName,server,fromAddr):
        interfaces.Package.__init__(self,packageName, server)
        #self.mailerType="smtp"
        self.fromAddr=fromAddr

    def createMessage(self,toAddr,subject,body,attachFilenames=[]):#,encoding="ISO-2022-JP"
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = self.fromAddr
        msg["To"] = toAddr
        msg["Date"] = formatdate()
        msg.attach(MIMEText(body))
        
        for item in attachFilenames:
            f=open(item)
            attachment = MIMEBase("application","octet-stream") 
            attachment.set_payload(f.read()) 
            f.close()
            Encoders.encode_base64(attachment)
            msg.attach(attachment)
            fname=item.split("/")[-1]
            attachment.add_header("Content-Disposition","attachment", filename=fname) 

        return msg
    

    def sendBySMTP(self,toAddr,smtp_server,subject,body,attachFilenames=[]):#,encoding="ISO-2022-JP"
        msg=self.createMessage(toAddr,subject,body,attachFilenames)
        
        smtp = smtplib.SMTP(smtp_server)
        smtp.sendmail(self.fromAddr, toAddr, msg.as_string())
        smtp.close()

    def sendByGmail(self,toAddr,username,password,subject,body,attachFilenames=[]):
        msg=self.createMessage(toAddr,subject,body,attachFilenames)
        
        smtp = smtplib.SMTP('smtp.gmail.com:587')
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(username,password)
        smtp.sendmail(self.fromAddr, toAddr, msg.as_string())
        smtp.quit()
