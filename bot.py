import telebot
from telebot import types
import datetime
import json
import os

# ===== ТВОИ ДАННЫЕ =====
BOT_TOKEN = "8457889014:AAG7uc7SiDg7NOfGN_36BKa19LjSttb77Lo"
MASTER_ID = "5342367062"
TEST_CHAT = "@Aleksandr_Semeno"

# ===== ДАННЫЕ САЛОНА =====
INSTAGRAM = "@valeriya_spiridonova__"
SALON_ADDRESS = "г. Елабуга, ул. Баки Урманче 5/1"
SALON_PHONE = "+7 939 362-57-60"
WORK_HOURS = ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]

# ===== УСЛУГИ И ЦЕНЫ =====
SERVICES = {
    "💄 Дневной макияж": 2000,
    "🌙 Вечерний макияж": 3000,
    "👰 Свадебный макияж": 5000,
    "💇‍♀️ Прическа": 2000,
    "✨ Комплекс (макияж + прическа)": 4000,
}

bot = telebot.TeleBot(BOT_TOKEN)

# ===== МЕНЮ =====
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📅 Записаться", "🖼️ Портфолио")
    markup.add("💅 Услуги и цены", "🗓️ Свободные дни")
    markup.add("📞 Контакты", "📸 Instagram")
    return markup

def services_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for service in SERVICES.keys():
        markup.add(service)
    markup.add("⬅️ Назад")
    return markup

# ===== СТАРТ =====
@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = (
        "✨ Добро пожаловать в салон Валерии! ✨\n\n"
        "💄 Визажист, свадебный и вечерний макияж\n"
        f"📍 {SALON_ADDRESS}\n\n"
        "Выберите действие:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu())

# ===== ИНСТАГРАМ (ИСПРАВЛЕНО) =====
def show_instagram(message):
    text = f"📸 Наш Instagram:\n{INSTAGRAM}\n\nПодписывайся, чтобы видеть свежие работы!"
    bot.send_message(message.chat.id, text, reply_markup=main_menu())

# ===== КОНТАКТЫ (ИСПРАВЛЕНО) =====
def show_contacts(message):
    text = (
        "📞 Контакты Валерии:\n\n"
        f"👩‍🎨 Мастер: Валерия\n"
        f"📱 Телефон: {SALON_PHONE}\n"
        f"📍 Адрес: {SALON_ADDRESS}\n"
        "⏰ Часы: 10:00–19:00 (ежедневно)\n\n"
        f"📸 Instagram: {INSTAGRAM}\n"
        f"💬 Telegram: @Fooop5"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu())

# ===== УСЛУГИ И ЦЕНЫ =====
def show_services(message):
    text = "💅 Услуги и цены:\n\n"
    for service, price in SERVICES.items():
        text += f"• {service} — {price}₽\n"
    text += f"\n📍 Адрес: {SALON_ADDRESS}\n⏰ Часы работы: 10:00–19:00"
    bot.send_message(message.chat.id, text, reply_markup=main_menu())

# ===== СВОБОДНЫЕ ДНИ =====
def show_free_dates(message):
    today = datetime.date.today()
    text = "🗓 Свободные даты на ближайшие 7 дней:\n\n"
    for i in range(1, 8):
        date = today + datetime.timedelta(days=i)
        text += f"📅 {date.strftime('%d.%m.%Y (%a)')}\n"
    text += "\n✅ Для записи нажмите «📅 Записаться»"
    bot.send_message(message.chat.id, text, reply_markup=main_menu())

# ===== ПОРТФОЛИО =====
def show_portfolio(message):
    text = (
        "🖼️ Портфолио Валерии:\n\n"
        "💄 Дневной макияж - 2000₽\n"
        "🌙 Вечерний макияж - 3000₽\n"
        "👰 Свадебный макияж - 5000₽\n"
        "💇‍♀️ Прическа - 2000₽\n"
        "✨ Комплекс - 4000₽\n\n"
        f"📸 Больше работ в Instagram: {INSTAGRAM}"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu())

# ===== ОБРАБОТЧИК КНОПОК =====
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    text = message.text

    if text == "📅 Записаться":
        bot.send_message(message.chat.id, "📞 Для записи звоните: +7 939 362-57-60\nИли пишите в Telegram: @Fooop5", reply_markup=main_menu())
    elif text == "🖼️ Портфолио":
        show_portfolio(message)
    elif text == "💅 Услуги и цены":
        show_services(message)
    elif text == "🗓️ Свободные дни":
        show_free_dates(message)
    elif text == "📞 Контакты":
        show_contacts(message)
    elif text == "📸 Instagram":
        show_instagram(message)
    elif text == "⬅️ Назад":
        bot.send_message(message.chat.id, "Главное меню:", reply_markup=main_menu())

# ===== ЗАПУСК =====
if __name__ == "__main__":
    print("=" * 50)
    print("🤖 БОТ ДЛЯ ВАЛЕРИИ ЗАПУЩЕН")
    print(f"📍 {SALON_ADDRESS}")
    print(f"📱 {SALON_PHONE}")
    print(f"📸 {INSTAGRAM}")
    print("=" * 50)
    
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("🔄 Перезапуск...")