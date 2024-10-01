import bs4 as bs
import urllib.request
import re




scraped_data = urllib.request.urlopen('https://www.sparknotes.com/lit/jekyll/facts/')
article = scraped_data.read()

parsed_article = bs.BeautifulSoup(article,'lxml')

paragraphs = parsed_article.find_all('p')

doc = ""

for p in paragraphs:
    doc += p.text


from summarizer import summarize

print(summarize('test', doc, 10))