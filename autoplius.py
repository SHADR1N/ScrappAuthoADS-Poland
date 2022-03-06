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


Years_start = ''
Years_stop = 2020
Money_start = 100
Money_stop = ''
Make_id = 104
Model = 18753
KPP = 38 # 38 автомат 37 механ
Petrol = 30 # 30 бензин 32 дизель

def Get_car():
    link = f'https://ru.m.autoplius.lt/objavlenija/b-u-avtomobili?slist=1353278043&category_id=2&make_date_from={Years_start}&make_date_to={Years_stop}&make_id%5B{Make_id}%5D={Model}&sell_price_from={Money_start}&sell_price_to={Money_stop}&gearbox_id={KPP}&fuel_id[{Petrol}]={Petrol}'
    print(link)

    headers = {'accept': '*/*',
               'user-agent': 'Mozilla/5.0(X11;Linux x86_64...)Geco/20100101 Firefox/60.0'}

    session = requests.session()
    request = session.get(link, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')

        if soup.findAll('ul', class_='auto-list list ru'):
            Main = soup.find('ul', class_='auto-list list ru')
            li_all = Main.findAll('li')

            for el in li_all:
                if el.findAll('a', class_='item'):
                    Name = el.find( 'strong', class_='title-list').text.strip()
                    price = el.find('div', class_='price-list').find('strong').text.strip()
                    if len(el.find('div', class_='param-list-row-block').findAll('div')[0].findAll('span')) == 2:
                        Date = el.find('div', class_='param-list-row-block').findAll('div')[0].findAll('span')[0].text.strip()
                        Longer = el.find('div', class_='param-list-row-block').findAll('div')[0].findAll('span')[1].text.strip()

                    else:
                        Date = el.find('div', class_='param-list-row-block').findAll('div')[0].findAll('span')[0].text.strip()
                        Longer = 'Не известно'

                    print(Name, price, Date, Longer)


def Get_list():
    link = 'https://ru.m.autoplius.lt/poisk/vybor-znacheniya/b-u-avtomobili?field_name=make_id&parent_value_id=104&qt=&qt_autocomplete=&slist=1353278043&category_id=2'
    headers = {'accept': '*/*',
               'user-agent': 'Mozilla/5.0(X11;Linux x86_64...)Geco/20100101 Firefox/60.0'}

    session = requests.session()
    request = session.get(link, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        All = soup.find('ul', class_='search-field-selector field-column').findAll('li')
        x = []
        for el in All:
            asd = (el['id'])
            if 'item' in asd:
                item_name = el.find('a').text.strip()
                item_name_close = el.find('a').find('span').text.strip()

                item_name = item_name.replace(item_name_close, '')

                item_href = el.find('a').get('href').strip()
                item_id = asd.split('_')[1].strip()
                data_car = [item_id, item_name, item_href]
                x.append(data_car)
                #print(item_id, item_name, item_href)

        Start_pars(x)


def Start_pars(x):

    for el in x:
        ID = el[0]
        Name = el[1]
        link = el[2]

        headers = {'accept': '*/*',
                   'user-agent': 'Mozilla/5.0(X11;Linux x86_64...)Geco/20100101 Firefox/60.0'}

        session = requests.session()
        request = session.get(link, headers=headers)
        if request.status_code == 200:
            soup = bs(request.content, 'html.parser')

            All = soup.find('ul', class_='search-field-selector field-column').findAll('li')

            for ele in All[1:]:
                asd = (ele['id'])
                if 'item' in asd:
                    item_name = ele.find('a').text.strip()
                    item_name_close = ele.find('a').find('span').text.strip()

                    item_name = item_name.replace(item_name_close, '')

                    item_id = asd.split('_')[1].strip()
                    data_car = [item_id, item_name]
                    Model = item_name

                    if not Auto.row_exists__(Name, Model, 'autoplius'):
                        print(ID, Name, item_id, item_name)
                        Auto.creat_row__(Name, 'autoplius', Model, ID, item_id)


for el in range(0, 10):
    print(el)
    Get_list()