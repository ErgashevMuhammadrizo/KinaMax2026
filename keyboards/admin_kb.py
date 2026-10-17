from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def admin_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎬 Kino qo'shish"), KeyboardButton(text="📺 Serial qo'shish")],
            [KeyboardButton(text="❌ Kino o'chirish"), KeyboardButton(text="❌ Serial o'chirish")],
            [KeyboardButton(text="📢 Obuna sozlash"), KeyboardButton(text="📊 Statistika")],
            [KeyboardButton(text="📨 Habar yuborish")],
        ],
        resize_keyboard=True
    )


def cancel_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Bekor qilish")]],
        resize_keyboard=True
    )


def skip_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⏭ O'tkazib yuborish")],
            [KeyboardButton(text="❌ Bekor qilish")]
        ],
        resize_keyboard=True
    )


def subscriptions_manage_kb(subscriptions: list):
    buttons = []
    for sub in subscriptions:
        buttons.append([
            InlineKeyboardButton(
                text=f"🗑 {sub['channel_title'] or sub['channel_id']}",
                callback_data=f"del_sub_{sub['id']}"
            )
        ])
    buttons.append([InlineKeyboardButton(text="➕ Kanal qo'shish", callback_data="add_sub")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
