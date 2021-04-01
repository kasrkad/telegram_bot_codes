#!/bin/python3.9
import telebot
from telebot import  types
from parser import get_1c_codes
from log_pass import id_bot

1
bot = telebot.TeleBot(id_bot)

user = bot.get_me()
print (user)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "для получения кода 1с нажмите кнопку, и согласитесь поделиться контактом", reply_markup=start_keyboard())


@bot.message_handler(commands=['number']) #Объявили ветку для работы по команде <strong>number</strong>
def phone(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True) #Подключаем клавиатуру
    button_phone = types.KeyboardButton(text="Получить пароль от 1с", request_contact=True) #Указываем название кнопки, которая появится у пользователя
    keyboard.add(button_phone) #Добавляем эту кнопку
    bot.send_message(message.chat.id, 'Намите на кнопку получить пароль от 1с', reply_markup=keyboard) #Дублируем сообщением о том, что пользователь сейчас отправит боту свой номер телефона (на всякий случай, но это не обязательно)
 
@bot.message_handler(content_types=['contact']) #Объявили ветку, в которой прописываем логику на тот случай, если пользователь решит прислать номер телефона :) 
def contact(message):
    if message.contact is not None: #Если присланный объект <strong>contact</strong> не равен нулю
        phone = str(message.contact)
        contact_dict = {}
        phone = phone[1:len(phone)-1].split(sep=',')
        for i in phone:
            key, value = i.split(': ')
            contact_dict[key.replace('\'', '')]=value.replace('\'','').replace('+','')
        
        if len(contact_dict['phone_number']) == 11 and contact_dict['phone_number'].isdigit():
            try:
                bot.reply_to(message, 'проверяем списки СМС, может занять до 10 секунд')
                bot.reply_to(message, get_1c_codes(contact_dict['phone_number']))
            except KeyError as exc:
                print(contact_dict['phone_number'])
                bot.reply_to(message,f"Ошибка, СМС для номера {contact_dict['phone_number']} не найдена, попробуйте запросить еще один пароль в 1с")
        else:
            bot.reply_to(message,f"Проверьте правильность номера {contact_dict['phone_number']}")


def start_keyboard():
    keyboard2 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True) #Подключаем клавиатуру
    button_phone = types.KeyboardButton(text="Получить пароль от 1с", request_contact=True) #Указываем название кнопки, которая появится у пользователя
    keyboard2.add(button_phone) #Добавляем эту кнопку
 
    keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
    keyboard1.row('/number')
    return keyboard2

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()
