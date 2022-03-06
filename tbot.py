import telebot
from telebot import types
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
import configparser
from SimpleQIWI import *


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
    Balance = peewee.IntegerField(default = 0)

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
    def row_exists__(cls, Brand_car):
        query = cls().select().where(cls.Brand_car == Brand_car)
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


sub_month = 150

config = configparser.ConfigParser()
config.read("config.ini")

token_qiwi = '' 
phone = ''

token = config['config']['token']
bot = telebot.TeleBot(token)

@bot.message_handler(commands=["admin"])
def start(message):
    USERID = message.chat.id
    
    if not Users.row_exists(USERID):
        Users.creat_row(USERID)

    if Users.get(Users.USERID == USERID).Private == 'Admin':

        knb = types.InlineKeyboardMarkup(row_width=1)
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['Рассылка по пользователям', 'Вкл/Выкл подписки', 'Добавить администратора', '🏠 Главное меню']])
        subs_activate = []
        subs_disable = []
        subs_test = []
        for el in Users.select():
            if el.Subcribe == 'Yes':
                subs_activate.append(el.USERID)

            if el.Subcribe == 'No':
                subs_disable.append(el.USERID)

            if el.Subcribe == 'Test':
                subs_test.append(el.USERID)

        msg = f'🔐 Админ панель\n\n👥 Кол-во пользователей: { len(Users.select()) }\n✅ Активных подписок: { len(subs_activate) }\n❌ Не активных подписок: { len(subs_disable) }\n⚠️ Тестовых подписок: { len(subs_test) }'
        bot.send_message(USERID, msg ,reply_markup=knb, parse_mode="Html")



    else:
        bot.send_message(USERID, 'Вы не обладаете правами доступа...\n\nДля продолжения работы нажмите /start')

def Status_subs(message):
    USERID = message.chat.id
    txt = message.text

    if txt != '/cancel':
        # Записать в переменную 
        # Определить подписку
        if txt.isdigit() == True and Users.row_exists(txt) == True:
            au = Users.get(Users.USERID == USERID)
            au.Admin_user = txt
            au.save()
            status = Users.get(Users.USERID == txt ).Subcribe
            TimeActive = Users.get(Users.USERID == txt ).Time_subs
            TimeActive = int(TimeActive) / 60 / 60 / 24
            if status == 'No':
                status = 'Не активная'

            if status == 'Yes':
                status = 'Активная'

            if status == 'Test':
                status = 'Тестовый период'

            knb = types.InlineKeyboardMarkup(row_width=1)
            knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['✅ Активировать', '❌ Деактивировать', '🏠 Главное меню']])

            bot.send_message(USERID, f'пользователь: {txt}\n\nСтатус подписки: {status}\nВремя подписки: {TimeActive}',reply_markup=knb, parse_mode="Html")

        else:
            sent = bot.send_message(message.chat.id, 'ID не найден... Попробуйте снова\n\nДля отменыт нажмите /cancel')
            bot.register_next_step_handler(sent, Status_subs)

    else:
        knb = types.InlineKeyboardMarkup(row_width=1)
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['Рассылка по пользователям', 'Вкл/Выкл подписки', 'Добавить администратора', '🏠 Главное меню']])
        subs_activate = []
        subs_disable = []
        subs_test = []
        for el in Users.select():
            if el.Subcribe == 'Yes':
                subs_activate.append(el.USERID)

            if el.Subcribe == 'No':
                subs_disable.append(el.USERID)

            if el.Subcribe == 'Test':
                subs_test.append(el.USERID)

        msg = f'🔐 Админ панель\n\n👥 Кол-во пользователей: { len(Users.select()) }\n✅ Активных подписок: { len(subs_activate) }\n❌ Не активных подписок: { len(subs_disable) }\n⚠️ Тестовых подписок: { len(subs_test) }'
        bot.send_message(USERID, msg ,reply_markup=knb, parse_mode="Html")



def new_admin(message):
    USERID = message.chat.id
    us = message.text
    if us != '/cancel':


        if us.isdigit() == True and Users.row_exists(us) == True:
            u = Users.get(Users.USERID == us)
            u.Private = 'Admin'
            u.save()
            bot.send_message(message.chat.id, 'Администратор добавлен!')

        else:
            sent = bot.send_message(message.chat.id, 'ID не найден... Попробуйте снова\n\nДля отменыт нажмите /cancel')
            bot.register_next_step_handler(sent, new_admin)



    else:
        knb = types.InlineKeyboardMarkup(row_width=1)
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['Рассылка по пользователям', 'Вкл/Выкл подписки', 'Добавить администратора', '🏠 Главное меню']])
        subs_activate = []
        subs_disable = []
        subs_test = []
        for el in Users.select():
            if el.Subcribe == 'Yes':
                subs_activate.append(el.USERID)

            if el.Subcribe == 'No':
                subs_disable.append(el.USERID)

            if el.Subcribe == 'Test':
                subs_test.append(el.USERID)

        msg = f'🔐 Админ панель\n\n👥 Кол-во пользователей: { len(Users.select()) }\n✅ Активных подписок: { len(subs_activate) }\n❌ Не активных подписок: { len(subs_disable) }\n⚠️ Тестовых подписок: { len(subs_test) }'
        bot.send_message(USERID, msg ,reply_markup=knb, parse_mode="Html")

@bot.message_handler(commands=["start"])
def start(message):
    USERID = message.chat.id

    if not Users.row_exists(USERID):
        Users.creat_row(USERID)
        a = Users.get(Users.USERID == USERID)
        a.Time_subs = (time.time()) + int(259200)
        a.Subcribe = 'Yes'
        a.save()


    knb = types.InlineKeyboardMarkup(row_width=2)
    knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['👤 Личный кабинет']])
    knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🚔 Проверка авто по VIN', '🧮 Рассчитать таможню', '🔎 Поиск автомобилей']])
    bot.send_message(USERID, text = f'👋 Привет, @{message.chat.username}.\nРады тебя видеть! Находи автомобили быстро и не выходя из Телегам!',reply_markup=knb, parse_mode="Html")


@bot.callback_query_handler(func=lambda c: True)
def inline(x):
    USERID = x.message.chat.id
    MESSAGE = x.message.message_id

    if x.data == '💳 Оплатить подписку':

        knb = types.InlineKeyboardMarkup(row_width=2)
        knb.add(*[types.InlineKeyboardButton(text='💸 Оплатить', url = 'https://oplata.qiwi.com/form?invoiceUid=58743bad-9b37-4cb5-89dd-984fd7a56535')])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['♻️ Проверить оплату']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['👤 Личный кабинет']])
        bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text = f'<b>Стоимость подписки в месяц:\n\n150 RUB (рубли)\n2 USD (доллары)\n55 UAH (гривны)</b>\n\nПерейдите по ссылке и оплатите подписку!',reply_markup=knb, parse_mode="Html")

    if x.data == '♻️ Проверить оплату':
        knb = types.InlineKeyboardMarkup(row_width=2)
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['👤 Личный кабинет']])
        bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text = 'Ожидайте модераторы сейчас проверят ваш платеж... Это занимает не более 30 минут с момента оплаты.\n\nПриносим извинения за ожидание🥺',reply_markup=knb, parse_mode="Html")
        for el in Users.select():
            if el.Private == 'Admin':
                bot.send_message(el.USERID, f'Проверьте платеж пользователя...\n\nUsername: @{x.message.chat.username}\n👇Внизу его ID👇')
                bot.send_message(el.USERID, f'{x.message.chat.id}')
                bot.send_message(el.USERID, f'Нажмите /admin для перехода в "Админ панель"')

    if x.data == '👤 Личный кабинет':

        TimeActive = Users.get(Users.USERID == USERID ).Time_subs
        TimeActive = ((  float(TimeActive) - time.time()  )) / 60 / 60 / 24
        Balance = Users.get(Users.USERID == USERID).Balance
        knb = types.InlineKeyboardMarkup(row_width=2)
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['💳 Оплатить подписку', '🚔 Проверка авто по VIN', '🧮 Рассчитать таможню', '🔎 Поиск автомобилей']])
        bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text = f'Ваш ID: {USERID}\nNickname: {x.message.chat.first_name}\nUsername: @{x.message.chat.username}\n\n\nДней подписки: {TimeActive:.2f}',reply_markup=knb, parse_mode="Html")


    if Users.get(Users.USERID == USERID).Subcribe == 'No' and Users.get(Users.USERID == USERID).Private == 'User' and x.data not in ['👤 Личный кабинет', '💳 Оплатить подписку', '♻️ Проверить оплату']:

        knb = types.InlineKeyboardMarkup(row_width=1)
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['👤 Личный кабинет']])
        bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text = 'Срок подписки закончился😔',reply_markup=knb, parse_mode="Html")
        return

    if x.data == '🚔 Проверка авто по VIN' or x.data == '🧮 Рассчитать таможню':

        knb = types.InlineKeyboardMarkup(row_width=2)
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['👤 Личный кабинет']])
        bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text = f'Мы уже в разработке данного функционала, скоро добавим!',reply_markup=knb, parse_mode="Html") 
    Brand = Users.get(Users.USERID==USERID).Brand
    Model = Users.get(Users.USERID==USERID).Model
    Years_stop = Users.get(Users.USERID==USERID).Years_stop
    Years_start = Users.get(Users.USERID==USERID).Years_start
    Price_stop = Users.get(Users.USERID==USERID).Price_stop
    Price_start = Users.get(Users.USERID==USERID).Price_start
    Petrol = Users.get(Users.USERID==USERID).Petrol
    KPP  = Users.get(Users.USERID==USERID).KPP

    if KPP == 'automatic':
        KPP = 'АКПП'

    if KPP == 'manual':
        KPP = 'МКПП'

    if Petrol == 'diesel':
        Petrol = 'Дизель'

    if Petrol == 'petrol':
        Petrol = 'Бензин'


    if 'Olx' in x.data or 'Allegro'  in x.data or 'Otomoto'  in x.data or 'Autoplius'  in x.data or 'Autoscout24'  in x.data:
        u = Users.get(Users.USERID==USERID)
        u.Model = ''
        u.Brand = ''
        u.save()

        Brand = Users.get(Users.USERID==USERID).Brand
        Model = Users.get(Users.USERID==USERID).Model
        Years_stop = Users.get(Users.USERID==USERID).Years_stop
        Years_start = Users.get(Users.USERID==USERID).Years_start
        Price_stop = Users.get(Users.USERID==USERID).Price_stop
        Price_start = Users.get(Users.USERID==USERID).Price_start
        Petrol = Users.get(Users.USERID==USERID).Petrol
        KPP  = Users.get(Users.USERID==USERID).KPP

        if KPP == 'automatic':
            KPP = 'АКПП'

        if KPP == 'manual':
            KPP = 'МКПП'

        if Petrol == 'diesel':
            Petrol = 'Дизель'

        if Petrol == 'petrol':
            Petrol = 'Бензин'


        if 'Olx' in x.data:
            Saite = 'olx'
        if 'Allegro'  in x.data:
            Saite = 'allegro'

        if 'Otomoto'  in x.data:
            Saite = 'otomoto'
        if 'Autoplius'  in x.data:
            Saite = 'autoplius'

        if 'Autoscout24'  in x.data:
            Saite = 'autoscout24'

        u = Users.get(Users.USERID==USERID)
        u.Saite = Saite
        u.save()

        Saite = Users.get(Users.USERID==USERID).Saite
        knb = types.InlineKeyboardMarkup(row_width=2)
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🇵🇱 PL: Olx', '🇵🇱 PL: Allegro', '🇵🇱 PL: Otomoto', '🇱🇹 LT: Autoplius', '🇪🇺 EU: Autoscout24']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🚘 Марка', '📌 Модель']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['⏳ Год', '💷 Цена']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['⚙️ Тип ДВС', '📍 Тип КПП']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🔎 Поиск']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['❌ Сбросить параметры']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['👤 Личный кабинет']])
        bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text = f'Ваш ID: {USERID}\n\n<b>Параметры поиска</b>\n\nИсточник: {Saite}\nМарка: {Brand}\nМодель: {Model}\nГода: {Years_start} - {Years_stop}\nЦена: {Price_start} - {Price_stop}\nТип двигателя: {Petrol}\nТип КПП: {KPP}\n\nДля поиска вам необходимо задать параметры поиска и начать 🔎 Поиск.',reply_markup=knb, parse_mode="Html")



    if x.data == '🏠 Главное меню' or x.data == '🔎 Поиск автомобилей':

        Saite = Users.get(Users.USERID==USERID).Saite
        knb = types.InlineKeyboardMarkup(row_width=2)
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🇵🇱 PL: Olx', '🇵🇱 PL: Allegro', '🇵🇱 PL: Otomoto', '🇱🇹 LT: Autoplius', '🇪🇺 EU: Autoscout24']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🚘 Марка', '📌 Модель']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['⏳ Год', '💷 Цена']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['⚙️ Тип ДВС', '📍 Тип КПП']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🔎 Поиск']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['❌ Сбросить параметры']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['👤 Личный кабинет']])
        bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text = f'Ваш ID: {USERID}\n\n<b>Параметры поиска</b>\n\nИсточник: {Saite}\nМарка: {Brand}\nМодель: {Model}\nГода: {Years_start} - {Years_stop}\nЦена: {Price_start} - {Price_stop}\nТип двигателя: {Petrol}\nТип КПП: {KPP}\n\nДля поиска вам необходимо задать параметры поиска и начать 🔎 Поиск.',reply_markup=knb, parse_mode="Html")

    if x.data == '📍 Тип КПП':

        knb = types.InlineKeyboardMarkup(row_width=2)
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['💪 МКПП', '🦾 АКПП']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🏠 Главное меню']])
        bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text = '❕ Выберите модель:',reply_markup=knb, parse_mode="Html" ) 

    if x.data == '✅ Активировать':
        u = Users.get(Users.USERID == USERID).Admin_user

        au = Users.get(Users.USERID == u)
        au.Subcribe = 'Yes'
        au.Time_subs = time.time()
        au.save()


        status = Users.get(Users.USERID == u ).Subcribe


        TimeActive = Users.get(Users.USERID == u ).Time_subs
        TimeActive = ((int(TimeActive) - time.time())) / 60 / 60 / 24
        if status == 'No':
            status = 'Не активная'

        if status == 'Yes':
            status = 'Активная'

        if status == 'Test':
            status = 'Тестовый период'

        knb = types.InlineKeyboardMarkup(row_width=1)
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['✅ Активировать', '❌ Деактивировать', '🏠 Главное меню']])
        bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text =  f'пользователь: {u}\n\nСтатус подписки: {status}\nВремя подписки: {TimeActive}',reply_markup=knb, parse_mode="Html")


    if x.data == '❌ Деактивировать':
        u = Users.get(Users.USERID == USERID).Admin_user

        au = Users.get(Users.USERID == u)
        au.Subcribe = 'No'
        au.Time_subs = 0
        au.save()
        status = Users.get(Users.USERID == u ).Subcribe
        if Users.get(Users.USERID == u).Subcribe == 'No':
            TimeActive = 0

        if status == 'No':
            status = 'Не активная'

        if status == 'Yes':
            status = 'Активная'

        if status == 'Test':
            status = 'Тестовый период'

        knb = types.InlineKeyboardMarkup(row_width=1)
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['✅ Активировать', '❌ Деактивировать', '🏠 Главное меню']])
        bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text =  f'пользователь: {u}\n\nСтатус подписки: {status}\nВремя подписки: {TimeActive}',reply_markup=knb, parse_mode="Html")

    if x.data == '💪 МКПП':

        model = 'manual'
        u = Users.get(Users.USERID==USERID)
        u.KPP = model
        u.save()

        Brand = Users.get(Users.USERID==USERID).Brand
        Model = Users.get(Users.USERID==USERID).Model
        Years_stop = Users.get(Users.USERID==USERID).Years_stop
        Years_start = Users.get(Users.USERID==USERID).Years_start
        Price_stop = Users.get(Users.USERID==USERID).Price_stop
        Price_start = Users.get(Users.USERID==USERID).Price_start
        Petrol = Users.get(Users.USERID==USERID).Petrol
        KPP  = Users.get(Users.USERID==USERID).KPP

        if KPP == 'automatic':
            KPP = 'АКПП'

        if KPP == 'manual':
            KPP = 'МКПП'

        if Petrol == 'diesel':
            Petrol = 'Дизель'

        if Petrol == 'petrol':
            Petrol = 'Бензин'

        if Model == 'city':
            Model = 'City'

        if Model == 'crossline':
            Model = 'Crossline'

        Saite = Users.get(Users.USERID==USERID).Saite
        knb = types.InlineKeyboardMarkup(row_width=2)
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🇵🇱 PL: Olx', '🇵🇱 PL: Allegro', '🇵🇱 PL: Otomoto', '🇱🇹 LT: Autoplius', '🇪🇺 EU: Autoscout24']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🚘 Марка', '📌 Модель']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['⏳ Год', '💷 Цена']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['⚙️ Тип ДВС', '📍 Тип КПП']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🔎 Поиск']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['❌ Сбросить параметры']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['👤 Личный кабинет']])
        bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text = f'Ваш ID: {USERID}\n\n<b>Параметры поиска</b>\n\nИсточник: {Saite}\nМарка: {Brand}\nМодель: {Model}\nГода: {Years_start} - {Years_stop}\nЦена: {Price_start} - {Price_stop}\nТип двигателя: {Petrol}\nТип КПП: {KPP}\n\nДля поиска вам необходимо задать параметры поиска и начать 🔎 Поиск.',reply_markup=knb, parse_mode="Html")



    if x.data == '🦾 АКПП':

        model = 'automatic'
        u = Users.get(Users.USERID==USERID)
        u.KPP = model
        u.save()


        Brand = Users.get(Users.USERID==USERID).Brand
        Model = Users.get(Users.USERID==USERID).Model
        Years_stop = Users.get(Users.USERID==USERID).Years_stop
        Years_start = Users.get(Users.USERID==USERID).Years_start
        Price_stop = Users.get(Users.USERID==USERID).Price_stop
        Price_start = Users.get(Users.USERID==USERID).Price_start
        Petrol = Users.get(Users.USERID==USERID).Petrol
        KPP  = Users.get(Users.USERID==USERID).KPP

        if KPP == 'automatic':
            KPP = 'АКПП'

        if KPP == 'manual':
            KPP = 'МКПП'

        if Petrol == 'diesel':
            Petrol = 'Дизель'

        if Petrol == 'petrol':
            Petrol = 'Бензин'

        if Model == 'city':
            Model = 'City'

        if Model == 'crossline':
            Model = 'Crossline'

        Saite = Users.get(Users.USERID==USERID).Saite
        knb = types.InlineKeyboardMarkup(row_width=2)
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🇵🇱 PL: Olx', '🇵🇱 PL: Allegro', '🇵🇱 PL: Otomoto', '🇱🇹 LT: Autoplius', '🇪🇺 EU: Autoscout24']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🚘 Марка', '📌 Модель']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['⏳ Год', '💷 Цена']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['⚙️ Тип ДВС', '📍 Тип КПП']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🔎 Поиск']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['❌ Сбросить параметры']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['👤 Личный кабинет']])
        bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text = f'Ваш ID: {USERID}\n\n<b>Параметры поиска</b>\n\nИсточник: {Saite}\nМарка: {Brand}\nМодель: {Model}\nГода: {Years_start} - {Years_stop}\nЦена: {Price_start} - {Price_stop}\nТип двигателя: {Petrol}\nТип КПП: {KPP}\n\nДля поиска вам необходимо задать параметры поиска и начать 🔎 Поиск.',reply_markup=knb, parse_mode="Html")


    if x.data in [i.Model for i in Auto.select()]:
        u = Users.get(Users.USERID==USERID)
        u.Model = x.data 
        u.save()

        Brand = Users.get(Users.USERID==USERID).Brand
        Model = Users.get(Users.USERID==USERID).Model
        Years_stop = Users.get(Users.USERID==USERID).Years_stop
        Years_start = Users.get(Users.USERID==USERID).Years_start
        Price_stop = Users.get(Users.USERID==USERID).Price_stop
        Price_start = Users.get(Users.USERID==USERID).Price_start
        Petrol = Users.get(Users.USERID==USERID).Petrol
        KPP  = Users.get(Users.USERID==USERID).KPP

        if KPP == 'automatic':
            KPP = 'АКПП'

        if KPP == 'manual':
            KPP = 'МКПП'

        if Petrol == 'diesel':
            Petrol = 'Дизель'

        if Petrol == 'petrol':
            Petrol = 'Бензин'

        if Model == 'city':
            Model = 'City'

        if Model == 'crossline':
            Model = 'Crossline'

        Saite = Users.get(Users.USERID==USERID).Saite
        knb = types.InlineKeyboardMarkup(row_width=2)
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🇵🇱 PL: Olx', '🇵🇱 PL: Allegro', '🇵🇱 PL: Otomoto', '🇱🇹 LT: Autoplius', '🇪🇺 EU: Autoscout24']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🚘 Марка', '📌 Модель']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['⏳ Год', '💷 Цена']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['⚙️ Тип ДВС', '📍 Тип КПП']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🔎 Поиск']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['❌ Сбросить параметры']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['👤 Личный кабинет']])
        bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text = f'Ваш ID: {USERID}\n\n<b>Параметры поиска</b>\n\nИсточник: {Saite}\nМарка: {Brand}\nМодель: {Model}\nГода: {Years_start} - {Years_stop}\nЦена: {Price_start} - {Price_stop}\nТип двигателя: {Petrol}\nТип КПП: {KPP}\n\nДля поиска вам необходимо задать параметры поиска и начать 🔎 Поиск.',reply_markup=knb, parse_mode="Html")


    if x.data == 'Добавить администратора':
        sent = bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text = 'Пришлите ID юзера которому хотите дать права администратора.\n\nДля отмены /cancel')
        bot.register_next_step_handler(sent, new_admin)

    if x.data == "📌 Модель":

        a = Users.get(Users.USERID==USERID).Brand
        sas = Users.get(Users.USERID==USERID).Saite
        if sas == 'allegro':
            if a == '':
                knb = types.InlineKeyboardMarkup(row_width=3)
                knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🏠 Главное меню']])
                bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text = '❗️ Вы не выбрали марку автомобиля:',reply_markup=knb, parse_mode="Html" )

            else:

                base_url = Auto.get( Auto.Brand_car == Users.get(Users.USERID==USERID).Brand, Auto.Saite == Users.get(Users.USERID==USERID).Saite ).Links

                headers = {'accept': '*/*',
                           'user-agent': 'Mozilla/5.0(X11;Linux x86_64...)Geco/20100101 Firefox/60.0'}

                session = requests.session()
                request = session.get(base_url, headers=headers)
                if request.status_code == 200:
                    soup = bs(request.content, 'html.parser')

                    MainDiv = soup.find('ul', class_='_1rj80 _1sql3')
                    Div = MainDiv.findAll('li')
                    c = []
                    for i in Div:
                        try:
                            xs = i.find('a', class_='_w7z6o _uj8z7').text
                            url = i.find('a', class_='_w7z6o _uj8z7').get('href')
                            url = str('https://allegro.pl')+str(url)
                            Brand = Users.get(Users.USERID==USERID).Brand
                            Saite = 'allegro'
                            Model = xs
                            Links = base_url
                            Link_model = url
                            if not Auto.row_exists__(url):
                                Auto.creat_row__(Brand, Saite, Model, Links, Link_model)


                            c.append(xs)
                        except:
                            pass


                    knb = types.InlineKeyboardMarkup(row_width=3)
                    knb.add(*[types.InlineKeyboardButton(text=name, callback_data='model_'+str(name)) for name in[ i for i in c ]])
                    knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🏠 Главное меню']])
                    bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text = '❕ Выберите модель:',reply_markup=knb, parse_mode="Html" )

        else:

            a = Users.get(Users.USERID==USERID).Brand
            if a == '':
                knb = types.InlineKeyboardMarkup(row_width=3)
                knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🏠 Главное меню']])
                bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text = '❗️ Вы не выбрали марку автомобиля:',reply_markup=knb, parse_mode="Html" )

            else:
                c = []
                b = Users.get(Users.USERID==USERID).Saite
                for el in Auto.select():
                    if el.Brand_car == a:
                        if el.Saite == b:
                            c.append(el.Model)

                knb = types.InlineKeyboardMarkup(row_width=3)
                knb.add(*[types.InlineKeyboardButton(text=name, callback_data='model_'+str(name)) for name in[ i for i in c ]])
                knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🏠 Главное меню']])
                bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text = '❕ Выберите модель:',reply_markup=knb, parse_mode="Html" )



    if 'model_' in x.data:
        model = x.data.split('_')[1]
        u = Users.get(Users.USERID==USERID)
        u.Model = model
        u.save()


        Brand = Users.get(Users.USERID==USERID).Brand
        Model = Users.get(Users.USERID==USERID).Model
        Years_stop = Users.get(Users.USERID==USERID).Years_stop
        Years_start = Users.get(Users.USERID==USERID).Years_start
        Price_stop = Users.get(Users.USERID==USERID).Price_stop
        Price_start = Users.get(Users.USERID==USERID).Price_start
        Petrol = Users.get(Users.USERID==USERID).Petrol
        KPP  = Users.get(Users.USERID==USERID).KPP

        if KPP == 'automatic':
            KPP = 'АКПП'

        if KPP == 'manual':
            KPP = 'МКПП'

        if Petrol == 'diesel':
            Petrol = 'Дизель'

        if Petrol == 'petrol':
            Petrol = 'Бензин'

        if Model == 'city':
            Model = 'City'

        if Model == 'crossline':
            Model = 'Crossline'

        Saite = Users.get(Users.USERID==USERID).Saite
        knb = types.InlineKeyboardMarkup(row_width=2)
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🇵🇱 PL: Olx', '🇵🇱 PL: Allegro', '🇵🇱 PL: Otomoto', '🇱🇹 LT: Autoplius', '🇪🇺 EU: Autoscout24']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🚘 Марка', '📌 Модель']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['⏳ Год', '💷 Цена']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['⚙️ Тип ДВС', '📍 Тип КПП']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🔎 Поиск']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['❌ Сбросить параметры']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['👤 Личный кабинет']])
        bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text = f'Ваш ID: {USERID}\n\n<b>Параметры поиска</b>\n\nИсточник: {Saite}\nМарка: {Brand}\nМодель: {Model}\nГода: {Years_start} - {Years_stop}\nЦена: {Price_start} - {Price_stop}\nТип двигателя: {Petrol}\nТип КПП: {KPP}\n\nДля поиска вам необходимо задать параметры поиска и начать 🔎 Поиск.',reply_markup=knb, parse_mode="Html")


    if x.data == 'Рассылка по пользователям':
        sent = bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text = 'Введите текст сообщения для пользователей:\n\nДля отмены /cancel' )
        bot.register_next_step_handler(sent, spam)

    if x.data == '⚙️ Тип ДВС':
        knb = types.InlineKeyboardMarkup(row_width=2)
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['⛽️ Бензин', '🛢 Дизель']])

        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🏠 Главное меню']])
        bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text = '❕ Выберите тип ДВС:',reply_markup=knb, parse_mode="Html" )

    if x.data == '⛽️ Бензин':

        model = 'petrol'
        u = Users.get(Users.USERID==USERID)
        u.Petrol = model
        u.save()

        Brand = Users.get(Users.USERID==USERID).Brand
        Model = Users.get(Users.USERID==USERID).Model
        Years_stop = Users.get(Users.USERID==USERID).Years_stop
        Years_start = Users.get(Users.USERID==USERID).Years_start
        Price_stop = Users.get(Users.USERID==USERID).Price_stop
        Price_start = Users.get(Users.USERID==USERID).Price_start
        Petrol = Users.get(Users.USERID==USERID).Petrol
        KPP  = Users.get(Users.USERID==USERID).KPP

        if KPP == 'automatic':
            KPP = 'АКПП'

        if KPP == 'manual':
            KPP = 'МКПП'

        if Petrol == 'diesel':
            Petrol = 'Дизель'

        if Petrol == 'petrol':
            Petrol = 'Бензин'

        if Model == 'city':
            Model = 'City'

        if Model == 'crossline':
            Model = 'Crossline'

        Saite = Users.get(Users.USERID==USERID).Saite
        knb = types.InlineKeyboardMarkup(row_width=2)
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🇵🇱 PL: Olx', '🇵🇱 PL: Allegro', '🇵🇱 PL: Otomoto', '🇱🇹 LT: Autoplius', '🇪🇺 EU: Autoscout24']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🚘 Марка', '📌 Модель']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['⏳ Год', '💷 Цена']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['⚙️ Тип ДВС', '📍 Тип КПП']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🔎 Поиск']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['❌ Сбросить параметры']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['👤 Личный кабинет']])
        bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text = f'Ваш ID: {USERID}\n\n<b>Параметры поиска</b>\n\nИсточник: {Saite}\nМарка: {Brand}\nМодель: {Model}\nГода: {Years_start} - {Years_stop}\nЦена: {Price_start} - {Price_stop}\nТип двигателя: {Petrol}\nТип КПП: {KPP}\n\nДля поиска вам необходимо задать параметры поиска и начать 🔎 Поиск.',reply_markup=knb, parse_mode="Html")


    
    if x.data == '🛢 Дизель':

        model = 'diesel'
        u = Users.get(Users.USERID==USERID)
        u.Petrol = model
        u.save()

        Brand = Users.get(Users.USERID==USERID).Brand
        Model = Users.get(Users.USERID==USERID).Model
        Years_stop = Users.get(Users.USERID==USERID).Years_stop
        Years_start = Users.get(Users.USERID==USERID).Years_start
        Price_stop = Users.get(Users.USERID==USERID).Price_stop
        Price_start = Users.get(Users.USERID==USERID).Price_start
        Petrol = Users.get(Users.USERID==USERID).Petrol
        KPP  = Users.get(Users.USERID==USERID).KPP

        if KPP == 'automatic':
            KPP = 'АКПП'

        if KPP == 'manual':
            KPP = 'МКПП'

        if Petrol == 'diesel':
            Petrol = 'Дизель'

        if Petrol == 'petrol':
            Petrol = 'Бензин'

        if Model == 'city':
            Model = 'City'

        if Model == 'crossline':
            Model = 'Crossline'

        Saite = Users.get(Users.USERID==USERID).Saite
        knb = types.InlineKeyboardMarkup(row_width=2)
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🇵🇱 PL: Olx', '🇵🇱 PL: Allegro', '🇵🇱 PL: Otomoto', '🇱🇹 LT: Autoplius', '🇪🇺 EU: Autoscout24']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🚘 Марка', '📌 Модель']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['⏳ Год', '💷 Цена']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['⚙️ Тип ДВС', '📍 Тип КПП']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🔎 Поиск']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['❌ Сбросить параметры']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['👤 Личный кабинет']])
        bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text = f'Ваш ID: {USERID}\n\n<b>Параметры поиска</b>\n\nИсточник: {Saite}\nМарка: {Brand}\nМодель: {Model}\nГода: {Years_start} - {Years_stop}\nЦена: {Price_start} - {Price_stop}\nТип двигателя: {Petrol}\nТип КПП: {KPP}\n\nДля поиска вам необходимо задать параметры поиска и начать 🔎 Поиск.',reply_markup=knb, parse_mode="Html")

    if x.data == 'Вкл/Выкл подписки':
        sent =  bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text = 'Пришлите ID пользователя:\n\nДля отмены /cancel')
        bot.register_next_step_handler(sent, Status_subs)

    if x.data == '🔎 Поиск':


        Brand = Users.get(Users.USERID==USERID).Brand
        Model = Users.get(Users.USERID==USERID).Model
        Years_stop = Users.get(Users.USERID==USERID).Years_stop
        Years_start = Users.get(Users.USERID==USERID).Years_start
        Price_stop = Users.get(Users.USERID==USERID).Price_stop
        Price_start = Users.get(Users.USERID==USERID).Price_start
        Petrol = Users.get(Users.USERID==USERID).Petrol
        KPP  = Users.get(Users.USERID==USERID).KPP

        bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text = '🔍 Идет поиск, пожалуйста подождите...\n\n😳 Время ожидания может занять до 2 минут...', parse_mode="Html" )

        a = len(Auto_result.select().where(Auto_result.USERID == USERID))
        for i in range(a):
            category = Auto_result.get(Auto_result.USERID == USERID)
            category.delete_instance()


        if Users.get(Users.USERID == USERID).Saite == 'olx':

            t = threading.Thread(target=Olx_pars, args=(USERID, Brand, Model, Years_start, Years_stop, Price_start,Price_stop, Petrol, KPP,))
            t.start()

        if Users.get(Users.USERID == USERID).Saite == 'allegro':
            
            t = threading.Thread(target=allegro_pars, args=(USERID, Brand, Model, Years_start, Years_stop, Price_start,Price_stop, Petrol, KPP,))
            t.start()

        if Users.get(Users.USERID == USERID).Saite == 'otomoto':
            
            t = threading.Thread(target=otomoto_pars, args=(USERID, Brand, Model, Years_start, Years_stop, Price_start,Price_stop, Petrol, KPP,))
            t.start()


        if Users.get(Users.USERID == USERID).Saite == 'autoplius':
            
            t = threading.Thread(target=autoplius_pars, args=(USERID, Brand, Model, Years_start, Years_stop, Price_start,Price_stop, Petrol, KPP,))
            t.start()

        if Users.get(Users.USERID == USERID).Saite == 'autoscout24':
            
            t = threading.Thread(target=autoscout24_pars, args=(USERID, Brand, Model, Years_start, Years_stop, Price_start,Price_stop, Petrol, KPP,))
            t.start()


        xsx = []

        while len(xsx) == 0:
            if Auto_result.row_exists(USERID):
                el = Auto_result.select()
                for el in el:
                    if el.USERID == USERID:
                        if el.Status == 'Stop' or el.Status == 'Авто нет.':

                            if el.Status == 'Авто нет.':

                                bot.send_message(USERID, f'По вашему запросу нет автомобилей!', parse_mode="Html" )
                                xsx.append('asd')
                                break

                            if el.Status == 'Stop':
                                www = Auto_result.select()
                                for el in www:
                                    if el.USERID == USERID:

                                        Price_ = el.Price
                                        IMG = el.IMG
                                        Link = el.Link
                                        Year_facts = el.Year_facts
  
                                        knb = types.InlineKeyboardMarkup(row_width=1)
                                        knb.add(*[types.InlineKeyboardButton(text=name, url=Link) for name in ['🌐 Перейти на страницу']])

                                        bot.send_message(USERID, f'<a href="{IMG}">Цена:  {Price_}</a>\n\n{Year_facts}', reply_markup=knb, parse_mode="Html" )
                                        time.sleep(0.2)
                                        
                                xsx.append('asd')
                                break


            time.sleep(1)



        Brand = Users.get(Users.USERID==USERID).Brand
        Model = Users.get(Users.USERID==USERID).Model
        Years_stop = Users.get(Users.USERID==USERID).Years_stop
        Years_start = Users.get(Users.USERID==USERID).Years_start
        Price_stop = Users.get(Users.USERID==USERID).Price_stop
        Price_start = Users.get(Users.USERID==USERID).Price_start
        Petrol = Users.get(Users.USERID==USERID).Petrol
        KPP  = Users.get(Users.USERID==USERID).KPP

        if KPP == 'automatic':
            KPP = 'АКПП'

        if KPP == 'manual':
            KPP = 'МКПП'

        if Petrol == 'diesel':
            Petrol = 'Дизель'

        if Petrol == 'petrol':
            Petrol = 'Бензин'

        if Model == 'city':
            Model = 'City'

        if Model == 'crossline':
            Model = 'Crossline'


        Saite = Users.get(Users.USERID==USERID).Saite
        knb = types.InlineKeyboardMarkup(row_width=2)
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🇵🇱 PL: Olx', '🇵🇱 PL: Allegro', '🇵🇱 PL: Otomoto', '🇱🇹 LT: Autoplius', '🇪🇺 EU: Autoscout24']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🚘 Марка', '📌 Модель']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['⏳ Год', '💷 Цена']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['⚙️ Тип ДВС', '📍 Тип КПП']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🔎 Поиск']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['❌ Сбросить параметры']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['👤 Личный кабинет']])

        bot.send_message(USERID, text = f'Ваш ID: {USERID}\n\n<b>Параметры поиска</b>\n\nИсточник: {Saite}\nМарка: {Brand}\nМодель: {Model}\nГода: {Years_start} - {Years_stop}\nЦена: {Price_start} - {Price_stop}\nТип двигателя: {Petrol}\nТип КПП: {KPP}\n\nДля поиска вам необходимо задать параметры поиска и начать 🔎 Поиск.',reply_markup=knb, parse_mode="Html")

    if x.data == '❌ Сбросить параметры':
        u = Users.get(Users.USERID==USERID)
        u.Brand = ''
        u.Model = ''
        u.Years_start = ''
        u.Years_stop = ''
        u.Price_stop = ''
        u.Price_start = ''
        u.Petrol = ''
        u.KPP = ''
        u.save()

        Brand = Users.get(Users.USERID==USERID).Brand
        Model = Users.get(Users.USERID==USERID).Model
        Years_stop = Users.get(Users.USERID==USERID).Years_stop
        Years_start = Users.get(Users.USERID==USERID).Years_start
        Price_stop = Users.get(Users.USERID==USERID).Price_stop
        Price_start = Users.get(Users.USERID==USERID).Price_start
        Petrol = Users.get(Users.USERID==USERID).Petrol
        KPP  = Users.get(Users.USERID==USERID).KPP

        if KPP == 'automatic':
            KPP = 'АКПП'

        if KPP == 'manual':
            KPP = 'МКПП'

        if Petrol == 'diesel':
            Petrol = 'Дизель'

        if Petrol == 'petrol':
            Petrol = 'Бензин'

        if Model == 'city':
            Model = 'City'

        if Model == 'crossline':
            Model = 'Crossline'


        Saite = Users.get(Users.USERID==USERID).Saite
        knb = types.InlineKeyboardMarkup(row_width=2)
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🇵🇱 PL: Olx', '🇵🇱 PL: Allegro', '🇵🇱 PL: Otomoto', '🇱🇹 LT: Autoplius', '🇪🇺 EU: Autoscout24']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🚘 Марка', '📌 Модель']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['⏳ Год', '💷 Цена']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['⚙️ Тип ДВС', '📍 Тип КПП']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🔎 Поиск']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['❌ Сбросить параметры']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['👤 Личный кабинет']])

        bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text = f'Ваш ID: {USERID}\n\n<b>Параметры поиска</b>\n\nИсточник: {Saite}\nМарка: {Brand}\nМодель: {Model}\nГода: {Years_start} - {Years_stop}\nЦена: {Price_start} - {Price_stop}\nТип двигателя: {Petrol}\nТип КПП: {KPP}\n\nДля поиска вам необходимо задать параметры поиска и начать 🔎 Поиск.',reply_markup=knb, parse_mode="Html")



    if x.data == '🚘 Марка':

        Car_brand = []
        _car = Auto.select()
        Saite = Users.get(Users.USERID==USERID).Saite

        for el in _car:
            if el.Saite == Saite:
                if el.Brand_car not in Car_brand:
                    Car_brand.append(el.Brand_car)

        knb = types.InlineKeyboardMarkup(row_width=3)

        knb.add(*[types.InlineKeyboardButton(text=f'{name}', callback_data=f'car_{name}') for name in  Car_brand  ])

        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🏠 Главное меню']])
        bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text = '❕ Выберите марку автомобиля:',reply_markup=knb, parse_mode="Html" )


    if x.data == '💷 Цена':

        sent = bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text = 'Введите минимальную цену автомобиля.')
        bot.register_next_step_handler(sent, Money_start_)


    if x.data == '⏳ Год':

        sent = bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text = 'Введите с какого года искать, формат 2001')
        bot.register_next_step_handler(sent, Years_start_add)

    if 'car_' in x.data:

        car = x.data.split('car_')[1]
        u = Users.get(Users.USERID==USERID)
        u.Brand = car
        u.Model = ''
        u.save()

        Brand = Users.get(Users.USERID==USERID).Brand
        Model = Users.get(Users.USERID==USERID).Model
        Years_stop = Users.get(Users.USERID==USERID).Years_stop
        Years_start = Users.get(Users.USERID==USERID).Years_start
        Price_stop = Users.get(Users.USERID==USERID).Price_stop
        Price_start = Users.get(Users.USERID==USERID).Price_start
        Petrol = Users.get(Users.USERID==USERID).Petrol
        KPP  = Users.get(Users.USERID==USERID).KPP

        if KPP == 'automatic':
            KPP = 'АКПП'

        if KPP == 'manual':
            KPP = 'МКПП'

        if Petrol == 'diesel':
            Petrol = 'Дизель'

        if Petrol == 'petrol':
            Petrol = 'Бензин'

        if Model == 'city':
            Model = 'City'

        if Model == 'crossline':
            Model = 'Crossline'

        Saite = Users.get(Users.USERID==USERID).Saite
        knb = types.InlineKeyboardMarkup(row_width=2)
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🇵🇱 PL: Olx', '🇵🇱 PL: Allegro', '🇵🇱 PL: Otomoto', '🇱🇹 LT: Autoplius', '🇪🇺 EU: Autoscout24']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🚘 Марка', '📌 Модель']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['⏳ Год', '💷 Цена']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['⚙️ Тип ДВС', '📍 Тип КПП']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🔎 Поиск']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['❌ Сбросить параметры']])
        knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['👤 Личный кабинет']])
        bot.edit_message_text(chat_id=USERID, message_id=MESSAGE, text = f'Ваш ID: {USERID}\n\n<b>Параметры поиска</b>\n\nИсточник: {Saite}\nМарка: {Brand}\nМодель: {Model}\nГода: {Years_start} - {Years_stop}\nЦена: {Price_start} - {Price_stop}\nТип двигателя: {Petrol}\nТип КПП: {KPP}\n\nДля поиска вам необходимо задать параметры поиска и начать 🔎 Поиск.',reply_markup=knb, parse_mode="Html")




def Money_stop_(message):
    USERID = message.chat.id
    if message.text.isdigit() == True:
        if Users.get(Users.USERID==USERID).Price_start < int(message.text):
            u = Users.get(Users.USERID==USERID)
            u.Price_stop = message.text
            u.save()        

            Brand = Users.get(Users.USERID==USERID).Brand
            Model = Users.get(Users.USERID==USERID).Model
            Years_stop = Users.get(Users.USERID==USERID).Years_stop
            Years_start = Users.get(Users.USERID==USERID).Years_start
            Price_stop = Users.get(Users.USERID==USERID).Price_stop
            Price_start = Users.get(Users.USERID==USERID).Price_start
            Petrol = Users.get(Users.USERID==USERID).Petrol
            KPP  = Users.get(Users.USERID==USERID).KPP

            if KPP == 'automatic':
                KPP = 'АКПП'

            if KPP == 'manual':
                KPP = 'МКПП'

            if Petrol == 'diesel':
                Petrol = 'Дизель'

            if Petrol == 'petrol':
                Petrol = 'Бензин'

            if Model == 'city':
                Model = 'City'

            if Model == 'crossline':
                Model = 'Crossline'

            Saite = Users.get(Users.USERID==USERID).Saite
            knb = types.InlineKeyboardMarkup(row_width=2)
            knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🇵🇱 PL: Olx', '🇵🇱 PL: Allegro', '🇵🇱 PL: Otomoto', '🇱🇹 LT: Autoplius', '🇪🇺 EU: Autoscout24']])
            knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🚘 Марка', '📌 Модель']])
            knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['⏳ Год', '💷 Цена']])
            knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['⚙️ Тип ДВС', '📍 Тип КПП']])
            knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🔎 Поиск']])
            knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['❌ Сбросить параметры']])
            knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['👤 Личный кабинет']])
            bot.send_message(message.chat.id, text = f'Ваш ID: {USERID}\n\n<b>Параметры поиска</b>\n\nИсточник: {Saite}\nМарка: {Brand}\nМодель: {Model}\nГода: {Years_start} - {Years_stop}\nЦена: {Price_start} - {Price_stop}\nТип двигателя: {Petrol}\nТип КПП: {KPP}\n\nДля поиска вам необходимо задать параметры поиска и начать 🔎 Поиск.',reply_markup=knb, parse_mode="Html")


        else:
            sent = bot.send_message(message.chat.id, 'Вы указали не верное значение\nВведите максиммальную цену автомобиля.')
            bot.register_next_step_handler(sent, Money_stop_)

    else:

        sent = bot.send_message(message.chat.id, 'Вы указали не верное значение\nВведите максиммальную цену автомобиля.')
        bot.register_next_step_handler(sent, Money_stop_)


def Money_start_(message):
    USERID = message.chat.id
    if message.text.isdigit() == True:
        u = Users.get(Users.USERID==USERID)
        u.Price_start = message.text
        u.save()        

        sent = bot.send_message(message.chat.id, 'Отлично!\nВведите максиммальную цену автомобиля.')
        bot.register_next_step_handler(sent, Money_stop_)

    else:

        sent = bot.send_message(message.chat.id, 'Вы указали не верное значение\nВведите минимальную цену автомобиля.')
        bot.register_next_step_handler(sent, Money_start_)



def Years_start_add(message):
    USERID = message.chat.id

    if message.text.isdigit() == True:

        if int(message.text) > 1900:
            u = Users.get(Users.USERID==USERID)
            u.Years_start = message.text
            u.save()

            sent = bot.send_message(message.chat.id, 'Введите год по какой искать, формат 2001')    
            bot.register_next_step_handler(sent, Years_stop_add)


        else:
            sent = bot.send_message(message.chat.id, 'Вы указали слишком поздний год, начинайте с 1900.\n\nВведите с какого года искать, формат 2001')
            bot.register_next_step_handler(sent, Years_start_add)


def Years_stop_add(message):
    USERID = message.chat.id

    if message.text.isdigit() == True:

        if int(message.text) > 1900:

            if int(Users.get(Users.USERID==USERID).Years_start) < int(message.text):

                u = Users.get(Users.USERID==USERID)
                u.Years_stop = message.text
                u.save()

                Brand = Users.get(Users.USERID==USERID).Brand
                Model = Users.get(Users.USERID==USERID).Model
                Years_stop = Users.get(Users.USERID==USERID).Years_stop
                Years_start = Users.get(Users.USERID==USERID).Years_start
                Price_stop = Users.get(Users.USERID==USERID).Price_stop
                Price_start = Users.get(Users.USERID==USERID).Price_start
                Petrol = Users.get(Users.USERID==USERID).Petrol
                KPP  = Users.get(Users.USERID==USERID).KPP

                if KPP == 'automatic':
                    KPP = 'АКПП'

                if KPP == 'manual':
                    KPP = 'МКПП'

                if Petrol == 'diesel':
                    Petrol = 'Дизель'

                if Petrol == 'petrol':
                    Petrol = 'Бензин'

                if Model == 'city':
                    Model = 'City'

                if Model == 'crossline':
                    Model = 'Crossline'

                Saite = Users.get(Users.USERID==USERID).Saite
                knb = types.InlineKeyboardMarkup(row_width=2)
                knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🇵🇱 PL: Olx', '🇵🇱 PL: Allegro', '🇵🇱 PL: Otomoto', '🇱🇹 LT: Autoplius', '🇪🇺 EU: Autoscout24']])
                knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🚘 Марка', '📌 Модель']])
                knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['⏳ Год', '💷 Цена']])
                knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['⚙️ Тип ДВС', '📍 Тип КПП']])
                knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['🔎 Поиск']])
                knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['❌ Сбросить параметры']])
                knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['👤 Личный кабинет']])
                bot.send_message(message.chat.id, text = f'Ваш ID: {USERID}\n\n<b>Параметры поиска</b>\n\nИсточник: {Saite}\nМарка: {Brand}\nМодель: {Model}\nГода: {Years_start} - {Years_stop}\nЦена: {Price_start} - {Price_stop}\nТип двигателя: {Petrol}\nТип КПП: {KPP}\n\nДля поиска вам необходимо задать параметры поиска и начать 🔎 Поиск.',reply_markup=knb, parse_mode="Html")



            else:
                sent = bot.send_message(message.chat.id, 'Вы не можете осуществить такой поиск, года не верны...\n\nВведите год по какой искать, формат 2010')    
                bot.register_next_step_handler(sent, Years_stop_add)


        else:
            sent = bot.send_message(message.chat.id, 'Вы указали слишком поздний год, начинайте с 1900.\n\nВведите с какого года искать, формат 2001')
            bot.register_next_step_handler(sent, Years_stop_add)


def allegro_pars(USERID, Brand, Model, Years_start, Years_stop, Price_start,Price_stop, Petrol, KPP):
    Saite = 'allegro'
    if Brand != "":

        for el in Auto.select():
            if str(el.Saite).strip().lower() == str(Saite).strip().lower():
                if str(el.Brand_car).strip().lower() == str(Brand).strip().lower():

                    link = el.Links
                    link = str(link)+f'?price_to={Price_stop}&price_from={Price_start}&rodzaj-paliwa={Petrol}&bmatch=cl-dict201214-ctx-aut-1-1-0112&rok-produkcji-od={Years_start}&rok-produkcji-do={Years_stop}'

        if Users.get(Users.USERID==USERID).Model != "":

            for el in Auto.select():
                if str(el.Saite).strip().lower() == str(Saite).strip().lower():
                    if str(el.Brand_car).strip().lower() == str(Brand).strip().lower():
                        if str(el.Model).strip().lower() == str(Users.get(Users.USERID==USERID).Model).strip().lower():

                            link = el.Link_model
                            link = str(link)+f'?price_to={Price_stop}&price_from={Price_start}&rodzaj-paliwa={Petrol}&bmatch=cl-dict201214-ctx-aut-1-1-0112&rok-produkcji-od={Years_start}&rok-produkcji-do={Years_stop}'
    else:
        link = f'https://allegro.pl/kategoria/samochody-osobowe-4029?price_to={Price_stop}&price_from={Price_start}&rodzaj-paliwa={Petrol}&bmatch=cl-dict201214-ctx-aut-1-1-0112&rok-produkcji-od={Years_start}&rok-produkcji-do={Years_stop}'

    chrome_options = Options()  
    chrome_options.add_argument("--disable-javascript")
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=chrome_options)
    driver.get(link)
    time.sleep(4)

    paggination = driver.find_elements_by_xpath('//div[@role="navigation"]')
    if paggination:
        p = driver.find_element_by_xpath('//div[@role="navigation"]')
        a = p.find_elements_by_xpath('.//a')
        a = len(a) - 3


    if not driver.find_elements_by_xpath('//div[@class="opbox-listing"]'):
        if not Auto_result.row_exists(USERID):
            Auto_result.creat_row(USERID, '1', '2', '3')

        u = Auto_result.get(Auto_result.USERID==USERID)
        u.Status = 'Авто нет.'
        u.save()
        driver.quit()

    else:
        div = driver.find_elements_by_xpath('.//div[@class="opbox-listing"]')[1]
        ddd = div.get_attribute('outerHTML').split('Oferty</h2>')[0]
        ddd = len(ddd.split('article')) - 1

        #section = div.find_elements_by_xpath('.//section')[0]

        for el in div.find_elements_by_xpath('.//article[@data-role="offer"]')[:int(ddd)]:

            asd = el.find_element_by_xpath('.//dl[@class="mp4t_0 m3h2_0 mryx_0 munh_0 mg9e_0 mvrt_0 mj7a_0 mh36_0 meqh_en msa3_z4 _1vx3o"]')


            Year_facts = asd.find_elements_by_xpath('.//dt[@class="mpof_uk mgmw_ag mp4t_0 m3h2_0 mryx_0 munh_0 mg9e_0 mvrt_0 mj7a_0 mh36_0 _9c44d_3hPFO"]')
            Km_longer = asd.find_elements_by_xpath('.//dd[@class="mpof_uk mp4t_0 m3h2_0 mryx_0 munh_0 mgmw_ia mg9e_0 mj7a_0 mh36_0 _9c44d_3n9Wf "]')

            sxs = []
            for iii in range(0, len(Year_facts)):
                row = str(Year_facts[iii].text)+' '+str(Km_longer[iii].text)
                sxs.append(row)

            Year_facts = '\n'.join(sxs)

            element = el.find_element_by_xpath(".//img")
            element.location_once_scrolled_into_view
            time.sleep(0.1)

            img = el.find_element_by_xpath('.//img').get_attribute('src')
            prices = el.find_element_by_xpath('.//span[@class="_1svub _lf05o"]')
            link_page = el.find_element_by_xpath('.//a[@rel="nofollow"]').get_attribute('href')

            if not Auto_result.row_exists(link_page):
                Auto_result.creat_row(USERID, link_page, img, prices.text, Year_facts)

    if not Auto_result.row_exists(USERID):
        Auto_result.creat_row(USERID, 'asd', 'asd', 'Авто нет.')
        u = Auto_result.get(Auto_result.USERID==USERID)
        u.Status = 'Авто нет.'
        u.save()
    else:
        el = Auto_result.select()
        for el in el:
            if el.USERID == USERID:
                el.Status = 'Stop'
                el.save()
                break

    driver.quit()



def otomoto_pars(USERID, Brand, Model, Years_start, Years_stop, Price_start,Price_stop, Petrol, KPP):
    Brand = Brand.replace(' ', '-').strip().lower()
    Model = Model.replace(' ', '-').strip().lower()
    Petrol = Petrol.strip().lower()

    link = f'https://www.otomoto.pl/osobowe/{Brand}/{Model}/od-{Years_start}/?search%5Bfilter_float_price%3Afrom%5D={Price_start}&search%5Bfilter_float_price%3Ato%5D={Price_stop}&search%5Bfilter_float_year%3Ato%5D={Years_stop}&search%5Bfilter_enum_fuel_type%5D%5B0%5D={Petrol}&search%5Border%5D=created_at%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D='
    

    headers = {'accept': '*/*',
               'user-agent': 'Mozilla/5.0(X11;Linux x86_64...)Geco/20100101 Firefox/60.0'}
    session = requests.session()
    request = session.get(link, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')

        if not soup.findAll('div', class_='offers list'):
            if not Auto_result.row_exists(USERID):
                Auto_result.creat_row(USERID, '1', '2', '3', '4')

            u = Auto_result.get(Auto_result.USERID==USERID)
            u.Status = 'Авто нет.'
            u.save()
            return

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

                Year_facts = f'Выпуск: {Year_facts}\nПробег: {Km_longer}'
                if not Auto_result.row_exists(link_page):
                    Auto_result.creat_row(USERID, link_page, IMG, prices, Year_facts)

    el = Auto_result.select()
    for el in el:
        if el.USERID == USERID:
            el.Status = 'Stop'
            el.save()
            break


def spam(message):
    text = message.text 

    if text == '/cancel':
        USERID = message.chat.id
        if Users.get(Users.USERID == USERID).Private == 'Admin':

            knb = types.InlineKeyboardMarkup(row_width=1)
            knb.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in['Рассылка по пользователям', 'Вкл/Выкл подписки', 'Добавить администратора', '🏠 Главное меню']])
            subs_activate = []
            subs_disable = []
            subs_test = []
            for el in Users.select():
                if el.Subcribe == 'Yes':
                    subs_activate.append(el.USERID)

                if el.Subcribe == 'No':
                    subs_disable.append(el.USERID)

                if el.Subcribe == 'Test':
                    subs_test.append(el.USERID)

            msg = f'🔐 Админ панель\n\n👥 Кол-во пользователей: { len(Users.select()) }\n✅ Активных подписок: { len(subs_activate) }\n❌ Не активных подписок: { len(subs_disable) }\n⚠️ Тестовых подписок: { len(subs_test) }'
            bot.send_message(USERID, msg ,reply_markup=knb, parse_mode="Html")



        else:
            bot.send_message(USERID, 'Вы не обладаете правами доступа...\n\nДля продолжения работы нажмите /start')

    else:

        for el in Users.select():
            bot.send_message(el.USERID, text)

        bot.send_message(message.chat.id, 'Сообщения отправлены!')


def autoscout24_pars(USERID, Brand, Model, Years_start, Years_stop, Price_start,Price_stop, Petrol, KPP):
    if KPP == 'manual':
        KPP = 'M'
    if KPP == 'automatic':
        KPP = 'A'

    if Petrol == 'petrol':
        Petrol = 'B'
    if Petrol == 'diesel':
        Petrol = 'D'

    Brand = Brand.replace(' ', '-').strip().lower()
    Model = Model.replace(' ', '-').strip().lower()

    link = f'https://www.autoscout24.ru/lst/{Brand}/{Model}?sort=standard&desc=0&gear={KPP}&fuel={Petrol}&ustate=N%2CU&size=20&page=1&priceto={Price_stop}&pricefrom={Price_start}&fregto={Years_stop}&fregfrom={Years_start}'
    headers = {'accept': '*/*',
               'user-agent': 'Mozilla/5.0(X11;Linux x86_64...)Geco/20100101 Firefox/60.0'}

    session = requests.session()
    request = session.get(link, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')

        if soup.findAll('div', class_='cl-list-element cl-list-element-gap'):
            main = soup.findAll('div', class_='cl-list-element cl-list-element-gap' )
            for el in main:
                price = el.find('span', class_='cldt-price sc-font-xl sc-font-bold').text.strip()

                Km_longer = el.find('ul', attrs={"data-item-name" : "vehicle-details"}).find('li', attrs={"data-type" : "mileage"}).text.strip()
                Date = el.find('ul', attrs={"data-item-name" : "vehicle-details"}).find('li', attrs={"data-type" : "first-registration"}).text.strip()
                Links = el.find('a', attrs={"data-item-name" : "detail-page-link"}).get('href').strip()
                Links = 'https://www.autoscout24.ru'+str(Links)
                price = price.split(',')[0]
                price = f'<b>{price}</b>'
                Year_facts = f'Выпуск: {Date}\nПробег: {Km_longer}'

                if not Auto_result.row_exists(Links):
                    Auto_result.creat_row(USERID, Links, Links, price, Year_facts)


        else:
            if not Auto_result.row_exists(USERID):
                Auto_result.creat_row(USERID, '1', '2', '3', '4')

            u = Auto_result.get(Auto_result.USERID==USERID)
            u.Status = 'Авто нет.'
            u.save()
            return

    el = Auto_result.select()
    for el in el:
        if el.USERID == USERID:
            el.Status = 'Stop'
            el.save()
            break


def autoplius_pars(USERID, Brand, Model, Years_start, Years_stop, Price_start,Price_stop, Petrol, KPP):
    Brand = Brand
    Model = Model
    Money_start = Price_start
    Money_stop = Price_stop
    year_start = Years_start
    year_stop = Years_stop
    petrol = Petrol.lower()
    transmission = KPP.lower()

    if Model != '':
        Make_id = Auto.get(Auto.Brand_car == Brand, Auto.Model == Model, Auto.Saite == 'autoplius').Links
        Models = Auto.get(Auto.Brand_car == Brand, Auto.Model == Model, Auto.Saite == 'autoplius').Link_model
    
    elif Brand == '':
        Make_id = ''
        Models = ''

    else:
        Make_id = Auto.get(Auto.Brand_car == Brand, Auto.Saite == 'autoplius').Links
        Models = ''

    if transmission == 'automatic':
        KPP = 38

    if transmission == 'manual':
        KPP = 37

    if petrol == 'diesel':
        Petrol = 32
    if petrol == 'petrol':
        Petrol = 30

    link = f'https://ru.m.autoplius.lt/objavlenija/b-u-avtomobili?slist=1353278043&category_id=2&make_date_from={Years_start}&make_date_to={Years_stop}&make_id%5B{Make_id}%5D={Models}&sell_price_from={Money_start}&sell_price_to={Money_stop}'

    if petrol != '':
        link = str(link)+f'&fuel_id[{Petrol}]={Petrol}'

    if transmission != '':
        link = str(link)+f'&gearbox_id={KPP}'

    
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
                    link_car = el.find('a').get('href')
                    if len(el.find('div', class_='param-list-row-block').findAll('div')[0].findAll('span')) == 2:
                        Date = el.find('div', class_='param-list-row-block').findAll('div')[0].findAll('span')[0].text.strip()
                        Longer = el.find('div', class_='param-list-row-block').findAll('div')[0].findAll('span')[1].text.strip()

                    else:
                        Date = el.find('div', class_='param-list-row-block').findAll('div')[0].findAll('span')[0].text.strip()
                        Longer = 'Не известно'

                    prices = f'<b>{price}</b>'
                    Year_facts = f'Выпуск: {Date}\nПробег: {Longer}'
                    if not Auto_result.row_exists(link_car):
                        Auto_result.creat_row(USERID, link_car, link_car, prices, Year_facts)
        else:
            if not Auto_result.row_exists(USERID):
                Auto_result.creat_row(USERID, '1', '2', '3', '4')

            u = Auto_result.get(Auto_result.USERID==USERID)
            u.Status = 'Авто нет.'
            u.save()
            return

    el = Auto_result.select()
    for el in el:
        if el.USERID == USERID:
            el.Status = 'Stop'
            el.save()
            break

def Olx_pars(USERID, Brand, Model, Years_start, Years_stop, Price_start,Price_stop, Petrol, KPP):

    marka = Brand.lower()
    model = Model.lower()
    price_start = Price_start
    price_stop = Price_stop
    year_start = Years_start
    year_stop = Years_stop
    petrol = Petrol.lower()
    transmission = KPP.lower()

    if ' ' in marka.strip():
        marka = marka.replace(' ', '-').strip()

    if ' ' in model.strip():
        model = model.replace(' ', '-').strip()


    link = f'https://www.olx.pl/motoryzacja/samochody/{marka}/{model}/?search%5Bfilter_float_price%3Afrom%5D={price_start}&search%5Bfilter_float_price%3Ato%5D={price_stop}&search%5Bfilter_float_year%3Afrom%5D={year_start}&search%5Bfilter_float_year%3Ato%5D={year_stop}&search%5Bfilter_enum_petrol%5D%5B0%5D={petrol}&search%5Bfilter_enum_transmission%5D%5B0%5D={transmission}'

    chrome_options = Options()  
    chrome_options.add_argument("--disable-javascript")
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=chrome_options)
    driver.get(link)
    time.sleep(4)

    #if not driver.find_elements_by_xpath('//div[@class="pager rel clr"]'):
    if not driver.find_elements_by_xpath('//table[@id="offers_table"]/tbody'):
        if not Auto_result.row_exists(USERID):
            Auto_result.creat_row(USERID, '1', '2', '3')

        u = Auto_result.get(Auto_result.USERID==USERID)
        u.Status = 'Авто нет.'
        u.save()
        driver.quit()
        return


    #table = driver.find_element_by_xpath('//table[@id="offers_table"]/tbody').find_elements_by_xpath('.//tr[@class="wrap"]')
    if len( driver.find_elements_by_xpath('//div[@class="rel listHandler "]/table') ) == 2:
        table = driver.find_elements_by_xpath('//div[@class="rel listHandler "]/table')[1]

    if len( driver.find_elements_by_xpath('//div[@class="rel listHandler "]/table') ) == 1:
        table = driver.find_elements_by_xpath('//div[@class="rel listHandler "]/table')[0]

    div = table.find_element_by_xpath('.//tbody').find_elements_by_xpath('.//tr[@class="wrap"]')

    for el in div:
        el.location_once_scrolled_into_view
        link_page = el.find_element_by_xpath('.//tbody')
        link_page = link_page.find_elements_by_xpath('.//tr')[0]

        prices = link_page.find_elements_by_xpath('.//td')[2]
        prices = prices.find_element_by_xpath('.//strong').text

        link_page = link_page.find_elements_by_xpath('.//td')[0]
        if link_page.find_elements_by_xpath('.//img'):
            img = link_page.find_element_by_xpath('.//img').get_attribute('src')
        else:
            img = 'https://howfix.net/wp-content/uploads/2018/02/sIaRmaFSMfrw8QJIBAa8mA-article.png'

        link_page = link_page.find_element_by_xpath('.//a').get_attribute('href')


        if not Auto_result.row_exists(link_page):
            Auto_result.creat_row(USERID, link_page, img, prices, '')

    if driver.find_elements_by_xpath('//div[@class="pager rel clr"]'):

        for el in [1, 2, 3, 4]:
            driver.get(link+str(f'&search%5Bpaidads_listing%5D=1&page={el}'))
            time.sleep(4)

            if len( driver.find_elements_by_xpath('//div[@class="rel listHandler "]/table') ) == 2:
                table = driver.find_elements_by_xpath('//div[@class="rel listHandler "]/table')[1]

            if len( driver.find_elements_by_xpath('//div[@class="rel listHandler "]/table') ) == 1:
                table = driver.find_elements_by_xpath('//div[@class="rel listHandler "]/table')[0]

            div = table.find_element_by_xpath('.//tbody').find_elements_by_xpath('.//tr[@class="wrap"]')

            for el in div:
                el.location_once_scrolled_into_view
                link_page = el.find_element_by_xpath('.//tbody')
                link_page = link_page.find_elements_by_xpath('.//tr')[0]

                prices = link_page.find_elements_by_xpath('.//td')[2]
                prices = prices.find_element_by_xpath('.//strong').text

                link_page = link_page.find_elements_by_xpath('.//td')[0]
                if link_page.find_elements_by_xpath('.//img'):
                    img = link_page.find_element_by_xpath('.//img').get_attribute('src')
                else:
                    img = 'https://howfix.net/wp-content/uploads/2018/02/sIaRmaFSMfrw8QJIBAa8mA-article.png'

                link_page = link_page.find_element_by_xpath('.//a').get_attribute('href')


                if not Auto_result.row_exists(link_page):
                    Auto_result.creat_row(USERID, link_page, img, prices, '')


    el = Auto_result.select()
    for el in el:
        if el.USERID == USERID:
            el.Status = 'Stop'
            el.save()
            break

    driver.quit()


def Check_sub():
    while True:
        for el in Users.select():
            time_stop = int(el.Time_subs) + 2592000

            if time_stop <= time.time() and el.Time_subs != 0:
                u = Users.get(Users.USERID == el.USERID)
                u.Subcribe = 'No'
                u.Time_subs = 0
                u.save()
                #bot.send_message(el.USERID, f'Ваша подписка закончилась!😔')

                
        time.sleep(600)


# def Qiwi_check():
#     date = ''
#     while True:
#         api = QApi(token=token_qiwi, phone=phone)
#         dic_ = api.payments

#         for i in dic_.get('data'):
#             comment_qiwi = (i.get('comment'))
#             account_qiwi = (i.get('account'))
#             amount_qiwi = int(i.get('sum').get('amount'))
#             date_qiwi = (i.get('date'))
#             try:
#                 if date_qiwi != date:
#                     for el in Users.select():
#                         if el.Private == 'Admin':
#                             bot.send_message(el.USERID, 'Поступил платеж! '+str(amount_qiwi)+f' RUB\nДата: {date_qiwi}')
#                 date = date_qiwi
#             except:
#                 pass

#         time.sleep(5)



if __name__ == '__main__':

    t = threading.Thread(target=Check_sub)
    t.start()

    # t = threading.Thread(target=Qiwi_check)
    # t.start()


    bot.polling(none_stop=True)