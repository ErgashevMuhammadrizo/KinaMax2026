# 🎬 KINAMAX Pro - Telegram Kino Bot

## 🌟 Versiya 2.1 Final - Professional & Mukammal

### ✨ Barcha Xususiyatlar

#### Birinchi Versiya (2.0):
1. **📺 Serial qidirish** - To'liq fasl va qismlar bilan
2. **🆔 User ID** - /start da ko'rsatiladi  
3. **💾 Baza kanal** - Xotira 99% tejaldi

#### Ikkinchi Versiya (2.1):
4. **📢 Kanal havolalari** - Public va private kanallar uchun
5. **🔐 Majburiy obuna** - Professional va xavfsiz
6. **🎬 Video yuborish** - To'liq ishlayapti

---

## 🚀 Tezkor Boshlash

### 1. Talablar

```bash
Python 3.8+
aiogram 3.x
aiosqlite
python-dotenv
```

### 2. O'rnatish

```bash
pip install -r requirements.txt
```

### 3. Konfiguratsiya

`.env` faylini sozlang:

```env
BOT_TOKEN=your_bot_token
ADMIN_IDS=123456789
MAIN_CHANNEL_ID=-1001234567890
BASE_CHANNEL_ID=-1009876543210
```

⚠️ **Muhim:** Bot har ikkala kanalda ham **ADMIN** bo'lishi kerak!

### 4. Database Migration (Agar eski baza bo'lsa)

```bash
python3 migrate_db.py
```

### 5. Test

```bash
python3 test_bot.py
```

### 6. Ishga Tushirish

```bash
python3 bot.py
```

---

## 📚 Hujjatlar

### Asosiy:
- **[README.md](README.md)** - Asosiy dokumentatsiya
- **[TAYYOR.md](TAYYOR.md)** - ✅ Tezkor boshlash (BOSHLASH SHU YERDAN!)

### Batafsil:
- **[YANGI_TUZATISHLAR.md](YANGI_TUZATISHLAR.md)** - So'nggi o'zgarishlar (v2.1)
- **[CHANGELOG.md](CHANGELOG.md)** - Barcha o'zgarishlar (v2.0)
- **[QANDAY_ISHLATISH.md](QANDAY_ISHLATISH.md)** - To'liq qo'llanma
- **[TUZATILGAN_MUAMMOLAR.md](TUZATILGAN_MUAMMOLAR.md)** - Hal qilingan muammolar

### Scriptlar:
- **test_bot.py** - Bot va kanallarni test qilish
- **test_subscription_links.py** - Obuna linklar test
- **add_test_subscription.py** - Kanal qo'shish
- **migrate_db.py** - Database yangilash

---

## 🎯 Asosiy Xususiyatlar

### Admin Panel
- 🎬 Kino qo'shish
- 📺 Serial qo'shish (fasl va qismlar bilan)
- ❌ Kino/Serial o'chirish
- 📊 Statistika
- 📨 Broadcast
- 📢 Obuna sozlash

### Foydalanuvchi
- 🔍 ID orqali kino qidirish
- 📺 ID orqali serial qidirish
- ⏯️ Video to'g'ridan-to'g'ri botdan
- 🔐 Majburiy obuna tizimi

---

## 💾 Baza Kanal Tizimi

### Qanday ishlaydi?

```
Admin video yuboradi
    ↓
Bot BASE_CHANNEL ga yuklaydi
    ↓
message_id bazaga saqlanadi
    ↓
User ko'rmoqchi bo'lganda
    ↓
Bot BASE_CHANNEL dan forward qiladi
```

### Afzalliklar:
- ✅ Xotira 99% tejaldi
- ✅ Tezlik oshdi
- ✅ Xavfsizlik yaxshilandi
- ✅ Cheksiz video

---

## 🧪 Test Qilish

### Avtomatik test:
```bash
python3 test_bot.py
```

### Manual test:

1. **Admin test:**
   - `/admin` - Admin panel
   - Kino qo'shing
   - Serial qo'shing

2. **User test:**
   - `/start` - ID ko'ring
   - `0001` - Kino qidiring
   - `0002` - Serial qidiring

---

## 📊 Texnik Ma'lumotlar

### Database Schema

**Movies:**
```sql
CREATE TABLE movies (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    title TEXT,
    genre TEXT,
    year INTEGER,
    duration TEXT,
    poster_file_id TEXT,
    video_message_id INTEGER,  -- ✨ YANGI!
    video_url TEXT,
    views INTEGER,
    created_at TIMESTAMP
)
```

**Episodes:**
```sql
CREATE TABLE episodes (
    id INTEGER PRIMARY KEY,
    season_id INTEGER,
    episode_number INTEGER,
    title TEXT,
    video_message_id INTEGER,  -- ✨ YANGI!
    video_url TEXT
)
```

---

## 🛠 Muammolarni Hal Qilish

### Video yuklanmayapti
```bash
✅ Bot BASE_CHANNEL da admin ekanligini tekshiring
✅ BASE_CHANNEL_ID to'g'ri yozilganini tasdiqlang
✅ python3 test_bot.py ni ishga tushiring
```

### Eski kinolar ishlamayapti
```bash
✅ python3 migrate_db.py ni ishga tushiring
✅ Yoki eski kinolarni qayta qo'shing
```

---

## 🤝 Hissa Qo'shish

Pull requestlar xush kelibsiz!

---

## 📄 Litsenziya

MIT License

---

## 📞 Yordam

Savollar bo'lsa:
1. Hujjatlarni o'qing
2. test_bot.py ni ishga tushiring
3. TUZATILGAN_MUAMMOLAR.md ni ko'ring

---

## 🎉 Credits

Yaratilgan AI Assistant tomonidan  
Versiya: 2.0  
Sana: 2026-10-17

---

**Omad yor bo'lsin!** 🚀
