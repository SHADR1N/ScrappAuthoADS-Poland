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

db = peewee.SqliteDatabase('tbot.db')
class BaseModel(peewee.Model):
    class Meta:
        database = db

class Users(BaseModel):
    USERID = peewee.IntegerField()
    Brand = peewee.TextField(default = '')
    Model = peewee.TextField(default = '')
    Price_start = peewee.IntegerField(default = '')
    Price_stop = peewee.IntegerField(default = '')
    Years_start = peewee.IntegerField(default = '')
    Years_stop = peewee.IntegerField(default = '')
    Petrol = peewee.TextField(default = '')
    KPP = peewee.TextField(default = '')
    Saite = peewee.TextField(default = '')
    Private = peewee.TextField(default = 'User')
    Subcribe = peewee.TextField( default = 'No' )
    Admin_user = peewee.TextField( null = True)
    Time_subs = peewee.IntegerField( default = 0)


    @classmethod
    def get_row(cls, ChatID):
        return cls.get(ChatID == ChatID)

    @classmethod
    def row_exists(cls, USERID):
        query = cls().select().where(cls.USERID == USERID)
        return query.exists()

    @classmethod
    def creat_row(cls, USERID):
        user, created = cls.get_or_create(USERID=USERID)


class Auto(BaseModel):
    Brand_car = peewee.IntegerField()
    Saite = peewee.TextField()
    Model = peewee.TextField()
    Links = peewee.TextField()
    Link_model = peewee.TextField()

    @classmethod
    def get_row(cls, Brand_car):
        return cls.get(Brand_car == Brand_car)

    @classmethod
    def row_exists(cls, Brand_car):
        query = cls().select().where(cls.Brand_car == Brand_car)
        return query.exists()

    @classmethod
    def row_exists__(cls, Brand_car, Model, Saite):
        query = cls().select().where(cls.Brand_car == Brand_car, cls.Model == Model, cls.Saite == Saite)
        return query.exists()


    @classmethod
    def creat_row(cls, Brand_car):
        user, created = cls.get_or_create(Brand_car=Brand_car)

    @classmethod
    def creat_row__(cls, Brand_car, Saite, Model, Links, Link_model):
        user, created = cls.get_or_create(Brand_car=Brand_car, Saite=Saite, Model=Model, Links=Links, Link_model=Link_model)


class Auto_result(BaseModel):
    USERID = peewee.IntegerField()
    Link = peewee.TextField()
    IMG = peewee.TextField()
    Price = peewee.TextField()
    Status = peewee.TextField(null=True)
    Year_facts = peewee.TextField()
    Km_longer = peewee.TextField()


    @classmethod
    def get_row(cls, USERID):
        return cls.get(USERID == USERID)

    @classmethod
    def row_exists(cls, USERID):
        query = cls().select().where(cls.USERID == USERID)
        return query.exists()


    @classmethod
    def row_exists(cls, USERID):
        query = cls().select().where(cls.USERID == USERID)
        return query.exists()


    @classmethod
    def creat_row(cls, USERID, link_page, img, prices, Year_facts):
        user, created = cls.get_or_create(USERID=USERID, Link=link_page, IMG=img, Price=prices, Year_facts=Year_facts)



db.create_tables([Auto_result])
db.create_tables([Auto])
db.create_tables([Users])




Brand = 'BMW'
Years_start = 2000
Years_stop = 2020
Price_start = 100
Price_stop = 12000
Model = '540'
KPP = 'M' # M мех A авто
Petrol = 'B' # B бенз D дизель

link = f'https://www.autoscout24.ru/lst/{Brand}/{Model}?sort=standard&desc=0&gear={KPP}&fuel={Petrol}&ustate=N%2CU&size=20&page=1&priceto={Price_stop}&pricefrom={Price_start}&fregto={Years_stop}&fregfrom={Years_start}'

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0(X11;Linux x86_64...)Geco/20100101 Firefox/60.0'}

session = requests.session()
request = session.get(link, headers=headers)
if request.status_code == 200:
    soup = bs(request.content, 'html.parser')

    if not soup.findAll('div', class_='cl-list-element cl-list-element-gap'):
    	return


    main = soup.findAll('div', class_='cl-list-element cl-list-element-gap' )

    for el in main:
    	price = el.find('span', class_='cldt-price sc-font-xl sc-font-bold').text.strip()

    	Km_longer = el.find('ul', attrs={"data-item-name" : "vehicle-details"}).find('li', attrs={"data-type" : "mileage"}).text.strip()
    	Date = el.find('ul', attrs={"data-item-name" : "vehicle-details"}).find('li', attrs={"data-type" : "first-registration"}).text.strip()
    	Links = el.find('a', attrs={"data-item-name" : "detail-page-link"}).get('href').strip()
    	Links = 'https://www.autoscout24.ru'+str(Links)

    	print(price, Km_longer, Date, Links)
