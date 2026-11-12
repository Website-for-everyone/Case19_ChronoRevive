import pytest
from aiogram import Router
from bot.handlers import router, PhotoAppraisalFSM, TrackOrderFSM, ORDERS_MOCK
from bot.keyboards import (
    get_main_keyboard,
    get_quick_track_kb,
    get_vintage_brands_kb
)

def test_router_registration():
    assert isinstance(router, Router)
    assert len(router.message.handlers) >= 5
    assert len(router.callback_query.handlers) >= 3

def test_keyboards_structure():
    main_kb = get_main_keyboard()
    assert len(main_kb.keyboard) >= 2
    button_texts = [btn.text for row in main_kb.keyboard for btn in row]
    assert "🔍 Оценка по фото" in button_texts
    assert "📦 Отследить заказ (CR-8492)" in button_texts

    track_kb = get_quick_track_kb()
    assert len(track_kb.inline_keyboard) == 3

    brands_kb = get_vintage_brands_kb()
    assert len(brands_kb.inline_keyboard) == 3

def test_fsm_states_definition():
    assert hasattr(PhotoAppraisalFSM, "watch_brand")
    assert hasattr(PhotoAppraisalFSM, "defect_photo_or_text")
    assert hasattr(PhotoAppraisalFSM, "client_name")
    assert hasattr(PhotoAppraisalFSM, "client_contact")

    assert hasattr(TrackOrderFSM, "order_id")

def test_orders_mock_integrity():
    assert "CR-8492" in ORDERS_MOCK
    assert "Speedmaster" in ORDERS_MOCK["CR-8492"]["watch"]
