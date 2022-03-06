from selenium import webdriver
import time 
import requests
from bs4 import BeautifulSoup as bs

from selenium import webdriver
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

    @classmethod
    def get_row(cls, Brand_car):
        return cls.get(Brand_car == Brand_car)

    @classmethod
    def row_exists(cls, Brand_car):
        query = cls().select().where(cls.Brand_car == Brand_car)
        return query.exists()

    @classmethod
    def creat_row(cls, Brand_car, Model, Saite):
        user, created = cls.get_or_create(Brand_car=Brand_car,Saite=Saite, Model=Model)


db.create_tables([Auto])
db.create_tables([Users])

marka = '' # aixam, 
model = '' # city, crossline
price_start = ''
price_stop = ''
year_start = ''
year_stop = ''
petrol ='' # petrol, diesel
transmission = '' # manual, automatic


def Olx_pars(Brand, Model, Years_start, Years_stop, Price_start,Price_stop, Petrol, KPP):



    link = f'https://www.olx.pl/motoryzacja/samochody/{marka}/{model}/?search%5Bfilter_float_price%3Afrom%5D={price_start}&search%5Bfilter_float_price%3Ato%5D={price_stop}&search%5Bfilter_float_year%3Afrom%5D={year_start}&search%5Bfilter_float_year%3Ato%5D={year_stop}&search%5Bfilter_enum_petrol%5D%5B0%5D={petrol}&search%5Bfilter_enum_transmission%5D%5B0%5D={transmission}=m'
#https://www.olx.pl/motoryzacja/samochody/bmw/?search%5Bfilter_float_price%3Afrom%5D=&search%5Bfilter_float_price%3Ato%5D=&search%5Bfilter_float_year%3Afrom%5D=2000&search%5Bfilter_float_year%3Ato%5D=2001&search%5Bfilter_enum_petrol%5D%5B0%5D=&search%5Bfilter_enum_transmission%5D%5B0%5D=manual

#https://www.olx.pl/motoryzacja/samochody/bmw/?search%5Bfilter_float_year%3Afrom%5D=2000&search%5Bfilter_float_year%3Ato%5D=2001&search%5Bfilter_enum_transmission%5D%5B0%5D=automatic  
#https://www.olx.pl/samochody/bmw/?search[filter_float_price:from]=&search[filter_float_price:to]=&search[filter_float_year:from]=2000&search[filter_float_year:to]=2001&search[filter_enum_petrol][0]=&search[filter_enum_transmission][0]=automatic


    chrome_options = Options()  
    chrome_options.add_argument("--disable-javascript")
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=chrome_options)
    link = ['https://www.olx.pl/motoryzacja/samochody/volvo/',
    'https://www.olx.pl/motoryzacja/samochody/volkswagen/',
    'https://www.olx.pl/motoryzacja/samochody/toyota/',
    'https://www.olx.pl/motoryzacja/samochody/suzuki/',
    'https://www.olx.pl/motoryzacja/samochody/subaru/',
    'https://www.olx.pl/motoryzacja/samochody/ssangyong/',
    'https://www.olx.pl/motoryzacja/samochody/smart/',
    'https://www.olx.pl/motoryzacja/samochody/skoda/',
    'https://www.olx.pl/motoryzacja/samochody/seat/',
    'https://www.olx.pl/motoryzacja/samochody/saab/',
    'https://www.olx.pl/motoryzacja/samochody/']
    for link in link:

        driver.get(link)
        time.sleep(4)


        # element = driver.find_element_by_id("list-item-171-4")
        # element.location_once_scrolled_into_view


        driver.find_element_by_xpath('/html/body/div[1]/header/div[3]/div/form/noindex/div/fieldset[2]/ul/li[1]/ul/li/div[2]/a').click()

        ls = driver.find_element_by_xpath('/html/body/div[1]/header/div[3]/div/form/noindex/div/fieldset[2]/ul/li[1]/ul/li/div[2]/ul').find_elements_by_xpath('.//li')[1:-1]

        for i in ls:
            if i.text != '':
                link_s = link.split('/')[-2]
                name_brand = link_s.capitalize()

                Auto.creat_row(name_brand, i.text, 'olx')



    # if not driver.find_elements_by_xpath('/html/body/div[1]/div[5]/section/div[3]/div/div[1]/table[1]/tbody/tr[1]/td/div/h2/a'):
    #     print('Авто нет.')
    #     return

    # all_link = driver.find_element_by_xpath('/html/body/div[1]/div[5]/section/div[3]/div/div[1]/table[1]/tbody/tr[1]/td/div/h2/a').get_attribute('href')
    # driver.get(all_link)#+str('&search%5Bpaidads_listing%5D=1&page=2'))
    # time.sleep(4)

    # if not driver.find_elements_by_xpath('//div[@class="pager rel clr"]'):
    #     table = driver.find_element_by_xpath('//table[@id="offers_table"]/tbody').find_elements_by_xpath('.//tr[@class="wrap"]')

    #     for el in table:
    #         link_page = el.find_element_by_xpath('.//tbody')
    #         link_page = link_page.find_elements_by_xpath('.//tr')[0]

    #         prices = link_page.find_elements_by_xpath('.//td')[2]
    #         prices = prices.find_element_by_xpath('.//strong').text

    #         link_page = link_page.find_elements_by_xpath('.//td')[0]

    #         img = link_page.find_element_by_xpath('.//img').get_attribute('src')

    #         link_page = link_page.find_element_by_xpath('.//a').get_attribute('href')



    #         print(link_page, img, prices)


    # else:
    #     for el in [1, 2, 3, 4]:
    #         driver.get(all_link+str(f'&search%5Bpaidads_listing%5D=1&page={el}'))
    #         time.sleep(4)

    #         table = driver.find_element_by_xpath('//table[@id="offers_table"]/tbody').find_elements_by_xpath('.//tr[@class="wrap"]')

    #         for el in table:
    #             link_page = el.find_element_by_xpath('.//tbody')
    #             link_page = link_page.find_elements_by_xpath('.//tr')[0]

    #             prices = link_page.find_elements_by_xpath('.//td')[2]
    #             prices = prices.find_element_by_xpath('.//strong').text

    #             link_page = link_page.find_elements_by_xpath('.//td')[0]

    #             img = link_page.find_element_by_xpath('.//img').get_attribute('src')

    #             link_page = link_page.find_element_by_xpath('.//a').get_attribute('href')



    #             print(link_page, img, prices)

marka = '' # aixam, 
model = '' # city, crossline
price_start = ''
price_stop = ''
year_start = ''
year_stop = ''
petrol ='' # petrol, diesel
transmission = '' # manual, automatic
Olx_pars(marka, model, year_start, year_stop, price_start,price_stop, petrol, transmission)
