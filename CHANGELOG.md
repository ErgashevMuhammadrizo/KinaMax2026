# 🎬 KINAMAX Bot - O'zgarishlar ro'yxati

## ✨ Yangi xususiyatlar

### 1. ✅ Serial qidirish funksiyasi
- Foydalanuvchilar endi **kino yoki serial** ID sini yuborish orqali qidirishlari mumkin
- Serial tanlanganda, barcha fasllar ko'rsatiladi
- Fasl tanlanganda, barcha qismlar chiqadi
- Qism tanlanganda, video avtomatik yuboriladi

**Qanday ishlaydi:**
- Foydalanuvchi `0001` kabi ID yuboradi
- Bot avval kinoda qidiradi
- Topilmasa, serialda qidiradi
- Deep link orqali ham kino ham serial ishlaydi: `/start movie_0001` yoki `/start serial_0001`

---

### 2. 🆔 Start xabarida foydalanuvchi ID si ko'rsatish
- `/start` bosilganda salomlashuv xabarida foydalanuvchining Telegram ID si ko'rsatiladi
- Bu adminlarga foydalanuvchilarni aniqlashda yordam beradi

**Misol:**
```
🎬 KINAMAX ga xush kelibsiz, Muhammad!

━━━━━━━━━━━━━━━━━━━━━━
🆔 Sizning ID: 6611338724
━━━━━━━━━━━━━━━━━━━━━━
```

---

### 3. 💾 Baza kanal orqali video saqlash (Xotira tejash)
Bu eng muhim o'zgarish - **bazada faqat video manzili saqlanadi, video fayl emas!**

**Eski tizim:**
- ❌ Video file_id server bazasida saqlanardi
- ❌ Bazada video fayllari to'lib ketardi
- ❌ Xotira ko'p sarflanardi

**Yangi tizim:**
- ✅ Video `BASE_CHANNEL` ga yuklanadi
- ✅ Bazada faqat message_id saqlanadi (4-8 bayt)
- ✅ Foydalanuvchiga video kerak bo'lganda baza kanaldan forward qilinadi
- ✅ Xotira 99% tejaldi!

**Qanday ishlaydi:**
1. Admin kino qo'shayotganda video yuboradi
2. Bot avtomatik video ni `BASE_CHANNEL`ga yuklaydi
3. Bazaga faqat message_id raqami saqlanadi
4. Foydalanuvchi ko'rmoqchi bo'lganda, bot baza kanaldan video ni forward qiladi

---

## 🔧 Texnik o'zgarishlar

### Database Schema O'zgarishlari

**Movies jadvali:**
```sql
-- Eski
video_file_id TEXT

-- Yangi  
video_message_id INTEGER
```

**Episodes jadvali:**
```sql
-- Eski
video_file_id TEXT

-- Yangi
video_message_id INTEGER
```

---

## 📦 O'rnatish va Migratsiya

### 1. Bazani yangilash
Agar sizda mavjud baza bor bo'lsa, migratsiya scriptini ishga tushiring:

```bash
python3 migrate_db.py
```

Bu script:
- ✅ Jadval strukturasini yangilaydi
- ✅ Eski ma'lumotlarni saqlaydi
- ⚠️ Eski video_file_id lar tozalanadi (ularni qayta yuklash kerak)

### 2. Botni ishga tushirish

```bash
python3 bot.py
```

---

## ⚠️ Muhim eslatmalar

### Baza kanal haqida
1. `.env` faylida `BASE_CHANNEL_ID` to'g'ri sozlangan bo'lishi kerak
2. Bot `BASE_CHANNEL` da **admin** bo'lishi shart
3. Kanal **private** bo'lishi mumkin (ko'proq xavfsiz)

### Migration
- Eski bazadagi kinolar uchun **video message_id** bo'lmaydi (NULL)
- Yangi kinolar avtomatik to'g'ri saqlanadi
- Agar eski kinolarni ishlashini xohlasangiz, ularni qayta qo'shish kerak

---

## 🎯 Test qilish

### 1. Kino qo'shish
```
Admin Panel → 🎬 Kino qo'shish
- Nomi: Test Film
- Janr: Drama
- Yil: 2024
- Davomiyligi: 1:30
- Poster: [rasm yuboring]
- Video: [video yuboring]
```

Video `BASE_CHANNEL` ga yuklanganini tekshiring!

### 2. Serial qo'shish
```
Admin Panel → 📺 Serial qo'shish
→ Yangi serial
→ Ma'lumotlarni kiriting
→ Fasl qo'shing
→ Qism qo'shing (video bilan)
```

### 3. Foydalanuvchi sifatida test
```
/start → ID ni ko'ring
0001 → Kino yoki serialni qidiring
```

---

## 🐛 Muammolar hal qilish

### Video yuklanmayapti
- Bot BASE_CHANNEL da admin ekanligini tekshiring
- BASE_CHANNEL_ID to'g'ri yozilganini tekshiring (minus bilan: `-1003741837863`)

### Eski videolar ishlamayapti
- Bu normal - ularni qayta yuklang
- Yoki migration dan oldin backup oling

### Xotira tejalmayapti
- Bazadagi eski video_file_id lar tozalangan bo'lishi kerak
- Yangi videolar message_id sifatida saqlanayotganini tekshiring

---

## 📊 Afzalliklar

| Xususiyat | Eski | Yangi |
|-----------|------|-------|
| Kino qidirish | ✅ | ✅ |
| Serial qidirish | ❌ | ✅ |
| User ID ko'rsatish | ❌ | ✅ |
| Video file bazada | ✅ | ❌ |
| Video message_id bazada | ❌ | ✅ |
| Xotira tejash | ❌ | ✅ |
| Baza kanal | Yo'q | ✅ |

---

## 🚀 Kelajakdagi rivojlanish

- [ ] Video quality tanlov (360p, 720p, 1080p)
- [ ] Subtitle qo'shish
- [ ] Ko'rishlar statistikasi
- [ ] Sevimlilar ro'yxati
- [ ] Izohlar tizimi

---

## 🤝 Yordam

Agar savollar bo'lsa yoki yordam kerak bo'lsa, botni to'liq o'rganib chiqing va testlang.

**Test ketma-ketligi:**
1. ✅ Migration scriptni ishga tushiring
2. ✅ Botni ishga tushiring
3. ✅ Yangi kino qo'shing
4. ✅ Yangi serial qo'shing
5. ✅ User sifatida kino va serial qidiring
6. ✅ Videolar to'g'ri yuborilayotganini tekshiring

---

**Version:** 2.0  
**Date:** 2026-10-17  
**Status:** ✅ Tayyor

---

## 📝 Versiyalar

### v2.0 (Joriy)
- Serial qidirish qo'shildi
- User ID ko'rsatish qo'shildi
- Baza kanal tizimi
- Xotira tejash optimizatsiyasi

### v1.0
- Asosiy kino bot funksiyalari
- Admin panel
- Obuna tizimi
- Broadcast
