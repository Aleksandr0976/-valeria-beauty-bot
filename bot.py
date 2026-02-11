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

# ===== ПОРТФОЛИО =====
PORTFOLIO = [
    {"id": 1, "title": "💄 Дневной макияж", "desc": "Натуральный, свежий образ", "price": 2000},
    {"id": 2, "title": "🌙 Вечерний макияж", "desc": "Яркий, выразительный образ", "price": 3000},
    {"id": 3, "title": "👰 Свадебный макияж", "desc": "Нежный и стойкий образ", "price": 5000},
    {"id": 4, "title": "💇‍♀️ Вечерняя прическа", "desc": "Укладка, локоны, пучки", "price": 2000},
    {"id": 5, "title": "✨ Комплекс (макияж + прическа)", "desc": "Полный образ со скидкой", "price": 4000},
]

bot = telebot.TeleBot(BOT_TOKEN)

temp_data = {}
portfolio_index = 0

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
    user_id = str(message.from_user.id)
    welcome_text = (
        "✨ *Добро пожаловать в салон Валерии!* ✨\n\n"
        "💄 Визажист, свадебный и вечерний макияж\n"
        f"📍 {SALON_ADDRESS}\n\n"
        "Выберите действие:"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=main_menu())
    if user_id == MASTER_ID:
        bot.send_message(message.chat.id, "👑 *Панель мастера*\n/stats — статистика заявок", parse_mode="Markdown")

# ===== ОБРАБОТКА КНОПОК =====
@bot.message_handler(func=lambda m: True)
def handler(message):
    text = message.text
    if text == "📅 Записаться":
        msg = bot.send_message(message.chat.id, "💅 *Выберите услугу:*", parse_mode="Markdown", reply_markup=services_menu())
        bot.register_next_step_handler(msg, process_service)
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
    elif text in SERVICES.keys():
        process_service(message)

# ===== СВОБОДНЫЕ ДНИ — 7/0 (БЕЗ ВЫХОДНЫХ) =====
def show_free_dates(message):
    today = datetime.date.today()
    text = "🗓 *Свободные даты на ближайшие 7 дней:*\n\n"
    for i in range(1, 8):
        date = today + datetime.timedelta(days=i)
        text += f"📅 {date.strftime('%d.%m.%Y (%a)')}\n"
    text += "\n✅ Для записи нажмите «📅 Записаться»"
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=main_menu())

# ===== ОСТАЛЬНЫЕ ФУНКЦИИ (БЕЗ ИЗМЕНЕНИЙ) =====
def show_instagram(message):
    bot.send_message(message.chat.id, f"📸 *Наш Instagram:*\n{INSTAGRAM}", parse_mode="Markdown", reply_markup=main_menu())

def show_services(message):
    text = "💅 *Услуги и цены:*\n\n"
    for service, price in SERVICES.items():
        text += f"• {service} — {price}₽\n"
    text += f"\n📍 *Адрес:* {SALON_ADDRESS}\n⏰ *Часы:* 10:00–19:00"
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=main_menu())

def show_contacts(message):
    text = (
        "📞 *Контакты Валерии:*\n\n"
        f"👩‍🎨 *Мастер:* Валерия\n"
        f"📱 *Телефон:* {SALON_PHONE}\n"
        f"📍 *Адрес:* {SALON_ADDRESS}\n"
        "⏰ *Часы:* 10:00–19:00 (ежедневно)\n\n"
        f"📸 *Instagram:* {INSTAGRAM}\n"
        f"💬 *Telegram:* @Fooop5"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=main_menu())

# ===== ПОРТФОЛИО =====
def show_portfolio(message):
    global portfolio_index
    portfolio_index = 0
    send_portfolio_item(message, portfolio_index)

def send_portfolio_item(message, index):
    if index < 0 or index >= len(PORTFOLIO):
        bot.send_message(message.chat.id, "🖼️ Портфолио закончилось", reply_markup=main_menu())
        return
    item = PORTFOLIO[index]
    text = f"""
🖼️ *{item['title']}*

{item['desc']}

💵 *Стоимость:* {item['price']}₽

📸 Больше работ в Instagram: {INSTAGRAM}
    """
    markup = types.InlineKeyboardMarkup(row_width=2)
    if index > 0:
        markup.add(types.InlineKeyboardButton("⬅️ Назад", callback_data=f"portfolio_{index-1}"))
    if index < len(PORTFOLIO) - 1:
        markup.add(types.InlineKeyboardButton("➡️ Вперед", callback_data=f"portfolio_{index+1}"))
    markup.add(types.InlineKeyboardButton("📅 Записаться", callback_data=f"book_{item['id']}"))
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    global portfolio_index
    if call.data.startswith("portfolio_"):
        index = int(call.data.split("_")[1])
        portfolio_index = index
        bot.delete_message(call.message.chat.id, call.message.message_id)
        send_portfolio_item(call.message, index)
    elif call.data.startswith("book_"):
        item_id = int(call.data.split("_")[1])
        for item in PORTFOLIO:
            if item['id'] == item_id:
                bot.answer_callback_query(call.id, f"✅ Выбрано: {item['title']}")
                user_id = call.from_user.id
                temp_data[user_id] = {"service": item['title']}
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
                today = datetime.date.today()
                for i in range(1, 8):
                    date = today + datetime.timedelta(days=i)
                    markup.add(date.strftime("%d.%m.%Y"))
                markup.add("⬅️ Назад")
                bot.send_message(call.message.chat.id, f"💅 *Услуга:* {item['title']}\n\n📅 Выберите дату:", parse_mode="Markdown", reply_markup=markup)
                bot.register_next_step_handler(call.message, process_date, user_id)

# ===== ПРОЦЕСС ЗАПИСИ =====
def process_service(message):
    user_id = message.from_user.id
    temp_data[user_id] = {"service": message.text}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    today = datetime.date.today()
    for i in range(1, 8):
        date = today + datetime.timedelta(days=i)
        markup.add(date.strftime("%d.%m.%Y"))
    markup.add("⬅️ Назад")
    msg = bot.send_message(message.chat.id, "📅 *Выберите дату:*", parse_mode="Markdown", reply_markup=markup)
    bot.register_next_step_handler(msg, process_date, user_id)

def process_date(message, user_id):
    if message.text == "⬅️ Назад":
        bot.send_message(message.chat.id, "Выберите услугу:", reply_markup=services_menu())
        return
    temp_data[user_id]["date"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    for t in WORK_HOURS:
        markup.add(t)
    markup.add("⬅️ Назад")
    msg = bot.send_message(message.chat.id, "⏰ *Выберите время:*", parse_mode="Markdown", reply_markup=markup)
    bot.register_next_step_handler(msg, process_time, user_id)

def process_time(message, user_id):
    if message.text == "⬅️ Назад":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        today = datetime.date.today()
        for i in range(1, 8):
            date = today + datetime.timedelta(days=i)
            markup.add(date.strftime("%d.%m.%Y"))
        markup.add("⬅️ Назад")
        bot.send_message(message.chat.id, "Выберите дату:", reply_markup=markup)
        return
    temp_data[user_id]["time"] = message.text
    msg = bot.send_message(message.chat.id, "📝 *Введите ваше имя:*", parse_mode="Markdown", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, process_name, user_id)

def process_name(message, user_id):
    temp_data[user_id]["name"] = message.text
    msg = bot.send_message(message.chat.id, "📱 *Введите ваш номер телефона:*\n(например: 89991234567)", parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_phone, user_id)

def process_phone(message, user_id):
    phone = message.text
    data = temp_data.get(user_id, {})
    if not data:
        bot.send_message(message.chat.id, "❌ Ошибка. Начните заново.", reply_markup=main_menu())
        return
    notification = f"""
🆕 *НОВАЯ ЗАЯВКА!*

👤 *Имя:* {data['name']}
📞 *Телефон:* {phone}
💅 *Услуга:* {data['service']}
📅 *Дата:* {data['date']}
⏰ *Время:* {data['time']}

📎 *Username:* @{message.from_user.username or 'нет'}
🆔 *ID:* {user_id}
    """
    try:
        bot.send_message(TEST_CHAT, notification, parse_mode="Markdown")
        bot.send_message(MASTER_ID, notification, parse_mode="Markdown")
    except:
        pass
    bot.send_message(message.chat.id, "✅ *Заявка отправлена!*\n\nВалерия свяжется с вами для подтверждения. 💕", parse_mode="Markdown", reply_markup=main_menu())
    temp_data.pop(user_id, None)

# ===== СТАТИСТИКА =====
@bot.message_handler(commands=['stats'])
def stats(message):
    if str(message.from_user.id) != MASTER_ID:
        return
    bot.send_message(message.chat.id, f"📊 *Статистика:*\n\n👥 Активных сессий: {len(temp_data)}", parse_mode="Markdown")

# ===== ЗАПУСК =====
if __name__ == "__main__":
    print("🤖 БОТ ЗАПУЩЕН (7/0 — без выходных)")
    bot.polling(none_stop=True)