from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import get_all_subscriptions


async def check_subscriptions(bot: Bot, user_id: int):
    subs = await get_all_subscriptions()
    if not subs:
        return True, []

    not_subscribed = []
    for sub in subs:
        try:
            member = await bot.get_chat_member(sub["channel_id"], user_id)
            if member.status in ("left", "kicked", "banned"):
                not_subscribed.append(sub)
        except Exception:
            pass

    return len(not_subscribed) == 0, not_subscribed


def build_subscription_keyboard(not_subscribed: list, check_data: str = "check_sub"):
    buttons = []
    for sub in not_subscribed:
        text = sub["channel_title"] or "Kanal"
        url = f"https://t.me/{sub['channel_username'].lstrip('@')}" if sub["channel_username"] else None
        if url:
            buttons.append([InlineKeyboardButton(text=f"📢 {text}", url=url)])
    buttons.append([InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data=check_data)])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
