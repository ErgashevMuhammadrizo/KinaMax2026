from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def main_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎬 Kino ID")],
        ],
        resize_keyboard=True
    )


def seasons_kb(seasons: list, serial_id: int):
    buttons = []
    for season in seasons:
        title = season['title'] or f"Fasl {season['season_number']}"
        buttons.append([InlineKeyboardButton(
            text=f"📁 {title}",
            callback_data=f"season_{season['id']}"
        )])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def episodes_kb(episodes: list, season_id: int):
    buttons = []
    for ep in episodes:
        title = ep['title'] or f"Qism {ep['episode_number']}"
        buttons.append([InlineKeyboardButton(
            text=f"🎞 {ep['episode_number']}. {title}",
            callback_data=f"episode_{ep['id']}"
        )])
    buttons.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"back_season_{season_id}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def episode_watch_kb(episode_id: int, season_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎥 Ko'rish", callback_data=f"watch_ep_{episode_id}")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"season_{season_id}")]
    ])
