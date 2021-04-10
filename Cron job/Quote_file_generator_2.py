import requests
import lxml
from bs4 import BeautifulSoup
from pprint import pprint
url='http://quotes.toscrape.com/tag/'
type_=["love","inspirational","life","humor","books","reading","friendship","friends","truth","simile",]
with open('QuotesForScrapingSeperator@.txt','w',encoding='utf-8') as f:    
    for i in range(len(type_)):
        r=requests.get(url+type_[i])
        soup=BeautifulSoup(r.text,'lxml')
        quotes=soup.find_all('span',class_='text')
        authors=soup.find_all('small',class_='author')
        tags=soup.find_all('div',class_='tags')
        for i in range(len(quotes)):
            tag=tags[i].find_all('a',class_='tag')
            t=' '
            for j in tag:
                t+=', #'+j.text
            f.write(f"Quote: {quotes[i].text}@Author: {authors[i].text}@Tags: {t[2:]}\n")