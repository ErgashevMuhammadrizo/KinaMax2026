#!/usr/bin/env python3
"""
Bot test script - BASE_CHANNEL va funksiyalarni tekshirish
"""

import asyncio
from aiogram import Bot
from config import BOT_TOKEN, BASE_CHANNEL_ID, MAIN_CHANNEL_ID, ADMIN_IDS


async def test_bot():
    """Bot va kanallarni test qilish"""
    bot = Bot(token=BOT_TOKEN)
    
    print("=" * 60)
    print("🤖 KINAMAX BOT TEST")
    print("=" * 60)
    
    # 1. Bot ma'lumotlarini olish
    try:
        bot_info = await bot.get_me()
        print(f"\n✅ Bot ismi: @{bot_info.username}")
        print(f"✅ Bot ID: {bot_info.id}")
        print(f"✅ Bot nomi: {bot_info.first_name}")
    except Exception as e:
        print(f"\n❌ Bot ma'lumotlarini olishda xatolik: {e}")
        return
    
    # 2. Admin ID larni tekshirish
    print(f"\n📋 Admin ID lar: {ADMIN_IDS}")
    
    # 3. BASE_CHANNEL tekshirish
    print(f"\n📺 BASE_CHANNEL_ID: {BASE_CHANNEL_ID}")
    try:
        base_chat = await bot.get_chat(BASE_CHANNEL_ID)
        print(f"✅ BASE_CHANNEL topildi: {base_chat.title}")
        
        # Bot admin ekanligini tekshirish
        bot_member = await bot.get_chat_member(BASE_CHANNEL_ID, bot_info.id)
        if bot_member.status in ['administrator', 'creator']:
            print(f"✅ Bot BASE_CHANNEL da ADMIN")
        else:
            print(f"❌ Bot BASE_CHANNEL da ADMIN EMAS! Status: {bot_member.status}")
            print(f"⚠️  Botni kanalga admin qiling!")
    except Exception as e:
        print(f"❌ BASE_CHANNEL xatosi: {e}")
        print(f"⚠️  BASE_CHANNEL_ID ni tekshiring va botni admin qiling!")
    
    # 4. MAIN_CHANNEL tekshirish
    print(f"\n📺 MAIN_CHANNEL_ID: {MAIN_CHANNEL_ID}")
    try:
        main_chat = await bot.get_chat(MAIN_CHANNEL_ID)
        print(f"✅ MAIN_CHANNEL topildi: {main_chat.title}")
        
        # Bot admin ekanligini tekshirish
        bot_member = await bot.get_chat_member(MAIN_CHANNEL_ID, bot_info.id)
        if bot_member.status in ['administrator', 'creator']:
            print(f"✅ Bot MAIN_CHANNEL da ADMIN")
        else:
            print(f"❌ Bot MAIN_CHANNEL da ADMIN EMAS! Status: {bot_member.status}")
            print(f"⚠️  Botni kanalga admin qiling!")
    except Exception as e:
        print(f"❌ MAIN_CHANNEL xatosi: {e}")
        print(f"⚠️  MAIN_CHANNEL_ID ni tekshiring va botni admin qiling!")
    
    # 5. Database tekshirish
    print(f"\n💾 Database tekshiruvi:")
    try:
        import os
        import aiosqlite
        
        db_path = "database/kino_bot.db"
        if os.path.exists(db_path):
            print(f"✅ Database fayli mavjud: {db_path}")
            
            async with aiosqlite.connect(db_path) as db:
                # Movies jadvalini tekshirish
                async with db.execute("PRAGMA table_info(movies)") as cur:
                    columns = await cur.fetchall()
                    column_names = [col[1] for col in columns]
                    
                if 'video_message_id' in column_names:
                    print(f"✅ Movies jadvali yangilangan (video_message_id mavjud)")
                else:
                    print(f"⚠️  Movies jadvali eski (video_file_id). Migration kerak!")
                
                # Episodes jadvalini tekshirish
                async with db.execute("PRAGMA table_info(episodes)") as cur:
                    columns = await cur.fetchall()
                    column_names = [col[1] for col in columns]
                    
                if 'video_message_id' in column_names:
                    print(f"✅ Episodes jadvali yangilangan (video_message_id mavjud)")
                else:
                    print(f"⚠️  Episodes jadvali eski (video_file_id). Migration kerak!")
                
                # Statistika
                async with db.execute("SELECT COUNT(*) FROM movies") as cur:
                    movies_count = (await cur.fetchone())[0]
                async with db.execute("SELECT COUNT(*) FROM serials") as cur:
                    serials_count = (await cur.fetchone())[0]
                async with db.execute("SELECT COUNT(*) FROM users") as cur:
                    users_count = (await cur.fetchone())[0]
                
                print(f"\n📊 Statistika:")
                print(f"   🎬 Kinolar: {movies_count}")
                print(f"   📺 Seriallar: {serials_count}")
                print(f"   👥 Foydalanuvchilar: {users_count}")
        else:
            print(f"❌ Database fayli topilmadi!")
            print(f"⚠️  Botni birinchi marta ishga tushiring!")
    except Exception as e:
        print(f"❌ Database xatosi: {e}")
    
    # Yakuniy xulosa
    print("\n" + "=" * 60)
    print("📋 TEST XULOSASI")
    print("=" * 60)
    print("\n✅ Agar barcha testlar muvaffaqiyatli bo'lsa, botni ishga tushirishingiz mumkin!")
    print("❌ Agar xatoliklar bo'lsa, yuqoridagi yo'riqnomalarni bajaring.\n")
    print("▶️  Botni ishga tushirish: python3 bot.py")
    print("▶️  Migration: python3 migrate_db.py\n")
    
    await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(test_bot())
    except KeyboardInterrupt:
        print("\n\n⚠️  Test to'xtatildi!")
    except Exception as e:
        print(f"\n\n❌ Test xatosi: {e}")
