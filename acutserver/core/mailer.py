# -*- coding:utf-8 -*-

import smtplib
from email.mime.text import MIMEText

smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.ehlo()      # say Hello
smtp.starttls()  # TLS 사용시 필요
smtp.login('lee@live.com', 'password')

msg = MIMEText('본문 테스트 메시지')
msg['Subject'] = '테스트'
msg['To'] = 'winzett0@gmail.com'
smtp.sendmail('winzett0@gmail.com', 'winzett0@gmail.com', msg.as_string())

smtp.quit()
