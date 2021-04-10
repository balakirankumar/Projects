import smtplib
import os
import sys
from email.message import EmailMessage


def job():
    EMAIL_ADDRESS=os.environ.get('Email_mail')
    EMAIL_PASSWORD=os.environ.get('Email_pass')
    contacts = sys.argv[1]
    print(contacts)
    subject_in= "Subscribe Notification"
    content_in= "Thanks For Subscribing to ngit.in"
    msg = EmailMessage()
    msg['Subject'] = subject_in
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = contacts
    msg.set_content(content_in)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
job()