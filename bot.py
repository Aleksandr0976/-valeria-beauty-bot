import telebot
from telebot import types
import datetime
import json
import os

# ===== ТВОИ ДАННЫЕ =====
BOT_TOKEN = "8457889014:AAG7uc7SiDg7NOfGN_36BKa19LjSttb77Lo"
MASTER_ID = "5342367062"
TEST_CHAT = "@Aleksandr_Semeno"  # СЮДА БУДУТ ПРИХОДИТЬ ЗАЯВКИ (для теста)

bot = telebot.TeleBot(BOT_TOKEN)

# ===== НАСТРОЙКИ =====
SERVICES = [
    "💄 Макияж (1500₽)",
    "💇‍♀️ Прическа (2000₽)",
    "✨ Комплекс макияж+прическа (3000₽)",
    "🌙 Вечерний образ (2500₽)",
    "👰 Свадебный образ (5000₽)"
]

WORK_HOURS = ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]

# ===== ХРАНЕНИЕ ЗАПИСЕЙ (ВРЕМЕННОЕ) =====
temp_data = {}

# ===== МЕНЮ =====
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📅 Записаться", "✨ Услуги")
    markup.add("🗓️ Свободные дни", "📞 Контакты")
    return markup

def services_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for s in SERVICES:
        markup.add(s)
    markup.add("⬅️ Назад")
    return markup

# ===== СТАРТ =====
@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    if user_id == MASTER_ID:
        bot.send_message(message.chat.id, "👑 *Панель мастера*\nИспользуй /stats для статистики", parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, 
            "✨ *Добро пожаловать!*\nЯ бот мастера *Валерии* 💅\n\nВыберите действие:",
            parse_mode="Markdown", reply_markup=main_menu())

# ===== ОБРАБОТКА КНОПОК =====
@bot.message_handler(func=lambda m: True)
def handler(message):
    text = message.text

    if text == "📅 Записаться":
        msg = bot.send_message(message.chat.id, "Выберите услугу:", reply_markup=services_menu())
        bot.register_next_step_handler(msg, process_service)

    elif text == "✨ Услуги":
        show_services(message)

    elif text == "🗓️ Свободные дни":
        show_free_dates(message)

    elif text == "📞 Контакты":
        show_contacts(message)

    elif text == "⬅️ Назад":
        bot.send_message(message.chat.id, "Главное меню:", reply_markup=main_menu())

    elif text in SERVICES:
        process_service(message)

# ===== ШАГ 1: УСЛУГА =====
def process_service(message):
    user_id = message.from_user.id
    temp_data[user_id] = {"service": message.text}

    # Показываем даты
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    today = datetime.date.today()
    for i in range(1, 8):
        date = today + datetime.timedelta(days=i)
        if date.weekday() < 6:
            markup.add(date.strftime("%d.%m.%Y"))
    markup.add("⬅️ Назад")

    msg = bot.send_message(message.chat.id, "📅 *Выберите дату:*", parse_mode="Markdown", reply_markup=markup)
    bot.register_next_step_handler(msg, process_date)

# ===== ШАГ 2: ДАТА =====
def process_date(message):
    user_id = message.from_user.id
    if message.text == "⬅️ Назад":
        bot.send_message(message.chat.id, "Выберите услугу:", reply_markup=services_menu())
        return

    temp_data[user_id]["date"] = message.text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    for t in WORK_HOURS:
        markup.add(t)
    markup.add("⬅️ Назад")

    msg = bot.send_message(message.chat.id, "⏰ *Выберите время:*", parse_mode="Markdown", reply_markup=markup)
    bot.register_next_step_handler(msg, process_time)

# ===== ШАГ 3: ВРЕМЯ =====
def process_time(message):
    user_id = message.from_user.id
    if message.text == "⬅️ Назад":
        # возврат к датам
        today = datetime.date.today()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        for i in range(1, 8):
            date = today + datetime.timedelta(days=i)
            if date.weekday() < 6:
                markup.add(date.strftime("%d.%m.%Y"))
        markup.add("⬅️ Назад")
        bot.send_message(message.chat.id, "Выберите дату:", reply_markup=markup)
        return

    temp_data[user_id]["time"] = message.text

    msg = bot.send_message(message.chat.id, "📝 *Введите ваше имя:*", parse_mode="Markdown", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, process_name)

# ===== ШАГ 4: ИМЯ =====
def process_name(message):
    user_id = message.from_user.id
    temp_data[user_id]["name"] = message.text

    msg = bot.send_message(message.chat.id, "📱 *Введите ваш номер телефона:*\n(например: 89991234567)", parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_phone)

# ===== ШАГ 5: ТЕЛЕФОН И ОТПРАВКА =====
def process_phone(message):
    user_id = message.from_user.id
    phone = message.text
    data = temp_data.get(user_id, {})

    if not data:
        bot.send_message(message.chat.id, "❌ Ошибка. Начните запись заново.", reply_markup=main_menu())
        return

    # ===== УВЕДОМЛЕНИЕ В ТЕЛЕГРАМ (на @Aleksandr_Semeno) =====
    notification = f"""
🆕 *НОВАЯ ЗАЯВКА НА ЗАПИСЬ!*

👤 *Имя:* {data['name']}
📞 *Телефон:* {phone}
💅 *Услуга:* {data['service']}
📅 *Дата:* {data['date']}
⏰ *Время:* {data['time']}

📎 *Отправитель:* @{message.from_user.username or 'нет username'}
🆔 *ID:* {user_id}
    """

    try:
        bot.send_message(TEST_CHAT, notification, parse_mode="Markdown")
        bot.send_message(MASTER_ID, notification, parse_mode="Markdown")
        print("✅ Уведомление отправлено мастеру и тестовому аккаунту")
    except Exception as e:
        print(f"❌ Ошибка отправки уведомления: {e}")

    # ===== ПОДТВЕРЖДЕНИЕ КЛИЕНТУ =====
    bot.send_message(
        message.chat.id,
        f"✅ *Заявка отправлена!*\n\n"
        f"Валерия свяжется с вами в ближайшее время для подтверждения записи.\n"
        f"Спасибо, что выбрали нас! 💕",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

    # ===== ОЧИСТКА ВРЕМЕННЫХ ДАННЫХ =====
    temp_data.pop(user_id, None)

# ===== УСЛУГИ =====
def show_services(message):
    text = "💅 *Наши услуги:*\n\n"
    for s in SERVICES:
        text += f"• {s}\n"
    text += "\n📍 *Адрес:* г. Елабуга, ул. Баки Урманче 5/1\n⏰ *Часы:* 10:00–19:00"
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=main_menu())

# ===== СВОБОДНЫЕ ДНИ =====
def show_free_dates(message):
    today = datetime.date.today()
    text = "🗓 *Свободные даты на ближайшие дни:*\n\n"
    for i in range(1, 8):
        date = today + datetime.timedelta(days=i)
        if date.weekday() < 6:
            text += f"📅 {date.strftime('%d.%m.%Y (%a)')}\n"
    text += "\n📞 Для записи нажмите «Записаться»"
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=main_menu())

# ===== КОНТАКТЫ =====
def show_contacts(message):
    text = (
        "📞 *Контакты Валерии:*\n\n"
        "👩‍🎨 *Мастер:* Валерия\n"
        "📱 *Телефон:* +7 939 362-57-60\n"
        "📍 *Адрес:* г. Елабуга, ул. Баки Урманче 5/1\n"
        "⏰ *Часы:* 10:00–19:00\n\n"
        "💬 *Telegram:* @Fooop5"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=main_menu())

# ===== СТАТИСТИКА ДЛЯ МАСТЕРА =====
@bot.message_handler(commands=['stats'])
def stats(message):
    if str(message.from_user.id) != MASTER_ID:
        return
    bot.send_message(message.chat.id, f"📊 *Всего заявок в сессии:* {len(temp_data)}", parse_mode="Markdown")

# ===== ЗАПУСК =====
if __name__ == "__main__":
    print("🤖 БОТ ЗАПУЩЕН")
    print("📨 Уведомления будут приходить на @Aleksandr_Semeno и мастеру")
    bot.polling(none_stop=True)