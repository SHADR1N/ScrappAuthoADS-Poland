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

class Auto(BaseModel):
    Brand_car = peewee.TextField()
    Model = peewee.TextField()
    Saite = peewee.TextField()
    Links = peewee.TextField()

    @classmethod
    def get_row(cls, Brand_car):
        return cls.get(Brand_car == Brand_car)

    @classmethod
    def row_exists(cls, Brand_car, Model, Saite):
        query = cls().select().where(cls.Brand_car == Brand_car, cls.Model==Model, cls.Saite == Saite)
        return query.exists()

    @classmethod
    def creat_row(cls, Brand_car, Model, Saite):
        user, created = cls.get_or_create(Brand_car=Brand_car,Saite=Saite, Model=Model)


db.create_tables([Auto])


chrome_options = Options()  
chrome_options.add_argument("--disable-javascript")
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=chrome_options)

link = 'https://www.autoscout24.ru/lst'

driver.get(link)
time.sleep(6)


main = driver.find_element_by_xpath('/html/body/div[1]/div[9]/div[4]/div[2]/div[4]/div[1]/div/div/div[1]/div[2]/div[1]/div[1]/div[1]/div/div/div/div[1]/div/input')
main.click()

list_car = []

time.sleep(2)
for el in main.find_element_by_xpath('//div[@class="as24-grouped-suggestions-list react-autocomplete__list react-autocomplete__list--visible"]').find_elements_by_xpath('.//li')[:-1]:
	el.location_once_scrolled_into_view
	#print(el.text)
	list_car.append(el.text)


for ele in list_car:
	car = ele.strip().replace(' ', '-')
	driver.get( f'https://www.autoscout24.ru/lst/{car}' )
	time.sleep(3)

	main2 = driver.find_element_by_xpath('/html/body/div[1]/div[9]/div[4]/div[2]/div[4]/div[1]/div/div/div[1]/div[2]/div[1]/div[1]/div[2]/div/div/div/div/div/input')
	main2.click()

	for elem in driver.find_element_by_xpath('//div[@class="react-autocomplete__list react-autocomplete__list--visible"]').find_elements_by_xpath('.//li')[:-1]:
		Models = elem.text
		Name = ele

		if not Auto.row_exists(Name, Models, 'autoscout24'):
			print(Name, Models)
			Auto.creat_row(Name, Models, 'autoscout24')


