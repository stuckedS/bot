import pandas as pd
from telebot import types
import time
import telebot
import os
from background import keep_alive
import pip
import pymongo
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


myclient = pymongo.MongoClient(
    "mongodb+srv://davidkus152003:qwerty213@cluster0.l7ryhjk.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["aeroport"]

pip.main(['install', 'pytelegrambotapi'])
pip.main(['install', 'openpyxl'])
bot = telebot.TeleBot('6382740126:AAFIRgihWHDjRcQ5xjnVZoNvnHP2nPPK5GI')

id_flight=''
save = ''
cv_data = []
way = ''

@bot.message_handler(commands=['start'])
def menu(message):
    start_menu = types.ReplyKeyboardMarkup(True, True)
    start_menu.row('Билет')
    start_menu.row('Табло')
    start_menu.row('Карта аэропорта и его услуги')
    bot.send_message(message.chat.id,
                     'Добро пожаловать на глваное окно аэропорта выберите действие которое хотите выполнить',
                     reply_markup=start_menu)


@bot.message_handler(func=lambda message: message.text == 'Билет')
def bilet(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Регистрация на рейс',
                    'Отменить рейс')
    user_markup.row(
        'Места для регистрации негабаритного багажа')
    bot.send_message(
        message.chat.id, "Что вам нужно сделать?", reply_markup=user_markup)


@bot.message_handler(func=lambda message: message.text == 'Регистрация на рейс')
def registration(message):
    global way
    way = 'add'
    registration_menu = types.ReplyKeyboardMarkup(True, True)
    mycol = mydb["registration_on_flight"]
    for x in mycol.find():
        registration_menu.row(x['Рейс'])
    bot.register_next_step_handler(message, cv)
    bot.send_message(message.chat.id, "Выберите рейс",
                     reply_markup=registration_menu)


@bot.message_handler(func=lambda message: message.text == 'Отменить рейс')
def decline_flight(message):
    global way
    way = 'delete'
    registration_menu = types.ReplyKeyboardMarkup(True, True)
    mycol = mydb["registration_on_flight"]
    for x in mycol.find():
        registration_menu.row(x['Рейс'])
    bot.register_next_step_handler(message, cv)
    bot.send_message(message.chat.id, "Выберите рейс",
                     reply_markup=registration_menu)


@bot.message_handler(func=lambda message: message.text == 'Места для регистрации негабаритного багажа')
def map_luggage(message):
    bot.send_message(message.chat.id, "in progress")


@bot.message_handler(func=lambda message: message.text == 'Табло')
def fligths(message):
    flights_menu = types.ReplyKeyboardMarkup(True, True)
    flights_menu.row('Назад')
    mycol = mydb["Flights"]
    projection = {
        "_id": 0,
        "idAircraft": 0
    }
    tablo =''
    for x in mycol.find({}, projection):
        tablo = ' | '+'Номер рейса '+str(x['idFlights '])+' | '+'Дата '+str(x['Data '])+' | '+'Аэропорт вылета '+str(x['Airport_out '])+' | '+'Аэропорт прилета '+str(x['Airport_in '])+' | '+'Компания '+str(x['Company'])+' | '
        bot.send_message(message.chat.id, tablo,reply_markup=flights_menu)
    



@bot.message_handler(func=lambda message: message.text == 'Карта аэропорта и его услуги')
def map_service(message):
    map_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    map_markup.row('Карта', 'Услуги')
    bot.send_message(
        message.chat.id, "Что вам нужно сделать?", reply_markup=map_markup)


@bot.message_handler(func=lambda message: message.text == 'Карта')
def map(message):
    bot.send_photo(message.chat.id, photo=open('map.png', 'rb'))
    map_places = telebot.types.ReplyKeyboardMarkup(True, True)
    map_places.row('1 зона', '2 зона', '3 зона')
    map_places.row('Назад')
    bot.send_message(
        message.chat.id, "Аэропорт имеет 3 зоны. Выберите зону которая вам нужна.", reply_markup=map_places)


@bot.message_handler(func=lambda message: message.text == 'Услуги')
def service(message):
    service = telebot.types.ReplyKeyboardMarkup(True, True)
    mycol = mydb["Services"]
    
    for x in mycol.find({},{"Услуги":1,'_id':0}):
        service.row(str(x['Услуги'])) 
    bot.send_message(
        message.chat.id, "Выберите услугу", reply_markup=service)
    bot.register_next_step_handler(message, show_service)


@bot.message_handler(func=lambda message: message.text == '1 зона')
def service(message):
    flights_menu = types.ReplyKeyboardMarkup(True, True)
    flights_menu.row('Назад')
    mycol = mydb["Map"]
    for x in mycol.find({"Зона": '1'}):
        bot.send_message(message.chat.id, 'Основное : '+str(x['Основное']),reply_markup=flights_menu)
        bot.send_message(message.chat.id, 'Услуги : '+str(x['Услуги']),reply_markup=flights_menu)


@bot.message_handler(func=lambda message: message.text == '2 зона')
def service(message):
    flights_menu = types.ReplyKeyboardMarkup(True, True)
    flights_menu.row('Назад')
    mycol = mydb["Map"]
    for x in mycol.find({"Зона": '2'}): 
        bot.send_message(message.chat.id, 'Основное : '+str(x['Основное']),reply_markup=flights_menu)
        bot.send_message(message.chat.id, 'Услуги : '+str(x['Услуги']),reply_markup=flights_menu)


@bot.message_handler(func=lambda message: message.text == '3 зона')
def service(message):
    flights_menu = types.ReplyKeyboardMarkup(True, True)
    flights_menu.row('Назад')
    mycol = mydb["Map"]
    for x in mycol.find({"Зона": '3'}):
        bot.send_message(message.chat.id, 'Основное : '+str(x['Основное']),reply_markup=flights_menu)
        bot.send_message(message.chat.id, 'Услуги : '+str(x['Услуги']),reply_markup=flights_menu)


@bot.message_handler(content_types=['text'])
def handle_text(message):

    menu(message)

@bot.message_handler(func=lambda message: message.text == 'Назад')
def handle_text(message):
    menu(message)

def cv(message):
    global id_flight
    id_flight = message.text
    bot.send_message(message.chat.id, 'Введите свою Фамилию и Имя, и номер билета(через пробел)')
    bot.register_next_step_handler(message, save_cv)


def save_cv(message):
    global save
    save = message.text
    save = save.replace(' ','_')
    bot.reply_to(message, 'Я сохранил это сообщение: ' + save)
    registration_flight(message)


def registration_flight(message):
    global way
    mycol = mydb["registration_on_flight"]
    if (way == 'add'):
        _extracted_from_registration_flight_5(message, mycol, '$push')
    elif (way == 'delete'):
        _extracted_from_registration_flight_5(message, mycol, '$pull')
    else:
        bot.send_message(message.chat.id, '404')

    menu(message)


# TODO Rename this here and in `registration_flight`
def _extracted_from_registration_flight_5(message, mycol, arg2):
    bot.send_message(message.chat.id, id_flight)
    bot.send_message(message.chat.id, save)
    mycol.update_one({ 'Рейс': id_flight }, {arg2: { 'Пассажиры': save }})
    way =''
        

def show_service(message):
    mycol = mydb["Services"]
    flights_menu = types.ReplyKeyboardMarkup(True, True)
    flights_menu.row('Назад')
    for x in mycol.find({"Услуги": str(message.text)}):
        print(x)
        bot.send_message(message.chat.id, str(x['Описание']),reply_markup=flights_menu)


def tablo_krutoe(message):
    mycol = mydb["Services"]
    flights_menu = types.ReplyKeyboardMarkup(True, True)
    flights_menu.row('Назад')
    for x in mycol.find({"Услуги": str(message.text)}):
        print(x)
        bot.send_message(message.chat.id, str(x['Описание']),reply_markup=flights_menu)


# запускаем flask-сервер в отдельном потоке. Подробнее ниже...
keep_alive()
bot.polling(non_stop=True, interval=0)  # запуск бота
