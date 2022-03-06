from selenium import webdriver
import time 
import requests
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import peewee


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
    Brand_car = peewee.TextField()
    Model = peewee.TextField()
    Saite = peewee.TextField()
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
    def creat_row(cls, Link, Brand, Saite):
        user, created = cls.get_or_create(Brand_car=Brand,Saite=Saite, Links=Link)



    @classmethod
    def row_exists__(cls, Brand, Model, Saite):
        query = cls().select().where(cls.Brand_car == Brand, cls.Model == Model, cls.Saite == Saite)
        return query.exists()

    @classmethod
    def creat_row_(cls, Brand, Saite, Model):
        user, created = cls.get_or_create(Brand_car=Brand,Saite=Saite, Model=Model)




db.create_tables([Auto])
db.create_tables([Users])

link = 'https://www.otomoto.pl/osobowe/?search%5Border%5D=created_at%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D='

def start(link):


    chrome_options = Options()  
    chrome_options.add_argument("--disable-javascript")
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=chrome_options)

    driver.get(link)
    time.sleep(3)

    Brand = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div/form/noindex/fieldset[2]/ul/li[2]/div/div')
    Brand.click()

    Brand = Brand.find_element_by_xpath('.//select').find_elements_by_xpath('.//option')
    x = []
    for i in Brand:
        a = (i.get_attribute('value').capitalize())
        #print(a)
        x.append(a)


    for ele in x:
        u = ele.replace(' ', '-')
        pr = f'https://www.otomoto.pl/osobowe/{u}/?search%5Border%5D=created_at%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D='

        driver.get(pr)
        time.sleep(3)

        Model = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div/form/noindex/fieldset[2]/ul/li[3]/div/div')
        Model.click()

        Model = Model.find_element_by_xpath('.//select').find_elements_by_xpath('.//option')

        for i in Model[1:]:
            Brand = ele.capitalize()
            i.location_once_scrolled_into_view
            time.sleep(0.1)
            Model = i.get_attribute('value').capitalize()
            Saite = 'otomoto'
            if not Auto.row_exists__(Brand, Model, Saite):
                Auto.creat_row_(Brand, Saite, Model)
                print(Brand, Model)


start(link)
# Brand = ''
# Model = ''
# Price_start = ''
# Price_stop = ''
# Years_start = ''
# Years_stop = ''
# Petrol = '' # petrol, diesel


# f'https://www.otomoto.pl/osobowe/{Brand}/{Model}/od-{Years_start}/?search%5Bfilter_float_price%3Afrom%5D=Price_start&search%5Bfilter_float_price%3Ato%5D={Price_stop}&search%5Bfilter_float_year%3Ato%5D={Years_stop}&search%5Bfilter_enum_fuel_type%5D%5B0%5D={Petrol}&search%5Border%5D=created_at%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D='
# f'https://www.otomoto.pl/osobowe/{Brand}/{Model}/od-{Years_start}/?search%5Bfilter_float_price%3Afrom%5D={Price_start}&search%5Bfilter_float_price%3Ato%5D={Price_stop}&search%5Bfilter_float_year%3Ato%5D={Years_stop}&search%5Bfilter_enum_fuel_type%5D%5B0%5D={Petrol}&search%5Border%5D=created_at%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D='