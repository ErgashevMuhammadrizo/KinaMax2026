#!/usr/bin/env python3
"""
Database migration script to update existing database structure
Changes:
- Rename video_file_id to video_message_id in movies table
- Rename video_file_id to video_message_id in episodes table
"""

import asyncio
import aiosqlite
import os

DB_PATH = "database/kino_bot.db"


async def migrate():
    if not os.path.exists(DB_PATH):
        print("❌ Database file not found!")
        return
    
    async with aiosqlite.connect(DB_PATH) as db:
        # Check if old column exists in movies table
        async with db.execute("PRAGMA table_info(movies)") as cur:
            columns = await cur.fetchall()
            column_names = [col[1] for col in columns]
            
        if 'video_file_id' in column_names:
            print("🔄 Migrating movies table...")
            # Create new table with updated schema
            await db.execute("""
                CREATE TABLE IF NOT EXISTS movies_new (
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
            
            # Copy data
            await db.execute("""
                INSERT INTO movies_new (id, code, title, genre, year, duration, poster_file_id, video_message_id, video_url, views, created_at)
                SELECT id, code, title, genre, year, duration, poster_file_id, NULL, video_url, views, created_at FROM movies
            """)
            
            # Replace old table
            await db.execute("DROP TABLE movies")
            await db.execute("ALTER TABLE movies_new RENAME TO movies")
            print("✅ Movies table migrated!")
        else:
            print("✅ Movies table already up-to-date!")
        
        # Check if old column exists in episodes table
        async with db.execute("PRAGMA table_info(episodes)") as cur:
            columns = await cur.fetchall()
            column_names = [col[1] for col in columns]
            
        if 'video_file_id' in column_names:
            print("🔄 Migrating episodes table...")
            # Create new table with updated schema
            await db.execute("""
                CREATE TABLE IF NOT EXISTS episodes_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    season_id INTEGER NOT NULL,
                    episode_number INTEGER NOT NULL,
                    title TEXT,
                    video_message_id INTEGER,
                    video_url TEXT,
                    FOREIGN KEY (season_id) REFERENCES seasons(id)
                )
            """)
            
            # Copy data
            await db.execute("""
                INSERT INTO episodes_new (id, season_id, episode_number, title, video_message_id, video_url)
                SELECT id, season_id, episode_number, title, NULL, video_url FROM episodes
            """)
            
            # Replace old table
            await db.execute("DROP TABLE episodes")
            await db.execute("ALTER TABLE episodes_new RENAME TO episodes")
            print("✅ Episodes table migrated!")
        else:
            print("✅ Episodes table already up-to-date!")
        
        await db.commit()
        print("\n🎉 Migration completed successfully!")
        print("\n⚠️  IMPORTANT:")
        print("   - Old video_file_id values were not migrated")
        print("   - You need to re-upload videos to BASE_CHANNEL")
        print("   - New videos will automatically be stored correctly")


if __name__ == "__main__":
    asyncio.run(migrate())
