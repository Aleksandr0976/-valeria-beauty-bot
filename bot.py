import telebot
from telebot import types
import datetime
import json
import os

BOT_TOKEN = "8457889014:AAG7uc7SiDg7NOfGN_36BKa19LjSttb77Lo"
MASTER_ID = "5342367062"

bot = telebot.TeleBot(BOT_TOKEN)

SERVICES = {
    'makeup': '💄 Макияж (1500₽)',
    'hairstyle': '💇‍♀️ Прическа (2000₽)',
    'both': '✨ Комплекс (3000₽)',
    'evening': '🌙 Вечерний образ (2500₽)'
}

WORK_HOURS = ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00']

bookings = {}

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('📅 Записаться', '✨ Услуги')
    markup.add('🗓️ Свободные дни', '📞 Контакты')
    return markup

@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = str(message.from_user.id)
    
    if user_id == MASTER_ID:
        bot.send_message(message.chat.id, "👑 Привет, Валерия! Панель мастера.", reply_markup=main_menu())
    else:
        bot.send_message(message.chat.id, "✨ Добро пожаловать! Я бот мастера Валерии 💅", reply_markup=main_menu())

@bot.message_handler(func=lambda m: True)
def handle_messages(message):
    text = message.text
    
    if text == '📅 Записаться':
        bot.send_message(message.chat.id, "📞 Для записи звоните: +7 939 362-57-60")
    elif text == '✨ Услуги':
        services = "💅 Услуги:\n• 💄 Макияж (1500₽)\n• 💇‍♀️ Прическа (2000₽)\n• ✨ Комплекс (3000₽)"
        bot.send_message(message.chat.id, services)
    elif text == '🗓️ Свободные дни':
        bot.send_message(message.chat.id, "🗓️ Пн-Сб: 10:00-19:00\n📞 +7 939 362-57-60")
    elif text == '📞 Контакты':
        contacts = "📞 Контакты:\n👩‍🎨 Валерия\n📱 +7 939 362-57-60\n📍 Елабуга, Баки Урманче 5/1"
        bot.send_message(message.chat.id, contacts)

if __name__ == '__main__':
    print("🤖 Бот запущен!")
    bot.polling(none_stop=True)