#encoding:utf-8
__author__ = 'binpo'


import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email():
    try:
        # me == my email address
        # you == recipient's email address
        me = "admin@zenmez.com"
        you = "binpocn@163.com"

        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Link"
        msg['From'] = me
        msg['To'] = you

        # Create the body of the message (a plain-text and an HTML version).
        text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
        html = """\
        <html>
          <head></head>
          <body>
            <p>Hi!<br>
               How are you?<br>
               Here is the <a href="http://www.python.org">link</a> you wanted.
            </p>
          </body>
        </html>
        """

        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        msg.attach(part1)
        msg.attach(part2)

        s = smtplib.SMTP('localhost')
        print s
        print type(s)
        print dir(s)
        s.sendmail(me, you, msg.as_string())
        s.quit()

        return True
    except:

        return False

if __name__ == '__main__':
    if send_email():
        #['binpocn@163.com'],"hello","<a href='http://www.cnblogs.com/xiaowuyi'>小五义</a>"):
        print "发送成功"
    else:
        print "发送失败"