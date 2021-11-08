import smtplib
from email.message import EmailMessage
from passwords import *

def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = email_user
    msg['from'] = user
    password = email_password

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()

#email_alert('test', 'test', 'piotrborsuk266@gmail.com')