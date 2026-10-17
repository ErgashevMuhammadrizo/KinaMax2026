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
    """
    Majburiy obuna kanallarini ko'rsatadi.
    Agar kanal username bo'lsa: https://t.me/username
    Agar kanal ID bo'lsa: https://t.me/c/channel_id (private kanal)
    """
    buttons = []
    for sub in not_subscribed:
        text = sub["channel_title"] or "Kanal"
        
        # Agar username bo'lsa
        if sub["channel_username"]:
            username = sub["channel_username"].lstrip('@')
            url = f"https://t.me/{username}"
        # Agar faqat ID bo'lsa (private kanal)
        elif sub["channel_id"]:
            # -100 prefiksini olib tashlaymiz va kanal linkini yasaymiz
            channel_id_str = str(sub["channel_id"])
            if channel_id_str.startswith('-100'):
                clean_id = channel_id_str[4:]  # -100 ni olib tashlash
                url = f"https://t.me/c/{clean_id}/1"
            else:
                # Fallback - to'g'ridan-to'g'ri ID
                url = f"https://t.me/c/{channel_id_str.lstrip('-')}/1"
        else:
            # Agar hech narsa bo'lmasa, tugmani qo'shmaymiz
            continue
        
        buttons.append([InlineKeyboardButton(text=f"📢 {text}", url=url)])
    
    # Tekshirish tugmasi
    buttons.append([InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data=check_data)])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
