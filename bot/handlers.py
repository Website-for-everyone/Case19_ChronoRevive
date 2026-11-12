from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.keyboards import (
    get_main_keyboard,
    get_quick_track_kb,
    get_vintage_brands_kb
)
from bot.config import TELEGRAM_OWNER_USERNAME

router = Router()

class PhotoAppraisalFSM(StatesGroup):
    watch_brand = State()
    defect_photo_or_text = State()
    client_name = State()
    client_contact = State()

class TrackOrderFSM(StatesGroup):
    order_id = State()

ORDERS_MOCK = {
    "CR-8492": {
        "watch": "Omega Speedmaster 1968 (Calibre 321)",
        "client": "Константин В.",
        "progress": "85%",
        "current_stage": "Юстировка точности хода на Witschi Chronoscope",
        "notes": "Амплитуда колебаний баланса доведена до 292°. Выкачка 0.1 мс. Финальная проверка изохронизма."
    },
    "CR-7120": {
        "watch": "Patek Philippe Calatrava 1956 (Cal. 12-600 AT)",
        "client": "Михаил Д.",
        "progress": "40%",
        "current_stage": "Ультразвуковая очистка камней и ручная полировка мостов",
        "notes": "Эмалевый циферблат очищен без повреждения надписи. Ведется подбор оси баланса."
    }
}

@router.message(Command("start"))
async def cmd_start(message: Message):
    text = (
        "🕰 **АТЕЛЬЕ РЕСТАВРАЦИИ ЧАСОВ CHRONOREVIVE**\n\n"
        "Мы возвращаем к жизни музейные швейцарские калибры 1940–1980 гг.\n\n"
        "⚡ Возможности сервиса:\n"
        "— Экспресс-оценка стоимости реставрации по фото механизма или циферблата\n"
        "— Проверка стадии выполнения текущего заказа по трек-номеру (CR-8492)\n"
        "— Просмотр отреставрированных калибров из нашего архива\n\n"
        "Выберите нужное действие ниже:"
    )
    await message.answer(text, reply_markup=get_main_keyboard(), parse_mode="Markdown")

# Photo Appraisal FSM
@router.message(F.text == "🔍 Оценка по фото")
async def start_appraisal(message: Message, state: FSMContext):
    await state.set_state(PhotoAppraisalFSM.watch_brand)
    await message.answer(
        "🔍 **ОЦЕНКА СТОИМОСТИ РЕСТАВРАЦИИ**\n\n"
        "Шаг 1 из 4: Выберите или напишите марку ваших часов:",
        reply_markup=get_vintage_brands_kb()
    )

@router.callback_query(F.data.startswith("brand_"), PhotoAppraisalFSM.watch_brand)
async def process_brand_choice(callback: CallbackQuery, state: FSMContext):
    brand = callback.data.replace("brand_", "")
    await state.update_data(watch_brand=brand)
    await state.set_state(PhotoAppraisalFSM.defect_photo_or_text)
    await callback.message.edit_text(
        f"Выбрана марка: **{brand}**\n\n"
        f"Шаг 2 из 4: Отправьте фотографию часов/механизма или подробно опишите повреждения (не идут, разбито стекло, коррозия, замена деталей):",
        parse_mode="Markdown"
    )
    await callback.answer()

@router.message(PhotoAppraisalFSM.defect_photo_or_text)
async def process_photo_or_text(message: Message, state: FSMContext):
    desc = message.caption or message.text or "Прикреплена фотография часов"
    await state.update_data(defect_description=desc)
    await state.set_state(PhotoAppraisalFSM.client_name)
    await message.answer("Шаг 3 из 4: Как к вам обращаться (Ваше имя)?")

@router.message(PhotoAppraisalFSM.client_name)
async def process_client_name(message: Message, state: FSMContext):
    await state.update_data(client_name=message.text)
    await state.set_state(PhotoAppraisalFSM.client_contact)
    await message.answer("Шаг 4 из 4: Укажите номер телефона или Telegram-юзернейм для связи:")

@router.message(PhotoAppraisalFSM.client_contact)
async def process_contact(message: Message, state: FSMContext):
    data = await state.get_data()
    contact = message.text
    await state.clear()

    brand = data.get("watch_brand", "Vintage Watch")
    est_range = "45 000 – 75 000 ₽" if brand in ["Patek", "Rolex"] else "25 000 – 48 000 ₽"

    summary = (
        "✅ **ПРЕДВАРИТЕЛЬНЫЙ ВЕРДИКТ МАСТЕРА СФОРМИРОВАН!**\n\n"
        f"🕰 Марка: **{brand}**\n"
        f"📋 Описание: _{data.get('defect_description')}_\n"
        f"💰 Ориентировочная смета: **{est_range}**\n"
        f"👤 Клиент: **{data.get('client_name')}** ({contact})\n\n"
        f"Главный часовщик ателье {TELEGRAM_OWNER_USERNAME} изучит детальные снимки и свяжется с вами для согласования отправки часов в мастерскую с курьерской страховкой Спецсвязи."
    )
    await message.answer(summary, reply_markup=get_main_keyboard(), parse_mode="Markdown")

# Order Tracking
@router.message(F.text == "📦 Отследить заказ (CR-8492)")
async def track_menu(message: Message):
    text = (
        "📦 **СИСТЕМА ТРЕКИНГА РЕСТАВРАЦИИ**\n\n"
        "Выберите заказ для мгновенной проверки статуса или отправьте команду `/track НОМЕР`:"
    )
    await message.answer(text, reply_markup=get_quick_track_kb(), parse_mode="Markdown")

@router.callback_query(F.data.startswith("track_"))
async def handle_track_callback(callback: CallbackQuery):
    order_id = callback.data.replace("track_", "")
    order = ORDERS_MOCK.get(order_id)
    if not order:
        await callback.answer("Заказ не найден", show_alert=True)
        return

    text = (
        f"🔍 **СТАТУС ЗАКАЗА: {order_id}**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🕰 Часы: **{order['watch']}**\n"
        f"👤 Владелец: {order['client']}\n"
        f"📊 Прогресс готовности: **{order['progress']}**\n"
        f"⚙ Текущий этап: **{order['current_stage']}**\n"
        f"📝 Комментарий мастера: _{order['notes']}_\n"
        f"━━━━━━━━━━━━━━━━━━"
    )
    await callback.message.edit_text(text, parse_mode="Markdown")
    await callback.answer()

@router.message(Command("track"))
async def cmd_track(message: Message):
    args = message.text.split()
    order_id = args[1].upper() if len(args) > 1 else "CR-8492"
    order = ORDERS_MOCK.get(order_id, {
        "watch": "Vintage Timepiece",
        "client": message.from_user.full_name,
        "progress": "50%",
        "current_stage": "Ультразвуковая мойка трибов и рубинов",
        "notes": "Детали в работе у мастера. Ориентировочный срок сборки — 5 дней."
    })
    text = (
        f"🔍 **СТАТУС ЗАКАЗА: {order_id}**\n\n"
        f"🕰 Экземпляр: **{order['watch']}**\n"
        f"⚙ Стадия: **{order['current_stage']}**\n"
        f"📊 Готовность: **{order['progress']}**\n"
        f"📝 Заметка: _{order['notes']}_"
    )
    await message.answer(text, parse_mode="Markdown")

@router.message(F.text == "🕰 Галерея калибров")
async def show_calibers(message: Message):
    text = (
        "🏛 **ШЕДЕВРЫ ИЗ НАШЕЙ РЕСТАВРАЦИОННОЙ МАСТЕРСКОЙ**\n\n"
        "1. **Omega Speedmaster 1968 (Cal. 321)** — колонное колесо, восстановлен оригинальный ступенчатый циферблат.\n"
        "2. **Patek Philippe Calatrava 1956 (Cal. 12-600 AT)** — золотой ротор 18K, горячая эмаль.\n"
        "3. **Rolex Submariner 1972 (Cal. 1520)** — тритиевый циферблат, герметичность восстановлена до 20 BAR."
    )
    await message.answer(text, parse_mode="Markdown")

@router.message(F.text == "ℹ Об ателье ChronoRevive")
async def show_about(message: Message):
    text = (
        "🏛 **CHRONOREVIVE HAUTE HORLOGERIE ATELIER**\n\n"
        "• Оборудование: Witschi Chronoscope, ультразвуковые ванны Elma, станки Schaublin.\n"
        "• Гарантия: 24 месяца на безупречный ход восстановленного механизма.\n"
        "• Доставка: Ценная бронированная доставка часов по всей России.\n"
        "• Главный мастер: @Idrisov_prod"
    )
    await message.answer(text, parse_mode="Markdown")

@router.callback_query(F.data == "back_to_menu")
async def handle_back_menu(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Главное меню:", reply_markup=get_main_keyboard())
    await callback.answer()
