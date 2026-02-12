import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode
import logging
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# ==== КОНСТАНТЫ ====
INSTAGRAM_VALERIA = "valeria.beauty"      # Instagram Валерии (портфолио)
TELEGRAM_MASTER = "Aleksandr_Semeno"      # Твой Telegram (запись к тебе)

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

def booking_keyboard():
    """Запись в Telegram к Александру"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📩 Записаться в Telegram", 
                              url=f"https://t.me/{TELEGRAM_MASTER}")],
        [InlineKeyboardButton(text="« Назад", callback_data="main")]
    ])

# ==== ХЕНДЛЕРЫ ====
@dp.message(Command("start"))
async def cmd_start(message: Message):
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
async def main_menu_callback(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "✨ <b>Valeria Beauty</b> — студия красоты\n\nВыберите услугу:",
        reply_markup=main_menu()
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "services")
async def show_services(callback: types.CallbackQuery):
    text = (
        "💄 <b>Прайс-лист</b>\n\n"
        "🔹 <b>Комплекс «Полный образ»</b> — 5000 ₽\n"
        "   • Макияж + прическа + образ целиком\n\n"
        "🔹 <b>Макияж дневной/вечерний</b> — 2500 ₽\n"
        "🔹 <b>Прическа</b> (укладка/свадебная/вечерняя) — 2500 ₽\n\n"
        "💅 Также принимаю заказы на:\n"
        "   • оформление бровей\n"
        "   • макияж для фотосессий\n\n"
        "📍 <i>Цены фиксированы, расходные материалы включены</i>"
    )
    await callback.message.edit_text(text, reply_markup=back_button())
    await callback.answer()

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
        "<i>Цены в портфолио не указаны — актуальный прайс в разделе «Услуги»</i>"
    )
    await callback.message.edit_text(
        text, 
        reply_markup=portfolio_keyboard(), 
        disable_web_page_preview=True
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "book")
async def book_appointment(callback: types.CallbackQuery):
    """Запись идёт на Александра (для отладки и работы)"""
    text = (
        "✍️ <b>Запись</b>\n\n"
        "Напишите мастеру в Telegram:\n\n"
        f"📩 @{TELEGRAM_MASTER}\n\n"
        "В сообщении укажите:\n"
        "• услугу\n"
        "• желаемую дату и время\n"
        "• ваше имя\n\n"
        "Я отвечу в ближайшее время ✅"
    )
    await callback.message.edit_text(
        text, 
        reply_markup=booking_keyboard()
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "contacts")
async def show_contacts(callback: types.CallbackQuery):
    """Контакты: адрес, вход со двора, Telegram мастера, Instagram Валерии"""
    text = (
        "📍 <b>Контакты</b>\n\n"
        "📍 Адрес: ул. Пушкина, д. 10 (центр)\n"
        "🚪 Вход: <b>со двора</b>\n"
        "⏰ Часы работы: 10:00 – 20:00 (пн–сб)\n"
        "📞 Телефон: +7 (999) 123-45-67\n\n"
        f"📩 Telegram (запись): @{TELEGRAM_MASTER}\n"
        f"📸 Instagram (портфолио): instagram.com/{INSTAGRAM_VALERIA}\n\n"
        "🚗 Есть парковка"
    )
    await callback.message.edit_text(text, reply_markup=back_button())
    await callback.answer()

# ==== ЗАПУСК ====
async def main():
    logger.info("✅ Бот запущен!")
    logger.info(f"📸 Instagram Валерии: @{INSTAGRAM_VALERIA}")
    logger.info(f"📩 Запись к мастеру: @{TELEGRAM_MASTER}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())