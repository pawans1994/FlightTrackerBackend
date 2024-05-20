import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Here I am using yahoo mail server

def send_mail(fromAddr, toAddrs, subject, body):
    load_dotenv()
    msg = MIMEText(body)
    msg['From'] = fromAddr
    msg['To'] = ', '.join(toAddrs)
    msg['Subject'] = subject
    s = smtplib.SMTP_SSL(os.getenv('MAIL_SERVER'), os.getenv('MAIL_PORT'))
    s.ehlo()
    s.login(os.getenv('MAIL_USERNAME'), os.getenv('MAIL_PASSWORD'))
    s.sendmail(fromAddr, toAddrs, msg.as_string())
    s.quit()