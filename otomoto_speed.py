import time
import peewee
from selenium import webdriver
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import threading
from bs4 import BeautifulSoup as bs
import requests


link = 'https://www.otomoto.pl/osobowe/'

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0(X11;Linux x86_64...)Geco/20100101 Firefox/60.0'}

session = requests.session()
request = session.get(link, headers=headers)
if request.status_code == 200:
    soup = bs(request.content, 'html.parser')

    if not soup.findAll('div', class_='offers list'):
    	print('No')
    else:
    	main = soup.find('div', class_='offers list')
    	article = main.findAll('article')

    	for el in article:
            Year_facts = el.find('ul', class_='ds-params-block').find('li', attrs={"data-code" : "year"}).text.strip()
            Km_longer = el.find('ul', class_='ds-params-block').find('li', attrs={"data-code" : "mileage"}).text.strip()

            prices = el.findAll('div')[1].find('span', class_='offer-price__number ds-price-number').findAll('span')[0].text.strip()
            prices = str(prices) + ' PLN'
            link_page = el.findAll('div')[1].find('a', class_='offer-title__link').get('href')
            IMG = link_page
            print(Year_facts, Km_longer, prices, link_page)
