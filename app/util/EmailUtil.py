import smtplib
from email.mime.text import MIMEText

# Here I am using yahoo mail server

YAHOO_ACCOUNT= '#USERNAME' # Sender Username
YAHOO_PASS='#PASSWORD'    # App password generated for mail server

def send_mail(fromAddr, toAddrs, subject, body):
    msg = MIMEText(body)
    msg['From'] = fromAddr
    msg['To'] = ', '.join(toAddrs)
    msg['Subject'] = subject
    s = smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465)
    s.ehlo()
    s.login(YAHOO_ACCOUNT, YAHOO_PASS)
    s.sendmail(fromAddr, toAddrs, msg.as_string())
    s.quit()