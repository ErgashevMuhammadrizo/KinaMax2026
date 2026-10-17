import asyncio
import logging
import aiosqlite
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import ADMIN_IDS, MAIN_CHANNEL_ID, BASE_CHANNEL_ID
from keyboards.admin_kb import admin_menu_kb, cancel_kb, skip_kb, subscriptions_manage_kb
from database.db import (
    add_movie, get_movie_by_code, delete_movie,
    add_serial, get_serial_by_code, get_all_serials, get_seasons, add_season, add_episode,
    add_subscription, get_all_subscriptions, delete_subscription,
    get_movie_by_id, get_serial_by_id,
    get_all_users, get_users_count, block_user
)

router = Router()
logger = logging.getLogger(__name__)


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


def make_code(num: int) -> str:
    """4 xonali ID yasaydi: 1 -> 0001"""
    return str(num).zfill(4)


class AdminStates(StatesGroup):
    add_movie_title = State()
    add_movie_genre = State()
    add_movie_year = State()
    add_movie_duration = State()
    add_movie_poster = State()
    add_movie_video = State()
    add_serial_title = State()
    add_serial_genre = State()
    add_serial_year = State()
    add_serial_poster = State()
    add_season_serial_id = State()
    add_season_number = State()
    add_season_title = State()
    add_episode_serial_id = State()
    add_episode_season_id = State()
    add_episode_number = State()
    add_episode_title = State()
    add_episode_video = State()
    delete_movie_code = State()
    delete_serial_code = State()
    add_sub_channel = State()
    broadcast_message = State()
    broadcast_confirm = State()


# ==================== ADMIN PANEL ====================

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Sizda admin huquqi yo'q.")
        return
    users_count = await get_users_count()
    await message.answer(
        f"👑 <b>Admin Panel</b>\n\n"
        f"👥 Jami foydalanuvchilar: <b>{users_count}</b>",
        parse_mode="HTML",
        reply_markup=admin_menu_kb()
    )


@router.message(F.text == "❌ Bekor qilish")
async def cancel_action(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.clear()
    await message.answer("❌ Bekor qilindi.", reply_markup=admin_menu_kb())


# ==================== AUTO POST TO CHANNEL ====================

async def post_movie_to_channel(bot: Bot, movie_id: int, code: str):
    """Kino posterini asosiy kanalda yuboradi. Video allaqachon baza kanalda."""
    movie = await get_movie_by_id(movie_id)
    if not movie:
        return

    bot_info = await bot.get_me()
    bot_username = bot_info.username
    caption = (
        f"🎬 <b>{movie['title']}</b>\n"
        f"🎭 Janr: {movie['genre'] or '—'}\n"
        f"📅 Yil: {movie['year'] or '—'}\n"
        f"🕒 Davomiyligi: {movie['duration'] or '—'}\n\n"
        f"🔑 ID: <code>{code}</code>"
    )

    main_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="▶️ Ko'rish",
            url=f"https://t.me/{bot_username}?start=movie_{code}"
        )]
    ])

    try:
        if movie['poster_file_id']:
            await bot.send_photo(
                chat_id=MAIN_CHANNEL_ID,
                photo=movie['poster_file_id'],
                caption=caption,
                parse_mode='HTML',
                reply_markup=main_kb
            )
        else:
            await bot.send_message(
                chat_id=MAIN_CHANNEL_ID,
                text=caption,
                parse_mode='HTML',
                reply_markup=main_kb
            )
    except Exception as e:
        logger.error(f'Asosiy kanalda post xatosi: {e}')


async def post_serial_to_channel(bot: Bot, serial_id: int, code: str):
    """Serial kanalga post qiladi"""
    serial = await get_serial_by_id(serial_id)
    if not serial:
        return
    bot_info = await bot.get_me()
    bot_username = bot_info.username
    caption = (
        f"📺 <b>{serial['title']}</b>\n"
        f"🎭 Janr: {serial['genre'] or '—'}\n"
        f"📅 Yil: {serial['year'] or '—'}\n\n"
        f"🔑 ID: <code>{code}</code>"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="▶️ Ko'rish",
            url=f"https://t.me/{bot_username}?start=serial_{code}"
        )]
    ])
    try:
        if serial['poster_file_id']:
            await bot.send_photo(chat_id=BASE_CHANNEL_ID, photo=serial['poster_file_id'],
                                  caption=caption, parse_mode='HTML', reply_markup=kb)
        else:
            await bot.send_message(chat_id=BASE_CHANNEL_ID, text=caption,
                                    parse_mode='HTML', reply_markup=kb)
    except Exception as e:
        logger.error(f'Kanalga serial post xatosi: {e}')


# ==================== ADD MOVIE ====================

@router.message(F.text == "🎬 Kino qo'shish")
async def add_movie_start(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.set_state(AdminStates.add_movie_title)
    await message.answer("📝 <b>Kino nomini kiriting:</b>", parse_mode="HTML", reply_markup=cancel_kb())


@router.message(AdminStates.add_movie_title)
async def add_movie_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await state.set_state(AdminStates.add_movie_genre)
    await message.answer("🎭 <b>Janrini kiriting:</b>\n\nMisol: Drama, Komediya, Jangari", parse_mode="HTML", reply_markup=skip_kb())


@router.message(AdminStates.add_movie_genre)
async def add_movie_genre(message: Message, state: FSMContext):
    genre = None if message.text == "⏭ O'tkazib yuborish" else message.text.strip()
    await state.update_data(genre=genre)
    await state.set_state(AdminStates.add_movie_year)
    await message.answer("📅 <b>Yilini kiriting:</b>\n\nMisol: 2024", parse_mode="HTML", reply_markup=skip_kb())


@router.message(AdminStates.add_movie_year)
async def add_movie_year(message: Message, state: FSMContext):
    year = None if message.text == "⏭ O'tkazib yuborish" else message.text.strip()
    if year:
        try:
            year = int(year)
        except ValueError:
            await message.answer("❌ Yilni to'g'ri kiriting (raqam):")
            return
    await state.update_data(year=year)
    await state.set_state(AdminStates.add_movie_duration)
    await message.answer("🕒 <b>Davomiyligini kiriting:</b>\n\nMisol: 1:45", parse_mode="HTML", reply_markup=skip_kb())


@router.message(AdminStates.add_movie_duration)
async def add_movie_duration(message: Message, state: FSMContext):
    duration = None if message.text == "⏭ O'tkazib yuborish" else message.text.strip()
    await state.update_data(duration=duration)
    await state.set_state(AdminStates.add_movie_poster)
    await message.answer("🖼 <b>Poster rasmini yuboring:</b>", parse_mode="HTML", reply_markup=skip_kb())


@router.message(AdminStates.add_movie_poster)
async def add_movie_poster(message: Message, state: FSMContext):
    poster_file_id = None
    if message.text == "⏭ O'tkazib yuborish":
        pass
    elif message.photo:
        poster_file_id = message.photo[-1].file_id
    await state.update_data(poster_file_id=poster_file_id)
    await state.set_state(AdminStates.add_movie_video)
    await message.answer("🎬 <b>Video yuboring:</b>\n\n(Video fayl yuboring yoki URL kiriting)", parse_mode="HTML", reply_markup=skip_kb())


@router.message(AdminStates.add_movie_video)
async def add_movie_video(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    video_message_id = None
    video_url = None
    
    if message.text == "⏭ O'tkazib yuborish":
        pass
    elif message.video or message.document:
        # Video yoki document fayl kelgan - baza kanalga yuklash
        try:
            if message.video:
                sent_msg = await bot.send_video(
                    chat_id=BASE_CHANNEL_ID,
                    video=message.video.file_id,
                    caption=f"🎬 {data['title']}\n\n⚠️ Ushbu video baza kanalidagi xizmat videosi."
                )
            else:
                sent_msg = await bot.send_document(
                    chat_id=BASE_CHANNEL_ID,
                    document=message.document.file_id,
                    caption=f"🎬 {data['title']}\n\n⚠️ Ushbu video baza kanalidagi xizmat videosi."
                )
            video_message_id = sent_msg.message_id
        except Exception as e:
            logger.error(f'Baza kanalga video yuklashda xatolik: {e}')
            await message.answer(f"❌ Baza kanalga video yuklashda xatolik: {e}", reply_markup=admin_menu_kb())
            await state.clear()
            return
    elif message.text and (message.text.startswith('http://') or message.text.startswith('https://')):
        video_url = message.text.strip()

    movie_id = await add_movie(
        code='TEMP',
        title=data['title'],
        genre=data.get('genre'),
        year=data.get('year'),
        duration=data.get('duration'),
        poster_file_id=data.get('poster_file_id'),
        video_message_id=video_message_id,
        video_url=video_url
    )
    await state.clear()
    if movie_id:
        code = make_code(movie_id)
        async with aiosqlite.connect('database/kino_bot.db') as db:
            await db.execute('UPDATE movies SET code=? WHERE id=?', (code, movie_id))
            await db.commit()
        await message.answer(
            f"✅ <b>Kino qo'shildi!</b>\n\n"
            f"🔑 ID: <code>{code}</code>\n"
            f"🎬 Nomi: {data['title']}\n"
            f"💾 Video baza kanalga yuklandi!\n\n"
            f"📢 Kanal: kanalga post qilinmoqda...",
            parse_mode='HTML',
            reply_markup=admin_menu_kb()
        )
        await post_movie_to_channel(bot, movie_id, code)
        await message.answer(f"✅ Kanal postlandi! ID: <code>{code}</code>", parse_mode='HTML')
    else:
        await message.answer("❌ Xatolik yuz berdi. Qayta urinib ko'ring.", reply_markup=admin_menu_kb())


# ==================== DELETE MOVIE ====================

@router.message(F.text == "❌ Kino o'shish")
async def delete_movie_start(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.set_state(AdminStates.delete_movie_code)
    await message.answer("🔑 <b>O'chiriladigan kino ID sini kiriting:</b>\n\nMisol: <code>0001</code>", parse_mode='HTML', reply_markup=cancel_kb())


@router.message(AdminStates.delete_movie_code)
async def delete_movie_by_code(message: Message, state: FSMContext):
    code = message.text.strip().zfill(4)
    movie = await get_movie_by_code(code)
    if not movie:
        await message.answer(f"❌ <code>{code}</code> ID li kino topilmadi.", parse_mode='HTML')
        return
    await delete_movie(code)
    await state.clear()
    await message.answer(f"✅ <b>{movie['title']}</b> o'chirildi.", parse_mode='HTML', reply_markup=admin_menu_kb())


# ==================== ADD SERIAL ====================

@router.message(F.text == "📺 Serial qo'shish")
async def add_serial_menu(message: Message):
    if not is_admin(message.from_user.id):
        return
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📺 Yangi serial", callback_data="admin_add_new_serial")],
        [InlineKeyboardButton(text="📁 Mavjud serialga fasl qo'shish", callback_data="admin_add_season")],
        [InlineKeyboardButton(text="🎞 Mavjud faslga qism qo'shish", callback_data="admin_add_episode")],
    ])
    await message.answer("📺 Serial boshqaruvi:", reply_markup=kb)


@router.callback_query(F.data == "admin_add_new_serial")
async def start_add_serial(cb: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.add_serial_title)
    await cb.message.answer("📝 <b>Serial nomini kiriting:</b>", parse_mode='HTML', reply_markup=cancel_kb())


@router.message(AdminStates.add_serial_title)
async def serial_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await state.set_state(AdminStates.add_serial_genre)
    await message.answer("🎭 <b>Janrini kiriting:</b>", parse_mode='HTML', reply_markup=skip_kb())


@router.message(AdminStates.add_serial_genre)
async def serial_genre(message: Message, state: FSMContext):
    genre = None if message.text == "⏭ O'tkazib yuborish" else message.text.strip()
    await state.update_data(genre=genre)
    await state.set_state(AdminStates.add_serial_year)
    await message.answer("📅 <b>Yilini kiriting:</b>", parse_mode='HTML', reply_markup=skip_kb())


@router.message(AdminStates.add_serial_year)
async def serial_year(message: Message, state: FSMContext):
    year = None if message.text == "⏭ O'tkazib yuborish" else message.text.strip()
    if year:
        try:
            year = int(year)
        except ValueError:
            await message.answer("❌ Raqam kiriting:")
            return
    await state.update_data(year=year)
    await state.set_state(AdminStates.add_serial_poster)
    await message.answer("🖼 <b>Poster yuboring:</b>", parse_mode='HTML', reply_markup=skip_kb())


@router.message(AdminStates.add_serial_poster)
async def serial_poster(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    poster_file_id = None
    if message.photo:
        poster_file_id = message.photo[-1].file_id
    serial_id = await add_serial(
        code='TEMP', title=data['title'], genre=data.get('genre'),
        year=data.get('year'), poster_file_id=poster_file_id
    )
    await state.clear()
    if serial_id:
        code = make_code(serial_id)
        async with aiosqlite.connect('database/kino_bot.db') as db:
            await db.execute('UPDATE serials SET code=? WHERE id=?', (code, serial_id))
            await db.commit()
        await message.answer(
            f"✅ Serial qo'shildi!\n\n"
            f"🔑 ID: <code>{code}</code>\n"
            f"📺 Nomi: <b>{data['title']}</b>\n\n"
            f"📢 Kanalga post qilinmoqda...",
            parse_mode='HTML', reply_markup=admin_menu_kb()
        )
        await post_serial_to_channel(bot, serial_id, code)
        await message.answer(f"✅ Kanal postlandi! ID: <code>{code}</code>", parse_mode='HTML')
    else:
        await message.answer("❌ Xatolik yuz berdi.", reply_markup=admin_menu_kb())


# ==================== DELETE SERIAL ====================

@router.message(F.text == "❌ Serial o'shish")
async def delete_serial_start(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.set_state(AdminStates.delete_serial_code)
    await message.answer("🔑 <b>O'chiriladigan serial ID sini kiriting:</b>", parse_mode='HTML', reply_markup=cancel_kb())


@router.message(AdminStates.delete_serial_code)
async def delete_serial_by_code(message: Message, state: FSMContext):
    code = message.text.strip().zfill(4)
    serial = await get_serial_by_code(code)
    if not serial:
        await message.answer(f"❌ <code>{code}</code> ID li serial topilmadi.", parse_mode='HTML')
        return
    async with aiosqlite.connect('database/kino_bot.db') as db:
        await db.execute('DELETE FROM serials WHERE code=?', (code,))
        await db.commit()
    await state.clear()
    await message.answer(f"✅ <b>{serial['title']}</b> o'chirildi.", parse_mode='HTML', reply_markup=admin_menu_kb())


# ==================== ADD SEASON ====================

@router.callback_query(F.data == "admin_add_season")
async def start_add_season(cb: CallbackQuery, state: FSMContext):
    serials = await get_all_serials()
    if not serials:
        await cb.answer("Avval serial qo'shing", show_alert=True)
        return
    buttons = [[InlineKeyboardButton(text=f"{s['title']} (ID: {s['code']})", callback_data=f"sel_serial_season_{s['id']}")] for s in serials]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await cb.message.answer("📺 Serial tanlang:", reply_markup=kb)


@router.callback_query(F.data.startswith("sel_serial_season_"))
async def season_serial_selected(cb: CallbackQuery, state: FSMContext):
    serial_id = int(cb.data.split('_')[-1])
    await state.update_data(serial_id=serial_id)
    await state.set_state(AdminStates.add_season_number)
    await cb.message.answer("🔢 <b>Fasl raqamini kiriting:</b>", parse_mode='HTML', reply_markup=cancel_kb())


@router.message(AdminStates.add_season_number)
async def season_number(message: Message, state: FSMContext):
    try:
        num = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Raqam kiriting:")
        return
    await state.update_data(season_number=num)
    await state.set_state(AdminStates.add_season_title)
    await message.answer("📝 <b>Fasl nomi (ixtiyoriy):</b>", parse_mode='HTML', reply_markup=skip_kb())


@router.message(AdminStates.add_season_title)
async def season_title(message: Message, state: FSMContext):
    data = await state.get_data()
    title = None if message.text == "⏭ O'tkazib yuborish" else message.text.strip()
    season_id = await add_season(data['serial_id'], data['season_number'], title)
    await state.clear()
    await message.answer(f"✅ Fasl {data['season_number']} qo'shildi! Fasl ID: <code>{season_id}</code>",
                         parse_mode='HTML', reply_markup=admin_menu_kb())


# ==================== ADD EPISODE ====================

@router.callback_query(F.data == "admin_add_episode")
async def start_add_episode(cb: CallbackQuery, state: FSMContext):
    serials = await get_all_serials()
    if not serials:
        await cb.answer("Avval serial qo'shing", show_alert=True)
        return
    buttons = [[InlineKeyboardButton(text=f"{s['title']} (ID: {s['code']})", callback_data=f"sel_serial_ep_{s['id']}")] for s in serials]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await cb.message.answer("📺 Serial tanlang:", reply_markup=kb)


@router.callback_query(F.data.startswith("sel_serial_ep_"))
async def episode_serial_selected(cb: CallbackQuery, state: FSMContext):
    serial_id = int(cb.data.split('_')[-1])
    seasons = await get_seasons(serial_id)
    if not seasons:
        await cb.answer("Bu serialda fasl yo'q. Avval fasl qo'shing.", show_alert=True)
        return
    buttons = [[InlineKeyboardButton(
        text=s['title'] or f"Fasl {s['season_number']}",
        callback_data=f"sel_season_ep_{s['id']}"
    )] for s in seasons]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await cb.message.answer("📁 Fasl tanlang:", reply_markup=kb)


@router.callback_query(F.data.startswith("sel_season_ep_"))
async def episode_season_selected(cb: CallbackQuery, state: FSMContext):
    season_id = int(cb.data.split('_')[-1])
    await state.update_data(season_id=season_id)
    await state.set_state(AdminStates.add_episode_number)
    await cb.message.answer("🔢 <b>Qism raqamini kiriting:</b>", parse_mode='HTML', reply_markup=cancel_kb())


@router.message(AdminStates.add_episode_number)
async def episode_number(message: Message, state: FSMContext):
    try:
        num = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Raqam kiriting:")
        return
    await state.update_data(episode_number=num)
    await state.set_state(AdminStates.add_episode_title)
    await message.answer("📝 <b>Qism nomini kiriting:</b>", parse_mode='HTML', reply_markup=skip_kb())


@router.message(AdminStates.add_episode_title)
async def episode_title(message: Message, state: FSMContext):
    title = None if message.text == "⏭ O'tkazib yuborish" else message.text.strip()
    data = await state.get_data()
    await state.update_data(title=title or f"Qism {data['episode_number']}")
    await state.set_state(AdminStates.add_episode_video)
    await message.answer("🎬 <b>Video yuboring:</b>", parse_mode='HTML', reply_markup=skip_kb())


@router.message(AdminStates.add_episode_video)
async def episode_video(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    video_message_id = None
    video_url = None
    
    if message.text == "⏭ O'tkazib yuborish":
        pass
    elif message.video or message.document:
        # Video yoki document fayl kelgan - baza kanalga yuklash
        try:
            if message.video:
                sent_msg = await bot.send_video(
                    chat_id=BASE_CHANNEL_ID,
                    video=message.video.file_id,
                    caption=f"📺 {data['title']}\n\n⚠️ Ushbu video baza kanalidagi xizmat videosi."
                )
            else:
                sent_msg = await bot.send_document(
                    chat_id=BASE_CHANNEL_ID,
                    document=message.document.file_id,
                    caption=f"📺 {data['title']}\n\n⚠️ Ushbu video baza kanalidagi xizmat videosi."
                )
            video_message_id = sent_msg.message_id
        except Exception as e:
            logger.error(f'Baza kanalga video yuklashda xatolik: {e}')
            await message.answer(f"❌ Baza kanalga video yuklashda xatolik: {e}", reply_markup=admin_menu_kb())
            await state.clear()
            return
    elif message.text and message.text.startswith('http'):
        video_url = message.text.strip()
    
    await add_episode(data['season_id'], data['episode_number'], data['title'], video_message_id, video_url)
    await state.clear()
    await message.answer(
        f"✅ Qism {data['episode_number']} qo'shildi!\n"
        f"💾 Video baza kanalga yuklandi!",
        parse_mode='HTML', 
        reply_markup=admin_menu_kb()
    )


# ==================== SUBSCRIPTIONS ====================

@router.message(F.text == "📢 Obuna sozlash")
async def manage_subscriptions(message: Message):
    if not is_admin(message.from_user.id):
        return
    subs = await get_all_subscriptions()
    text = "📢 <b>Majburiy obuna kanallari:</b>" if subs else "📢 Hozircha kanallar yo'q."
    await message.answer(text, parse_mode='HTML', reply_markup=subscriptions_manage_kb(subs))


@router.callback_query(F.data == "add_sub")
async def add_sub_start(cb: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.add_sub_channel)
    await cb.message.answer(
        "📢 <b>Kanal ma'lumotlarini kiriting:</b>\n\n"
        "Format: <code>channel_id|Kanal nomi|@username</code>\n\n"
        "Misol: <code>-1001234567890|Kino Kanal|@kinokanaluz</code>",
        parse_mode='HTML', reply_markup=cancel_kb()
    )


@router.message(AdminStates.add_sub_channel)
async def add_sub_channel(message: Message, state: FSMContext):
    try:
        parts = message.text.strip().split('|')
        channel_id = parts[0].strip()
        channel_title = parts[1].strip() if len(parts) > 1 else 'Kanal'
        channel_username = parts[2].strip() if len(parts) > 2 else None
        await add_subscription(channel_id, channel_title, channel_username)
        await state.clear()
        await message.answer(f"✅ Kanal qo'shildi: <b>{channel_title}</b>",
                             parse_mode='HTML', reply_markup=admin_menu_kb())
    except Exception as e:
        await message.answer(f"❌ Xatolik: {e}\n\nQayta kiriting:")


@router.callback_query(F.data.startswith("del_sub_"))
async def delete_sub(cb: CallbackQuery):
    sub_id = int(cb.data.split('_')[-1])
    await delete_subscription(sub_id)
    await cb.answer("✅ Kanal o'chirildi")
    subs = await get_all_subscriptions()
    await cb.message.edit_reply_markup(reply_markup=subscriptions_manage_kb(subs))


# ==================== BROADCAST ====================

@router.message(F.text == "📨 Habar yuborish")
async def broadcast_start(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    users_count = await get_users_count()
    await state.set_state(AdminStates.broadcast_message)
    await message.answer(
        f"📨 <b>Barcha foydalanuvchilarga habar yuborish</b>\n\n"
        f"👥 Jami foydalanuvchilar: <b>{users_count}</b>\n\n"
        "Habarni yuboring (matn, rasm, video yoki hamma turi):\n\n"
        "<i>Habar aynan shu ko'rinishda yuboriladi</i>",
        parse_mode='HTML', reply_markup=cancel_kb()
    )


@router.message(AdminStates.broadcast_message)
async def broadcast_preview(message: Message, state: FSMContext):
    """Habarni preview ko'rsatish va tasdiqlash"""
    if message.text and message.text != "❌ Bekor qilish":
        await state.update_data(msg_type='text', text=message.text, entities=message.entities)
    elif message.photo:
        await state.update_data(msg_type='photo', file_id=message.photo[-1].file_id,
                               caption=message.caption, caption_entities=message.caption_entities)
    elif message.video:
        await state.update_data(msg_type='video', file_id=message.video.file_id,
                               caption=message.caption, caption_entities=message.caption_entities)
    elif message.document:
        await state.update_data(msg_type='document', file_id=message.document.file_id,
                               caption=message.caption, caption_entities=message.caption_entities)
    elif message.animation:
        await state.update_data(msg_type='animation', file_id=message.animation.file_id,
                               caption=message.caption, caption_entities=message.caption_entities)
    else:
        await message.answer("❌ Bu turdagi habarni yuborish mumkin emas. Qayta yuboring:")
        return

    users_count = await get_users_count()
    confirm_kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Tasdiqlash va yuborish", callback_data="broadcast_confirm_yes"),
        InlineKeyboardButton(text="❌ Bekor qilish", callback_data="broadcast_confirm_no"),
    ]])
    await state.set_state(AdminStates.broadcast_confirm)
    await message.answer(
        f"⚠️ <b>Tasdiqlang!</b>\n\n"
        f"👥 Jami <b>{users_count}</b> foydalanuvchiga yuboriladi.\n\n"
        "Yuqoridagi habar aynan shu ko'rinishda yuboriladi.\n"
        "Davom etasizmi?",
        parse_mode='HTML', reply_markup=confirm_kb
    )


@router.callback_query(F.data == "broadcast_confirm_no")
async def broadcast_cancel(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await cb.message.edit_text("❌ Habar yuborish bekor qilindi.")
    await cb.message.answer("👑 Admin panel:", reply_markup=admin_menu_kb())
    await cb.answer()


@router.callback_query(F.data == "broadcast_confirm_yes")
async def broadcast_send(cb: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await state.clear()
    users = await get_all_users()
    total = len(users)
    sent = 0
    failed = 0
    blocked = 0
    await cb.message.edit_text(
        f"📤 Yuborilmoqda...\n"
        f"👥 Jami: {total} ta foydalanuvchi"
    )
    await cb.answer()
    msg_type = data.get('msg_type', 'text')
    for user in users:
        try:
            uid = user['id']
            if msg_type == 'text':
                await bot.send_message(chat_id=uid, text=data['text'], entities=data.get('entities'))
            elif msg_type == 'photo':
                await bot.send_photo(chat_id=uid, photo=data['file_id'],
                                     caption=data.get('caption'), caption_entities=data.get('caption_entities'))
            elif msg_type == 'video':
                await bot.send_video(chat_id=uid, video=data['file_id'],
                                     caption=data.get('caption'), caption_entities=data.get('caption_entities'))
            elif msg_type == 'document':
                await bot.send_document(chat_id=uid, document=data['file_id'],
                                        caption=data.get('caption'), caption_entities=data.get('caption_entities'))
            elif msg_type == 'animation':
                await bot.send_animation(chat_id=uid, animation=data['file_id'],
                                         caption=data.get('caption'), caption_entities=data.get('caption_entities'))
            sent += 1
        except Exception as e:
            err_str = str(e).lower()
            if 'blocked' in err_str or 'deactivated' in err_str:
                blocked += 1
                await block_user(user['id'])
            else:
                failed += 1
        await asyncio.sleep(0.05)
    await cb.message.answer(
        f"✅ <b>Broadcast yakunlandi!</b>\n\n"
        f"📤 Jami yuborildi: <b>{sent}</b>\n"
        f"🚫 Bloklagan: <b>{blocked}</b>\n"
        f"❌ Xatolik: <b>{failed}</b>\n"
        f"📊 Jami: <b>{total}</b>",
        parse_mode='HTML', reply_markup=admin_menu_kb()
    )


# ==================== STATISTICS ====================

@router.message(F.text == "📊 Statistika")
async def statistics(message: Message):
    if not is_admin(message.from_user.id):
        return
    async with aiosqlite.connect('database/kino_bot.db') as db:
        async with db.execute('SELECT COUNT(*) FROM movies') as cur:
            total_movies = (await cur.fetchone())[0]
        async with db.execute('SELECT COUNT(*) FROM serials') as cur:
            total_serials = (await cur.fetchone())[0]
        async with db.execute('SELECT COUNT(*) FROM users') as cur:
            total_users = (await cur.fetchone())[0]
        async with db.execute('SELECT COUNT(*) FROM users WHERE is_blocked=1') as cur:
            blocked_users = (await cur.fetchone())[0]
        async with db.execute('SELECT title, views FROM movies ORDER BY views DESC LIMIT 1') as cur:
            top_movie = await cur.fetchone()
    top_text = f"{top_movie[0]} ({top_movie[1]} ko'rishlar)" if top_movie else '—'
    await message.answer(
        f"📊 <b>Statistika</b>\n\n"
        f"🎬 <b>Jami kinolar:</b> {total_movies}\n"
        f"📺 <b>Jami seriallar:</b> {total_serials}\n"
        f"👥 <b>Jami foydalanuvchilar:</b> {total_users}\n"
        f"🚫 <b>Bloklangan:</b> {blocked_users}\n\n"
        f"👑 <b>Eng ko'p ko'rilgan:</b> {top_text}",
        parse_mode='HTML'
    )
