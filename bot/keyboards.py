from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="🔍 Оценка по фото"), KeyboardButton(text="📦 Отследить заказ (CR-8492)")],
        [KeyboardButton(text="🕰 Галерея калибров"), KeyboardButton(text="ℹ Об ателье ChronoRevive")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_quick_track_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="🔍 Отследить CR-8492 (Omega 1968)", callback_data="track_CR-8492")],
        [InlineKeyboardButton(text="🔍 Отследить CR-7120 (Patek 1956)", callback_data="track_CR-7120")],
        [InlineKeyboardButton(text="« Главное меню", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_vintage_brands_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Omega", callback_data="brand_Omega"),
            InlineKeyboardButton(text="Rolex", callback_data="brand_Rolex")
        ],
        [
            InlineKeyboardButton(text="Patek Philippe", callback_data="brand_Patek"),
            InlineKeyboardButton(text="Heuer / Breitling", callback_data="brand_Heuer")
        ],
        [InlineKeyboardButton(text="Другая марка", callback_data="brand_Other")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
