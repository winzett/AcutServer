from django.core.mail import send_mail
import sendgrid
import os
from sendgrid.helpers.mail import *
from django.http import HttpResponse


#import smtplib
#from email.mime.text import MIMEText

#def test_mail():
#    smtp = smtplib.SMTP('smtp.gmail.com', 587)
#    smtp.ehlo()      # say Hello
#    smtp.starttls()  
#    smtp.login('winzett0@gmail.com', '')
#
#    msg = MIMEText('test')
#    msg['Subject'] = 'test'
#    msg['To'] = 'winzett0@gma'l.com'
#    smtp.sendmail('winzett0@gmail.com', 'winzett0@gmail.com', msg.as_string())
#
#    smtp.quit()



def test_mail(request):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("customer_service@acut.com")
    to_email = Email("winzett0@gmail.com")
    subject = "Sending with SendGrid is Fun"
    content = Content("text/plain", "and easy to do anywhere, even with Python")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

    return HttpResponse("success") 

def test_test_mail():


   sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
   from_email = Email("test@example.com")
   to_email = Email("test@example.com")
   subject = "Sending with SendGrid is Fun"
   content = Content("text/plain", "and easy to do anywhere, even with Python")
   mail = Mail(from_email, subject, to_email, content)
   response = sg.client.mail.send.post(request_body=mail.get())
   print(response.status_code)
   print(response.body)
   print(response.headers)


def mailing():
    from django.core.mail import send_mail
    from django.core.mail import EmailMultiAlternatives

    mail = EmailMultiAlternatives(
          subject="test",
          body="This is a simple text email body.",
          from_email="woongjae lee <winzett0@gmail.com>",
          to=["winzett0@gmail.com"],
          reply_to=["support@sendgrid.com"]
      )

    mail.send()
