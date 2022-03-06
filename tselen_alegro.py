from selenium import webdriver
import time 
import requests
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import peewee



#https://allegro.pl/kategoria/osobowe-abarth-300565?price_to=25000&price_from=9000&rodzaj-paliwa=Benzyna&
#https://allegro.pl/kategoria/osobowe-audi-4031?price_to=25000&price_from=9000&rodzaj-paliwa=Benzyna

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
    def creat_row__(cls, Brand, Links, Saite, Model, Link_model):
        user, created = cls.get_or_create(Brand_car=Brand,Saite=Saite, Links=Links, Model=Model, Link_model=Link_model)




db.create_tables([Auto])
db.create_tables([Users])



link = 'https://allegro.pl/kategoria/samochody-osobowe-4029'


def start(link):


    chrome_options = Options()  
    chrome_options.add_argument("--disable-javascript")
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=chrome_options)

    driver.get(link)

    time.sleep(3)

    lis = driver.find_element_by_xpath('//div[@data-role="Categories"]').find_element_by_xpath('.//ul').find_elements_by_xpath('.//li[@data-role="LinkItem"]')
    xxx = []
    for el in lis:

        time.sleep(0.2)

        element = el.find_element_by_xpath(".//div")
        element.location_once_scrolled_into_view

        Brand = el.find_element_by_xpath('.//div').find_element_by_xpath('.//a').text.strip()
        Link = el.find_element_by_xpath('.//div').find_element_by_xpath('.//a').get_attribute('href').strip()
        Saite = 'allegro'
        #print(Brand)
        xxx.append([ Brand, Link ])
            #print('\n\n',Brand)
        # if not Auto.row_exists(Link):
        #     Auto.creat_row(Link, Brand, Saite)

    for ele in xxx:
        print(ele[0], ele[1])
        driver.get(ele[1])
        time.sleep(3)


        lis = driver.find_element_by_xpath('//div[@data-role="Categories"]').find_element_by_xpath('.//ul').find_elements_by_xpath('.//li[@data-role="LinkItem"]')

        for elem in lis:

            time.sleep(0.2)
            element = elem.find_element_by_xpath(".//div")
            element.location_once_scrolled_into_view
            
            if  driver.find_elements_by_xpath('button[@data-role="ToggleButton"]'):
                Link = ele[1]
                Brand = ele[0]
                Saite = 'allegro'

                if not Auto.row_exists(Link):
                    Auto.creat_row(Link, Brand, Saite)

                continue

            Model = elem.find_element_by_xpath('.//div')

            if not Model.find_elements_by_xpath('.//a'):

                continue

            else:
                Model = Model.find_element_by_xpath('.//a').text.strip()

            Link_model = elem.find_element_by_xpath('.//div').find_element_by_xpath('.//a').get_attribute('href').strip()
            Saite = 'allegro'
            Brand = ele[0]
            Links = ele[1]

            if not Auto.row_exists__(Brand, Model, Saite):
                #if Brand != None or Links != None or Model != None or Link_model != None or Brand != '' or Links != '' or Model != '' or Link_model != '':
                    Auto.creat_row__(Brand, Links, Saite, Model, Link_model)
                    print(Brand, Model, Links, Link_model, '\n')


start(link)



add = '?price_to={Price_start}&price_from={Price_stop}&rodzaj-paliwa={Petrol}&bmatch=cl-dict201214-ctx-aut-1-1-0112&p=1'