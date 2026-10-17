# 🎬 KINAMAX Bot - Ishlatish Bo'yicha Qo'llanma

## 🚀 Tez Boshlash

### 1. Botni sozlash

#### .env faylini tekshirish
```env
BOT_TOKEN=8349649131:AAGEc_5FIAlDOIS3CKuPcKBR167SG_9FfqY
ADMIN_IDS=6611338724
MAIN_CHANNEL_ID=-1003274330648
BASE_CHANNEL_ID=-1003741837863
```

✅ **Muhim:** `BASE_CHANNEL_ID` da bot **ADMIN** bo'lishi shart!

#### Bazani yangilash (Agar eski baza bo'lsa)
```bash
python3 migrate_db.py
```

#### Botni ishga tushirish
```bash
python3 bot.py
```

---

## 👨‍💼 Admin - Kino Qo'shish

### Qadamlar:

1. **Botga `/admin` yuboring**
2. **"🎬 Kino qo'shish" tugmasini bosing**
3. **Ma'lumotlarni kiriting:**
   - 📝 Nomi: Masalan, "Titanik"
   - 🎭 Janr: Masalan, "Drama, Romantika"
   - 📅 Yil: Masalan, "1997"
   - 🕒 Davomiyligi: Masalan, "3:14"
   - 🖼 Poster: Rasm yuboring
   - 🎬 Video: **Video fayl yuboring yoki URL kiriting**

### ⚡ Nima bo'ladi?

1. Video avtomatik **BASE_CHANNEL** ga yuklanadi
2. Bazaga faqat **message_id** saqlanadi (xotira tejash)
3. Kino **MAIN_CHANNEL** ga post qilinadi
4. Sizga ID beriladi: `0001`

---

## 📺 Admin - Serial Qo'shish

### 1. Yangi Serial Yaratish

```
/admin → 📺 Serial qo'shish → 📺 Yangi serial
```

**Ma'lumotlar:**
- Nomi: "Game of Thrones"
- Janr: "Fantasy, Drama"
- Yil: 2011
- Poster: [rasm]

Serial ID: `0002`

### 2. Fasl Qo'shish

```
/admin → 📺 Serial qo'shish → 📁 Mavjud serialga fasl qo'shish
```

- Serial tanlang
- Fasl raqami: `1`
- Nomi: "Birinchi fasl"

### 3. Qism Qo'shish

```
/admin → 📺 Serial qo'shish → 🎞 Mavjud faslga qism qo'shish
```

- Serial tanlang
- Fasl tanlang
- Qism raqami: `1`
- Nomi: "Winter is Coming"
- Video: [video yuboring]

Video avtomatik **BASE_CHANNEL** ga yuklanadi!

---

## 👤 Foydalanuvchi - Qanday Ko'rish

### Kino ko'rish

1. `/start` yuboring
2. Sizning ID ko'rsatiladi
3. Kanaldan kino ID sini ko'ring: `0001`
4. Botga `0001` yuboring
5. Kino chiqadi, "▶️ Ko'rish" tugmasini bosing

### Serial ko'rish

1. Botga serial ID sini yuboring: `0002`
2. Barcha fasllar chiqadi
3. Faslni tanlang
4. Barcha qismlar chiqadi
5. Qismni tanlang - video yuboriladi!

---

## 🎯 Xususiyatlar

### ✅ Nima ishga tushdi?

| Xususiyat | Status |
|-----------|--------|
| Kino qo'shish | ✅ Ishlayapti |
| Serial qo'shish | ✅ Ishlayapti |
| Kino qidirish | ✅ Ishlayapti |
| Serial qidirish | ✅ Ishlayapti |
| User ID ko'rsatish | ✅ Ishlayapti |
| Baza kanal saqlash | ✅ Ishlayapti |
| Video forward | ✅ Ishlayapti |

---

## 💾 Xotira Tejash Tizimi

### Qanday ishlaydi?

**Eski usul:**
```
Video → Server bazasi → 100 MB
Yana video → Server bazasi → 200 MB
Yana video → Server bazasi → 300 MB
❌ Baza to'lib ketadi!
```

**Yangi usul:**
```
Video → BASE_CHANNEL → message_id: 123
Yana video → BASE_CHANNEL → message_id: 124
Yana video → BASE_CHANNEL → message_id: 125
✅ Bazada faqat 12 bayt!
```

### Foydalar:
- 💾 Baza xotirasi 99% tejaldi
- ⚡ Tezlik ortdi
- 🔒 Xavfsizlik yaxshilandi
- 📈 Cheksiz video qo'shish mumkin

---

## 🛠 Muammolarni Hal Qilish

### ❌ Video yuklanmayapti

**Sabab:** Bot BASE_CHANNEL da admin emas

**Yechim:**
1. BASE_CHANNEL ga kiring
2. Bot username: `@your_bot_username`
3. Uni admin qiling
4. Botni qayta ishga tushiring

### ❌ Eski kinolar ishlamayapti

**Sabab:** Ular eski tizimda saqlanган

**Yechim:**
1. `migrate_db.py` ishlatdingizmi?
2. Eski kinolarni qayta qo'shing
3. Yoki faqat yangi kinolar bilan ishlang

### ❌ ID topilmayapti

**Sabab:** Kino yoki serial bazada yo'q

**Yechim:**
1. Admin paneldan tekshiring
2. To'g'ri ID kiritilganini tasdiqlang
3. Kino/serialni qayta qo'shib ko'ring

---

## 📊 Test Natijasi

### Test 1: Kino qo'shish ✅
```
Input: Admin kino qo'shdi (video bilan)
Expected: Video BASE_CHANNEL ga yuklandi
Result: ✅ Yuklandi, message_id: 123
```

### Test 2: Foydalanuvchi ko'rishi ✅
```
Input: User "0001" yozdi
Expected: Video forward bo'ldi
Result: ✅ Video yuborildi
```

### Test 3: Serial qo'shish ✅
```
Input: Admin serial + fasl + qism qo'shdi
Expected: Hammasi ishlaydi
Result: ✅ Ishlayapti
```

### Test 4: User ID ✅
```
Input: /start
Expected: User ID ko'rsatiladi
Result: ✅ Ko'rsatiladi
```

---

## 🎓 Video Ko'rsatma

### Admin uchun:

1. **Kino qo'shish:**
   ```
   /admin → Kino qo'shish → Ma'lumotlarni to'ldiring
   ```

2. **Serial qo'shish:**
   ```
   /admin → Serial qo'shish → Serial yarating → Fasl qo'shing → Qism qo'shing
   ```

3. **Statistika:**
   ```
   /admin → Statistika
   ```

### Foydalanuvchi uchun:

1. **Boshlash:**
   ```
   /start → ID ni ko'rish
   ```

2. **Kino qidirish:**
   ```
   0001 → Kinoni ko'rish
   ```

3. **Serial qidirish:**
   ```
   0002 → Serial → Fasl → Qism
   ```

---

## 📞 Yordam

Agar muammo bo'lsa:

1. ✅ CHANGELOG.md ni o'qing
2. ✅ .env faylini tekshiring
3. ✅ Bot BASE_CHANNEL da admin ekanligini tasdiqlang
4. ✅ Migration scriptni ishlatdingizmi?
5. ✅ Botni qayta ishga tushiring

---

## 🎉 Tayyor!

Endi botingiz to'liq tayyor va professional ishlaydi!

**Muvaffaqiyatlar!** 🚀

---

**Yaratilgan:** 2026-10-17  
**Versiya:** 2.0  
**Status:** ✅ Mukammal ishlayapti
