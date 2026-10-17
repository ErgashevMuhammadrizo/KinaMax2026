#!/usr/bin/env python3
"""
Test uchun majburiy obuna kanali qo'shish
"""

import asyncio
import aiosqlite


async def add_test_subscription():
    """Test kanal qo'shish"""
    
    print("=" * 60)
    print("📢 MAJBURIY OBUNA KANAL QO'SHISH")
    print("=" * 60)
    
    # Kanal ma'lumotlarini so'rash
    print("\n1. Kanal turini tanlang:")
    print("   a) Public kanal (@username bilan)")
    print("   b) Private kanal (faqat ID)")
    
    choice = input("\nTanlov (a/b): ").strip().lower()
    
    if choice == 'a':
        # Public kanal
        username = input("\nKanal username (@kinamax_channel): ").strip()
        channel_id = input("Kanal ID (-1001234567890): ").strip()
        title = input("Kanal nomi (KINAMAX Channel): ").strip()
        
        async with aiosqlite.connect("database/kino_bot.db") as db:
            await db.execute("""
                INSERT INTO subscriptions (channel_id, channel_title, channel_username)
                VALUES (?, ?, ?)
            """, (channel_id, title, username))
            await db.commit()
        
        print(f"\n✅ Kanal qo'shildi!")
        print(f"   Nomi: {title}")
        print(f"   Username: {username}")
        print(f"   ID: {channel_id}")
        print(f"\n📌 Havolasi: https://t.me/{username.lstrip('@')}")
        
    elif choice == 'b':
        # Private kanal
        channel_id = input("\nKanal ID (-1001234567890): ").strip()
        title = input("Kanal nomi (KINAMAX VIP): ").strip()
        
        async with aiosqlite.connect("database/kino_bot.db") as db:
            await db.execute("""
                INSERT INTO subscriptions (channel_id, channel_title, channel_username)
                VALUES (?, ?, NULL)
            """, (channel_id, title))
            await db.commit()
        
        # Private kanal uchun link yasash
        if channel_id.startswith('-100'):
            clean_id = channel_id[4:]
            link = f"https://t.me/c/{clean_id}/1"
        else:
            link = f"https://t.me/c/{channel_id.lstrip('-')}/1"
        
        print(f"\n✅ Kanal qo'shildi!")
        print(f"   Nomi: {title}")
        print(f"   ID: {channel_id}")
        print(f"\n📌 Havolasi: {link}")
    
    else:
        print("\n❌ Noto'g'ri tanlov!")
        return
    
    # Barcha kanallarni ko'rsatish
    print("\n" + "=" * 60)
    print("📋 BARCHA MAJBURIY OBUNA KANALLARI")
    print("=" * 60)
    
    async with aiosqlite.connect("database/kino_bot.db") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM subscriptions WHERE is_active=1") as cur:
            subs = await cur.fetchall()
    
    if not subs:
        print("\n❌ Hozircha kanallar yo'q")
    else:
        for i, sub in enumerate(subs, 1):
            print(f"\n{i}. {sub['channel_title']}")
            print(f"   ID: {sub['channel_id']}")
            if sub['channel_username']:
                print(f"   Username: {sub['channel_username']}")
                print(f"   Link: https://t.me/{sub['channel_username'].lstrip('@')}")
            else:
                if sub['channel_id'].startswith('-100'):
                    clean_id = sub['channel_id'][4:]
                    print(f"   Link: https://t.me/c/{clean_id}/1")
    
    print("\n✅ Tayyor! Botni ishga tushiring va test qiling.")


if __name__ == "__main__":
    try:
        asyncio.run(add_test_subscription())
    except KeyboardInterrupt:
        print("\n\n⚠️ Bekor qilindi!")
    except Exception as e:
        print(f"\n\n❌ Xatolik: {e}")
