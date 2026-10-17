# 🎬 Kino Bot

## O'rnatish

1. Kerakli kutubxonalarni o'rnatish:
```bash
pip install -r requirements.txt
```

2. `.env` faylini yarating va to'ldiring:
```
BOT_TOKEN=your_bot_token_here
ADMIN_IDS=123456789
BASE_CHANNEL_ID=-1001234567890
```

3. Botni ishga tushirish:
```bash
python bot.py
```

---

## ⚙️ Sozlash

| O'zgaruvchi | Tavsif |
|---|---|
| `BOT_TOKEN` | BotFather dan olingan token |
| `ADMIN_IDS` | Admin Telegram ID lari (vergul bilan) |
| `BASE_CHANNEL_ID` | Kino/serial postlarinatuvchi kanal ID si |

> Kanal ID ni olish uchun botni kanalga admin qilib qo'shing va @getidsbot yoki shunga o'xshash bot ishlatining.

---

## 🚀 Qanday ishlaydi

### Admin:
1. `/admin` → Admin panel ochiladi
2. **Kino qo'shish** → Nom, janr, yil, poster, video so'raladi → **4 xonali ID beriladi** (0001, 0002...) → **kanalga avtomatik post qilinadi**
3. **Serial qo'shish** → Yangi serial → Fasl → Qism ketma-ketligi
4. Post tugmasida `▶️ Ko'rish` tugmasi bo'ladi, foydalanuvchi bosganida bot ochiladi

### Foydalanuvchi:
1. Kanaldan `▶️ Ko'rish` bosadi → bot ochiladi, kino/serial chiqadi
2. Yoki botga ID ni yozadi (masalan: `0001`) → kino/serial topiladi
3. `/serials` → Barcha seriallar ro'yxati

---

## 📋 Admin buyruqlari

- `/admin` — Admin panel
- Kino qo'shish, o'chirish
- Serial + fasl + qism qo'shish
- Obuna kanallarini boshqarish
- Statistika ko'rish
