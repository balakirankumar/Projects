# __AUTHOR__   :   BalaKiranKumar



#Import required modules  

import os
import smtplib
from email.message import EmailMessage
import requests
import lxml
from bs4 import BeautifulSoup
import random

# take passwords from other file or from environ variables
EMAIL_ADDRESS=os.environ.get('Email_mail')
EMAIL_PASSWORD=os.environ.get('Email_pass')

Quotes=[]
Authors=[]
Tags=[]

if not os.path.exists('./QuotesForScrapingSeperator@.txt'):
    #url to scrap
    url='http://quotes.toscrape.com/tag/'
    type_=["love","inspirational","life","humor","books","reading","friendship","friends","truth","simile",]
    url_final=url+random.choice(type_)+"/"

    #making request to url
    r=requests.get(url_final)
    # getting into lxml form
    soup=BeautifulSoup(r.text,'lxml')

    #getting required data
    quotes=soup.find_all('span',class_='text')
    author=soup.find_all('small',class_='author')
    tags=soup.find_all('div',class_='tags')


    # getting text from lxml code
    for i in range(len(quotes)):
        Quotes.append(quotes[i].text)
        Authors.append(author[i].text)
        tag=tags[i].find_all('a',class_='tag')
        t=""
        for j in tag:
            t+=", #"+j.text
        Tags.append(t.lstrip(", "))
        random_quote=random.randrange(0,len(Quotes))
    Content=f"Quote: {Quotes[random_quote]} \nAuthor: {Authors[random_quote]}. \nTags: {Tags[random_quote]}."
else:
    with open('./QuotesForScrapingSeperator@.txt','r',encoding='utf-8') as f:
        for i in f.readlines():
            Q,A,T=i.split('@')
            Quotes.append(Q)
            Authors.append(A)
            Tags.append(T)
    random_quote=random.randrange(0,len(Quotes))
    Content=f"{Quotes[random_quote]}\n{Authors[random_quote]}.{Tags[random_quote]}."

#msg composing to
contacts = ["Reciever1@gmail.com","Reciever2@gmail.com","so_on@gmail.com"]
subject= "Good Morning "


msg = EmailMessage()
msg['Subject'] = subject
msg['From'] = EMAIL_ADDRESS
msg['Bcc'] = contacts
msg.set_content(Content)


with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
	smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
	smtp.send_message(msg)