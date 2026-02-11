t == "🗓️ Свободные дни":
        show_free_dates(message)
    elif text == "📞 Контакты":
        show_contacts(message)
    elif text == "📸 Instagram":
        show_instagram(message)
    elif text == "⬅️ Назад":
        bot.send_message(chat_id, "Главное меню:", reply_markup=main_menu())

    # Процесс записи
    elif chat_id in user_sessions:
        session = user_sessions[chat_id]
        # Выбор услуги
        if 'service' not in session:
            if text in SERVICES:
                select_date(message, text)
            else:
                bot.send_message(chat_id, "Пожалуйста, выберите услугу из списка.", reply_markup=services_menu())
        # Выбор даты
        elif 'date' not in session:
            try:
                # Проверяем, что введена дата в формате дд.мм.гггг
                datetime.datetime.strptime(text, "%d.%m.%Y")
                select_time(message, text)
            except:
                if text == "⬅️ Назад":
                    bot.send_message(chat_id, "Выберите услугу:", reply_markup=services_menu())
                    user_sessions[chat_id].pop('service', None)
                else:
                    bot.send_message(chat_id, "Пожалуйста, выберите дату из списка.", reply_markup=dates_menu())
        # Выбор времени
        elif 'time' not in session:
            date = session.get('date')
            busy_times = bookings.get(date, {})
            free_hours = [h for h in WORK_HOURS if h not in busy_times]
            if text in free_hours:
                confirm_booking(message, text)
            elif text == "⬅️ Назад":
                bot.send_message(chat_id, "Выберите дату:", reply_markup=dates_menu())
                user_sessions[chat_id].pop('date', None)
            else:
                bot.send_message(chat_id, "Пожалуйста, выберите свободное время из списка.", reply_markup=hours_menu())
        # Подтверждение
        else:
            if text == "✅ Подтвердить":
                finalize_booking(message)
            elif text == "❌ Отменить":
                bot.send_message(chat_id, "Запись отменена. Возврат в главное меню.", reply_markup=main_menu())
                user_sessions.pop(chat_id, None)
            else:
                bot.send_message(chat_id, "Пожалуйста, подтвердите или отмените запись.", reply_markup=confirm_menu())
    else:
        bot.send_message(chat_id, "Используйте кнопки меню.", reply_markup=main_menu())

if name == "main":
    print("Бот запущен...")
    bot.infinity_polling()