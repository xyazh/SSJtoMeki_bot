from email.mime.text import MIMEText
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


class MailHelper:
    ERROR = smtplib.SMTPAuthenticationError
    def _format_addr(self,s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def sendMail(self,to_addr:str,msg:str):
        msg:MIMEText = MIMEText(msg, 'plain', 'utf-8')
        msg['From'] = self._format_addr('admin <admin@1.14.66.227>')
        msg['Subject'] = Header('来自XYA-PAGE', 'utf-8').encode()
        from_addr =  "admin@1.14.66.227"
        password = 'uigig87gg'
        smtp_server = "1.14.66.227"
        server = smtplib.SMTP(smtp_server, 25) # SMTP协议默认端口是25
        server.set_debuglevel(0)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()