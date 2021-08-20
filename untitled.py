import json
import lxml,re
from lxml.html.clean import Cleaner
from bs4 import BeautifulSoup
from urllib.parse import *
import os

# from base64 import b64decode
# from flask import request,Flask
# app = Flask(__name__)

cleaner = Cleaner()
cleaner.style = True
cleaner.javascript = True
cleaner.links = False
cleaner.remove_tags = ['li', 'div']


ignore_tags = ['a','h1', 'img', 'strong', 'table', 'h2', 'h3', 'small', 'ul', 'span', 'h4', 'h5', 'h6', 'table', 'p', 'tr', 'td', 'th','ol']

def clean(soup):
	tags = [tag.name for tag in soup.find_all()]
	tags = list(dict.fromkeys(tags))
	print(tags)
	for i in tags:
		v = soup.findAll(i)
		for j in v:
			if "img " in str(j):
				continue
			if j.name not in ignore_tags:
				if len(j.text)<50:
					j.extract()
	return soup
def process(url, html_source):
	soup = BeautifulSoup(re.sub(r'\n','<br>',html_source), 'html.parser')
	h1 = soup.h1.text
	title = soup.title.text
	try:
		host = urlparse(url).netloc
	except Exception as e:
		host = "invalid url"
	imgs = soup.findAll('img')

	#absolute url
	for i in imgs:
		if i.get('src'):
			i['src'] = urljoin(url, i['src'])
	#############

	##clean
	soup = clean(soup)
	#######

	with open("temp.html", "w") as f:
		f.write(str(soup))


	soup = lxml.html.tostring(cleaner.clean_html(lxml.html.parse('temp.html')))
	soup = BeautifulSoup(soup,'html.parser')
	with open("temp.html", "w") as f:
		f.write(str(soup))

	k = {"url": url, "host": host, "h1": h1, "title": title, "content": str(soup)}
	return k #data type is json/dict



url = "https://www.chittorgarh.com/report/ipo-in-india-list-main-board-sme/82/"
print(process(url, open("tes.html").read()))
