from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup

from keyboards.user_kb import main_menu_kb
from database.db import (
    get_movie_by_code, get_movie_by_id, update_movie_views,
    add_or_update_user
)
from services.subscription import check_subscriptions, build_subscription_keyboard

router = Router()


class UserStates(StatesGroup):
    waiting_code = State()


# ==================== HELPERS ====================

async def send_movie_info(target, bot: Bot, movie, user_id: int):
    """Kino ma'lumotlarini yuboradi"""
    caption = (
        f"🎬 <b>{movie['title']}</b>\n"
        f"📅 Yil: {movie['year'] or '—'}\n"
        f"🎭 Janr: {movie['genre'] or '—'}\n"
        f"🕒 Davomiyligi: {movie['duration'] or '—'}\n"
        f"👁 Ko'rishlar: {movie['views']}\n"
        f"🔑 ID: <code>{movie['code']}</code>"
    )

    rows = []
    if movie["video_file_id"] or movie["video_url"]:
        rows.append([InlineKeyboardButton(text="▶️ Ko'rish", callback_data=f"watch_{movie['id']}")])
    kb = InlineKeyboardMarkup(inline_keyboard=rows)

    if isinstance(target, Message):
        if movie["poster_file_id"]:
            await target.answer_photo(photo=movie["poster_file_id"], caption=caption, parse_mode="HTML", reply_markup=kb)
        else:
            await target.answer(caption, parse_mode="HTML", reply_markup=kb)
    else:  # CallbackQuery
        if movie["poster_file_id"]:
            await target.message.answer_photo(photo=movie["poster_file_id"], caption=caption, parse_mode="HTML", reply_markup=kb)
        else:
            await target.message.answer(caption, parse_mode="HTML", reply_markup=kb)


# ==================== START ====================

@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot):
    # Foydalanuvchini bazaga saqlash
    await add_or_update_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    args = message.text.split()
    param = args[1] if len(args) > 1 else None

    # Deep link orqali kelgan: /start movie_0001
    if param and param.startswith("movie_"):
        code = param.replace("movie_", "")
        movie = await get_movie_by_code(code)
        if movie:
            ok, not_subscribed = await check_subscriptions(bot, message.from_user.id)
            if not ok:
                kb = build_subscription_keyboard(not_subscribed, "check_sub")
                await message.answer("⚠️ Ko'rish uchun avval kanallarga obuna bo'ling:", reply_markup=kb)
                return
            await update_movie_views(movie["id"])
            await send_movie_info(message, bot, movie, message.from_user.id)
            return
        await message.answer("❌ Kino topilmadi.")
        return

    # Professional salomlashuv xabari
    name = message.from_user.first_name or "Do'stim"
    welcome_text = (
        f"🎬 <b>KINAMAX</b> ga xush kelibsiz, <b>{name}</b>!\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🍿 <b>Nima ko'rmoqchisiz?</b>\n\n"
        f"🎥 <b>Kino</b> — ID raqamini yuboring\n"
        f"   <i>Misol: <code>0001</code></i>\n\n"
        f"🔍 <b>Qanday ishlaydi?</b>\n"
        f"   Kanal postida ko'rgan ID raqamini\n"
        f"   shu yerga yuboring — film tayyor! 🚀\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"✨ <i>Kinolardan bahramand bo'ling!</i>"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ℹ️ Qo'llanma", callback_data="help_info")],
    ])

    await message.answer(welcome_text, parse_mode="HTML", reply_markup=kb)


# ==================== INLINE START BUTTONS ====================

@router.callback_query(F.data == "help_info")
async def help_info_cb(cb: CallbackQuery):
    text = (
        "📖 <b>Bot qo'llanmasi</b>\n\n"
        "1️⃣ Kanalimizda kino e'lonini toping\n"
        "2️⃣ E'londa ko'rsatilgan <b>ID</b> raqamini nusxalang\n"
        "3️⃣ Shu ID ni botga yuboring\n"
        "4️⃣ Film avtomatik yuboriladi! 🎉"
    )
    await cb.message.answer(text, parse_mode="HTML")
    await cb.answer()


# ==================== CODE SEARCH ====================

@router.message(F.text.regexp(r'^\d{1,4}$'))
async def search_by_code(message: Message, bot: Bot):
    """Foydalanuvchi raqam yuborganda qidiradi"""
    code = message.text.strip().zfill(4)

    ok, not_subscribed = await check_subscriptions(bot, message.from_user.id)
    if not ok:
        kb = build_subscription_keyboard(not_subscribed)
        await message.answer("⚠️ Ko'rish uchun avval kanallarga obuna bo'ling:", reply_markup=kb)
        return

    movie = await get_movie_by_code(code)
    if movie:
        await update_movie_views(movie["id"])
        await send_movie_info(message, bot, movie, message.from_user.id)
        return

    await message.answer(f"❌ <code>{code}</code> ID li kino topilmadi.", parse_mode="HTML")


# ==================== WATCH ====================

@router.callback_query(F.data.startswith("watch_"))
async def watch_movie(cb: CallbackQuery, bot: Bot):
    movie_id = int(cb.data.split("_")[1])
    movie = await get_movie_by_id(movie_id)
    if not movie:
        await cb.answer("Kino topilmadi", show_alert=True)
        return

    await update_movie_views(movie_id)

    if movie["video_file_id"]:
        await cb.message.answer_video(
            video=movie["video_file_id"],
            caption=f"🎬 <b>{movie['title']}</b>\n\nTomosha qiling!",
            parse_mode="HTML"
        )
    elif movie["video_url"]:
        await cb.message.answer(
            f"🎬 <b>{movie['title']}</b>\n\n🎥 Ko'rish: {movie['video_url']}",
            parse_mode="HTML"
        )
    else:
        await cb.answer("Video hali qo'shilmagan", show_alert=True)


# ==================== SUBSCRIPTION CHECK ====================

@router.callback_query(F.data.startswith("check_sub"))
async def recheck_subscription(cb: CallbackQuery, bot: Bot):
    ok, not_subscribed = await check_subscriptions(bot, cb.from_user.id)
    if ok:
        await cb.answer("✅ Obuna tasdiqlandi! Endi foydalanishingiz mumkin.", show_alert=True)
        await cb.message.delete()
    else:
        await cb.answer("❌ Siz hali barcha kanallarga obuna bo'lmadingiz!", show_alert=True)
