import requests
import lxml
from bs4 import BeautifulSoup

main_='https://www.brainyquote.com/topics/'
r1=requests.get(main_)
soup1=BeautifulSoup(r1.text,'lxml')
span=soup1.find_all('span',class_='topicContentName')
urls=[]
for i in span:
    urls.append((main_+i.text+'-quotes').replace('\'s','s').replace(' ','-').lower())
quotes_Dupli=[]
authors=[]
quotes=[]
tags=[]
for i in urls:
    r2=requests.get(i)
    soup2=BeautifulSoup(r2.text,'lxml')
    quotes_a=soup2.find_all('a',title="view quote")
    for i in quotes_a:
        quotes_Dupli.append(i.text.strip('\n'))
    author_a=soup2.find_all('a',title="view author")
    for i in author_a:
        authors.append(i.text)
    quotes=list(set(quotes_Dupli))
    quotes.pop(0)
    tag_a=soup2.find_all('div',class_="kw-box")
    for i in tag_a:
        t=i.find_all('a',class_="qkw-btn btn btn-xs oncl_klc")
        tag_str=''
        for i in t:
            tag_str+=', #'+i.text
        tags.append(tag_str)

with open('./BrainyQuotesSeperator@.txt','w') as f:
    for i in range(len(quotes)):
        f.write(f'Quote: {quotes[i]}@Author: {authors[i]}@Tags: {tags[i][2:]}\n')