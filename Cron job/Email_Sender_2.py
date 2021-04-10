import requests
import lxml
from bs4 import BeautifulSoup
import random
from email.message import EmailMessage
import smtplib
import os

quotesdupli=[]
Quotes=[]
Author=[]
Tags=[]

if not os.path.exists('./BrainyQuotesSeperator@.txt'):

    main_url='https://www.brainyquote.com/topics/'
    r=requests.get(main_url)
    soup=BeautifulSoup(r.text,'lxml')
    span=soup.find_all('span',class_='topicContentName')
    topics=[]
    for i in span:
        topics.append(i.text+'-quotes')
    random_topic=random.choice(topics).replace('\'s','s').lower()
    main=main_url+random_topic.replace(' ','-')

    r=requests.get(main)
    soup=BeautifulSoup(r.text,'lxml')

    quotes_a=soup.find_all('a',title="view quote")
    for i in quotes_a:
        quotesdupli.append(i.text.strip('\n'))

    author_a=soup.find_all('a',title="view author")
    for i in author_a:
        Author.append(i.text)

    tag_a=soup.find_all('div',class_="kw-box")
    for i in tag_a:
        t=i.find_all('a',class_="qkw-btn btn btn-xs oncl_klc")
        tag_str=''
        for i in t:
            tag_str+=', #'+i.text
        Tags.append(tag_str)
    Quotes=list(set(quotesdupli))
    Quotes.pop(0)
    random_quote=random.randrange(0,len(Quotes))
    Content=f"Quote: {Quotes[random_quote]}\nAuthor: {Author[random_quote]}\nTags: {Tags[random_quote][2:]}"
    #time taken by requests is 1.9567549228668213 
    #time taken by file reading is 0.10269331932067871

else:
    with open('./BrainyQuotesSeperator@.txt','r') as f:
        for i in f.readlines():
            Q,A,T=i.split('@')
            Quotes.append(Q)
            Author.append(A)
            Tags.append(T)
    random_quote=random.randrange(0,len(Quotes))
    Content=f"{Quotes[random_quote]}\n{Author[random_quote]}\n{Tags[random_quote][2:]}"

reciepents=["Reciever1@gmail.com","Reciever2@gmail.com","so_on@gmail.com"]
EMAIL_ADDRESS=os.environ.get('Email_mail')
EMAIL_PASSWORD=os.environ.get('Email_pass')
subject='Good Morning'
msg=EmailMessage()
msg['Subject']=subject
msg['From']=EMAIL_ADDRESS
msg.set_content(Content)
msg['Bcc']=reciepents

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
	smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
	smtp.send_message(msg)
