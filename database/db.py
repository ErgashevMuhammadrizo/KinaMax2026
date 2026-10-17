import os

import aiosqlite

DB_PATH = "database/kino_bot.db"


async def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if os.path.exists(DB_PATH) and os.path.getsize(DB_PATH) == 0:
        open(DB_PATH, "wb").close()

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                genre TEXT,
                year INTEGER,
                duration TEXT,
                poster_file_id TEXT,
                video_message_id INTEGER,
                video_url TEXT,
                views INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS serials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                genre TEXT,
                year INTEGER,
                poster_file_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS seasons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                serial_id INTEGER NOT NULL,
                season_number INTEGER NOT NULL,
                title TEXT,
                FOREIGN KEY (serial_id) REFERENCES serials(id)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS episodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                season_id INTEGER NOT NULL,
                episode_number INTEGER NOT NULL,
                title TEXT,
                video_message_id INTEGER,
                video_url TEXT,
                FOREIGN KEY (season_id) REFERENCES seasons(id)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id TEXT NOT NULL,
                channel_title TEXT,
                channel_username TEXT,
                is_active INTEGER DEFAULT 1
            )
        """)
        # Users jadvali - broadcast uchun
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                is_blocked INTEGER DEFAULT 0,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()


# ==================== USERS ====================

async def add_or_update_user(user_id: int, username: str = None, first_name: str = None, last_name: str = None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO users (id, username, first_name, last_name)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                username = excluded.username,
                first_name = excluded.first_name,
                last_name = excluded.last_name
        """, (user_id, username, first_name, last_name))
        await db.commit()


async def get_all_users():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE is_blocked=0") as cur:
            return await cur.fetchall()


async def get_users_count():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM users") as cur:
            row = await cur.fetchone()
            return row[0] if row else 0


async def block_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET is_blocked=1 WHERE id=?", (user_id,))
        await db.commit()


# ==================== MOVIES ====================

async def add_movie(code, title, genre, year, duration, poster_file_id=None, video_message_id=None, video_url=None):
    async with aiosqlite.connect(DB_PATH) as db:
        try:
            await db.execute("""
                INSERT INTO movies (code, title, genre, year, duration, poster_file_id, video_message_id, video_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (code, title, genre, year, duration, poster_file_id, video_message_id, video_url))
            await db.commit()
            async with db.execute("SELECT id FROM movies WHERE code=?", (code,)) as cur:
                row = await cur.fetchone()
                return row[0] if row else None
        except Exception:
            return None


async def get_movie_by_code(code: str):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM movies WHERE code=?", (code,)) as cur:
            return await cur.fetchone()


async def get_movie_by_id(movie_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM movies WHERE id=?", (movie_id,)) as cur:
            return await cur.fetchone()


async def delete_movie(code: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM movies WHERE code=?", (code,))
        await db.commit()


async def update_movie_views(movie_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE movies SET views = views + 1 WHERE id=?", (movie_id,))
        await db.commit()


# ==================== SERIALS ====================

async def add_serial(code, title, genre, year, poster_file_id=None):
    async with aiosqlite.connect(DB_PATH) as db:
        try:
            await db.execute("""
                INSERT INTO serials (code, title, genre, year, poster_file_id)
                VALUES (?, ?, ?, ?, ?)
            """, (code, title, genre, year, poster_file_id))
            await db.commit()
            async with db.execute("SELECT id FROM serials WHERE code=?", (code,)) as cur:
                row = await cur.fetchone()
                return row[0] if row else None
        except Exception:
            return None


async def get_serial_by_code(code: str):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM serials WHERE code=?", (code,)) as cur:
            return await cur.fetchone()


async def get_serial_by_id(serial_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM serials WHERE id=?", (serial_id,)) as cur:
            return await cur.fetchone()


async def get_all_serials():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM serials ORDER BY created_at DESC") as cur:
            return await cur.fetchall()


async def add_season(serial_id, season_number, title=None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO seasons (serial_id, season_number, title) VALUES (?, ?, ?)
        """, (serial_id, season_number, title))
        await db.commit()
        async with db.execute("SELECT last_insert_rowid()") as cur:
            row = await cur.fetchone()
            return row[0]


async def get_seasons(serial_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM seasons WHERE serial_id=? ORDER BY season_number", (serial_id,)) as cur:
            return await cur.fetchall()


async def add_episode(season_id, episode_number, title=None, video_message_id=None, video_url=None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO episodes (season_id, episode_number, title, video_message_id, video_url)
            VALUES (?, ?, ?, ?, ?)
        """, (season_id, episode_number, title, video_message_id, video_url))
        await db.commit()


async def get_episodes(season_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM episodes WHERE season_id=? ORDER BY episode_number", (season_id,)) as cur:
            return await cur.fetchall()


async def get_episode(episode_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM episodes WHERE id=?", (episode_id,)) as cur:
            return await cur.fetchone()


# ==================== SUBSCRIPTIONS ====================

async def add_subscription(channel_id, channel_title, channel_username=None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO subscriptions (channel_id, channel_title, channel_username)
            VALUES (?, ?, ?)
        """, (channel_id, channel_title, channel_username))
        await db.commit()


async def get_all_subscriptions():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM subscriptions WHERE is_active=1") as cur:
            return await cur.fetchall()


async def delete_subscription(sub_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM subscriptions WHERE id=?", (sub_id,))
        await db.commit()
