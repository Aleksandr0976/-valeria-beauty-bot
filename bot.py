import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from datetime import datetime, timedelta, time
import logging
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# ==== КОНСТАНТЫ ====
INSTAGRAM_VALERIA = "valeria.beauty"      # Instagram Валерии (портфолио)
TELEGRAM_MASTER = "Aleksandr_Semeno"      # Твой Telegram (запись к тебе)

# ==== ВРЕМЕННЫЕ НАСТРОЙКИ ====
START_HOUR = 7    # Начало работы 7:00
END_HOUR = 20     # Конец работы 20:00

# ==== СОСТОЯНИЯ ДЛЯ ЗАПИСИ ====
class BookingStates(StatesGroup):
    choosing_service = State()
    choosing_time = State()
    choosing_name = State()
    confirming = State()

# ==== КЛАВИАТУРЫ ====
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💇‍♀️ Услуги и цены", callback_data="services")],
        [InlineKeyboardButton(text="📸 Портфолио", callback_data="portfolio")],
        [InlineKeyboardButton(text="✍️ Записаться", callback_data="book")],
        [InlineKeyboardButton(text="📍 Контакты", callback_data="contacts")]
    ])

def back_button():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="« Назад", callback_data="main")]
    ])

def portfolio_keyboard():
    """Instagram Валерии — для просмотра работ"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Instagram Валерии", 
                              url=f"https://instagram.com/{INSTAGRAM_VALERIA}")],
        [InlineKeyboardButton(text="« Назад", callback_data="main")]
    ])

def service_keyboard():
    """Выбор услуги для записи"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💄 Полный образ (резерв 3ч)", callback_data="service_complex")],
        [InlineKeyboardButton(text="✨ Макияж (резерв 2ч)", callback_data="service_makeup")],
        [InlineKeyboardButton(text="💇‍♀️ Прическа (резерв 2ч)", callback_data="service_hair")],
        [InlineKeyboardButton(text="« Отмена", callback_data="main")]
    ])

def cancel_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="« Отмена", callback_data="main")]
    ])

# ==== ХЕНДЛЕРЫ ====
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    text = (
        "✨ <b>Valeria Beauty</b> — студия красоты в центре города\n\n"
        "Добро пожаловать! Здесь вы можете:\n"
        "• посмотреть услуги и цены\n"
        "• оценить портфолио Валерии\n"
        "• записаться к мастеру\n\n"
        "Выберите пункт ниже 👇"
    )
    await message.answer(text, reply_markup=main_menu())

@dp.callback_query(lambda c: c.data == "main")
async def main_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    """Возврат в главное меню и сброс состояния"""
    await state.clear()
    await callback.message.edit_text(
        "✨ <b>Valeria Beauty</b> — студия красоты\n\nВыберите услугу:",
        reply_markup=main_menu()
    )
    await callback.answer()

# ==== УСЛУГИ И ЦЕНЫ ====
@dp.callback_query(lambda c: c.data == "services")
async def show_services(callback: types.CallbackQuery):
    text = (
        "💄 <b>Прайс-лист</b>\n\n"
        "🔹 <b>Комплекс «Полный образ»</b> — 5000 ₽\n"
        "   • Макияж + прическа + образ целиком\n"
        "   • ⏳ Резерв времени: 3 часа\n\n"
        "🔹 <b>Макияж дневной/вечерний</b> — 2500 ₽\n"
        "   • ⏳ Резерв времени: 2 часа\n\n"
        "🔹 <b>Прическа</b> (укладка/свадебная/вечерняя) — 2500 ₽\n"
        "   • ⏳ Резерв времени: 2 часа\n\n"
        "💅 Также принимаю заказы на:\n"
        "   • оформление бровей\n"
        "   • макияж для фотосессий\n\n"
        "📍 <i>Цены фиксированы, расходные материалы включены</i>"
    )
    await callback.message.edit_text(text, reply_markup=back_button())
    await callback.answer()

# ==== ПОРТФОЛИО (ТОЛЬКО ССЫЛКА, БЕЗ ЦЕН) ====
@dp.callback_query(lambda c: c.data == "portfolio")
async def show_portfolio(callback: types.CallbackQuery):
    """Портфолио Валерии — только Instagram, без цен"""
    text = (
        "📸 <b>Портфолио Валерии</b>\n\n"
        "Все работы — в Instagram:\n"
        f"👉 instagram.com/{INSTAGRAM_VALERIA}\n\n"
        "Там вы найдёте:\n"
        "• макияж\n"
        "• причёски\n"
        "• полные образы\n\n"
        "<i>Цены в портфолио не указаны</i>"
    )
    await callback.message.edit_text(
        text, 
        reply_markup=portfolio_keyboard(), 
        disable_web_page_preview=True
    )
    await callback.answer()

# ==== КОНТАКТЫ ====
@dp.callback_query(lambda c: c.data == "contacts")
async def show_contacts(callback: types.CallbackQuery):
    text = (
        "📍 <b>Контакты</b>\n\n"
        "📍 Адрес: ул. Пушкина, д. 10 (центр)\n"
        "🚪 Вход: <b>со двора</b>\n"
        "⏰ Часы работы: 7:00 – 20:00 (пн–сб)\n"
        "📞 Телефон: +7 (999) 123-45-67\n\n"
        f"📩 Telegram (запись): @{TELEGRAM_MASTER}\n"
        f"📸 Instagram (портфолио): instagram.com/{INSTAGRAM_VALERIA}\n\n"
        "🚗 Есть парковка"
    )
    await callback.message.edit_text(text, reply_markup=back_button())
    await callback.answer()

# ==== НАЧАЛО ЗАПИСИ ====
@dp.callback_query(lambda c: c.data == "book")
async def start_booking(callback: types.CallbackQuery, state: FSMContext):
    """Шаг 1: Выбор услуги"""
    await state.set_state(BookingStates.choosing_service)
    await callback.message.edit_text(
        "✍️ <b>Запись</b>\n\n"
        "Выберите услугу:",
        reply_markup=service_keyboard()
    )
    await callback.answer()

# ==== ВЫБОР УСЛУГИ ====
@dp.callback_query(lambda c: c.data.startswith("service_"), StateFilter(BookingStates.choosing_service))
async def process_service(callback: types.CallbackQuery, state: FSMContext):
    """Запоминаем услугу и переходим к выбору времени"""
    
    # Определяем услугу и время резерва
    service_data = {
        "service_complex": {"name": "Полный образ", "price": 5000, "reserve": 3},
        "service_makeup": {"name": "Макияж", "price": 2500, "reserve": 2},
        "service_hair": {"name": "Прическа", "price": 2500, "reserve": 2}
    }
    
    service = service_data[callback.data]
    await state.update_data(
        service_name=service["name"],
        service_price=service["price"],
        reserve_hours=service["reserve"]
    )
    
    await state.set_state(BookingStates.choosing_time)
    
    # Показываем пример ввода времени
    now = datetime.now()
    example_time = now.replace(hour=10, minute=0, second=0, microsecond=0)
    if example_time < now:
        example_time += timedelta(days=1)
    
    await callback.message.edit_text(
        f"💄 <b>Услуга: {service['name']}</b>\n"
        f"⏳ Резерв времени: {service['reserve']} часа\n\n"
        f"🕐 <b>Ко скольки нужно быть готовой?</b>\n"
        f"(время от {START_HOUR}:00 до {END_HOUR}:00)\n\n"
        f"Напишите время в формате ЧЧ:ММ\n"
        f"Например: {example_time.strftime('%H:%M')}\n\n"
        f"❗️ Важно: я начну работу за {service['reserve']} часа до указанного времени",
        reply_markup=cancel_keyboard()
    )
    await callback.answer()

# ==== ВВОД ВРЕМЕНИ ====
@dp.message(StateFilter(BookingStates.choosing_time))
async def process_time(message: types.Message, state: FSMContext):
    """Парсим время и проверяем доступность"""
    
    try:
        # Парсим время из сообщения
        ready_time = datetime.strptime(message.text.strip(), "%H:%M").time()
        
        # Проверяем, что время в рабочем интервале
        if ready_time.hour < START_HOUR or ready_time.hour > END_HOUR:
            await message.answer(
                f"❌ Время должно быть с {START_HOUR}:00 до {END_HOUR}:00\n"
                "Попробуйте ещё раз:",
                reply_markup=cancel_keyboard()
            )
            return
        
        # Получаем данные об услуге
        user_data = await state.get_data()
        reserve_hours = user_data["reserve_hours"]
        
        # Рассчитываем время начала приёма
        ready_datetime = datetime.combine(datetime.now().date(), ready_time)
        start_datetime = ready_datetime - timedelta(hours=reserve_hours)
        start_time = start_datetime.time()
        
        # Проверяем, что начало приёма не раньше открытия
        if start_time.hour < START_HOUR:
            await message.answer(
                f"❌ Для этой услуги нужно начать в {start_time.strftime('%H:%M')}, "
                f"но мы работаем с {START_HOUR}:00\n"
                f"Выберите время готовности после {START_HOUR + reserve_hours}:00",
                reply_markup=cancel_keyboard()
            )
            return
        
        # Проверяем, что запись не в прошлом
        now = datetime.now()
        ready_full = datetime.combine(now.date(), ready_time)
        start_full = datetime.combine(now.date(), start_time)
        
        if start_full < now:
            # Если сегодня уже поздно, предлагаем завтра
            tomorrow = now + timedelta(days=1)
            ready_tomorrow = datetime.combine(tomorrow.date(), ready_time)
            start_tomorrow = datetime.combine(tomorrow.date(), start_time)
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="✅ Да, на завтра", 
                                    callback_data=f"confirm_time_{start_tomorrow.timestamp()}_{ready_tomorrow.timestamp()}")],
                [InlineKeyboardButton(text="« Выбрать другое время", callback_data="book")],
                [InlineKeyboardButton(text="« Отмена", callback_data="main")]
            ])
            
            await message.answer(
                f"⚠️ Сегодня уже поздно для записи на {ready_time.strftime('%H:%M')}\n\n"
                f"Перенести запись на завтра?\n"
                f"• Начало работы: {start_tomorrow.strftime('%H:%M')}\n"
                f"• Готовность: {ready_tomorrow.strftime('%H:%M')}",
                reply_markup=keyboard
            )
            return
        
        # Сохраняем время
        await state.update_data(
            start_time=start_time.strftime("%H:%M"),
            ready_time=ready_time.strftime("%H:%M"),
            booking_date=now.strftime("%d.%m.%Y")
        )
        
        await state.set_state(BookingStates.choosing_name)
        await message.answer(
            "✅ Время принято!\n\n"
            "📝 Напишите ваше имя:",
            reply_markup=cancel_keyboard()
        )
        
    except ValueError:
        await message.answer(
            "❌ Неправильный формат времени\n"
            "Напишите время в формате ЧЧ:ММ, например 14:30",
            reply_markup=cancel_keyboard()
        )

# ==== ПОДТВЕРЖДЕНИЕ ВРЕМЕНИ НА ЗАВТРА ====
@dp.callback_query(lambda c: c.data.startswith("confirm_time_"))
async def confirm_tomorrow_time(callback: types.CallbackQuery, state: FSMContext):
    """Подтверждение записи на завтра"""
    _, _, start_ts, ready_ts = callback.data.split("_")
    
    start_dt = datetime.fromtimestamp(float(start_ts))
    ready_dt = datetime.fromtimestamp(float(ready_ts))
    
    await state.update_data(
        start_time=start_dt.strftime("%H:%M"),
        ready_time=ready_dt.strftime("%H:%M"),
        booking_date=start_dt.strftime("%d.%m.%Y")
    )
    
    await state.set_state(BookingStates.choosing_name)
    await callback.message.edit_text(
        "✅ Запись перенесена на завтра!\n\n"
        f"📅 Дата: {start_dt.strftime('%d.%m.%Y')}\n"
        f"🕐 Начало: {start_dt.strftime('%H:%M')}\n"
        f"✨ Готовность: {ready_dt.strftime('%H:%M')}\n\n"
        "📝 Напишите ваше имя:",
        reply_markup=cancel_keyboard()
    )
    await callback.answer()

# ==== ВВОД ИМЕНИ ====
@dp.message(StateFilter(BookingStates.choosing_name))
async def process_name(message: types.Message, state: FSMContext):
    """Сохраняем имя и показываем подтверждение"""
    
    if len(message.text.strip()) < 2:
        await message.answer(
            "❌ Имя должно содержать хотя бы 2 символа\n"
            "Попробуйте ещё раз:",
            reply_markup=cancel_keyboard()
        )
        return
    
    await state.update_data(client_name=message.text.strip())
    user_data = await state.get_data()
    
    # Формируем итоговое сообщение
    confirm_text = (
        "✅ <b>Предварительная запись</b>\n\n"
        f"👤 Имя: {user_data['client_name']}\n"
        f"💄 Услуга: {user_data['service_name']}\n"
        f"💰 Стоимость: {user_data['service_price']} ₽\n"
        f"📅 Дата: {user_data['booking_date']}\n"
        f"🕐 Начало работы: {user_data['start_time']}\n"
        f"✨ Готовность: {user_data['ready_time']}\n"
        f"⏳ Резерв: {user_data['reserve_hours']} ч\n\n"
        "📩 <b>Для подтверждения напишите мне в Telegram:</b>\n"
        f"@{TELEGRAM_MASTER}"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📩 Написать мастеру", 
                              url=f"https://t.me/{TELEGRAM_MASTER}")],
        [InlineKeyboardButton(text="« В главное меню", callback_data="main")]
    ])
    
    await message.answer(confirm_text, reply_markup=keyboard)
    await state.clear()

# ==== ЗАПУСК ====
async def main():
    logger.info("✅ Бот запущен!")
    logger.info(f"📸 Instagram Валерии: @{INSTAGRAM_VALERIA}")
    logger.info(f"📩 Запись к мастеру: @{TELEGRAM_MASTER}")
    logger.info(f"⏰ Рабочее время: {START_HOUR}:00 - {END_HOUR}:00")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())