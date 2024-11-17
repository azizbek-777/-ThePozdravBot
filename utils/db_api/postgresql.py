from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from datetime import datetime

from data import config
import pytz

class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        phone varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE 
        );
        """
        await self.execute(sql, execute=True)
    
    async def create_table_channels(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Channels ( 
        id SERIAL PRIMARY KEY,
        channel_id VARCHAR(255) NOT NULL UNIQUE,
        joined_count INT NOT NULL DEFAULT 0
        );
        """
        await self.execute(sql, execute=True)
    
    async def create_table_nominations(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Nominations (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT NOW()
        );
        """
        await self.execute(sql, execute=True)
    
    async def create_table_votes(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Votes (
        id SERIAL PRIMARY KEY,
        user_id INT NOT NULL UNIQUE,
        nomination_id INT NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
        FOREIGN KEY (user_id) REFERENCES Users(id),
        FOREIGN KEY (nomination_id) REFERENCES Nominations(id)
        );
        """
        await self.execute(sql, execute=True) 
    
    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_all_users(self): 
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)
    
    async def is_exists_phone_by_telegram_id(self, telegram_id):
        sql = "SELECT phone FROM Users WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, fetchval=True)
    
    async def add_phone_by_telegram_id(self, telegram_id, phone):
        sql = "UPDATE Users SET phone=$1 WHERE telegram_id=$2"
        return await self.execute(sql, phone, telegram_id, execute=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)
        
    async def add_channel(self, channel_id):
        sql = "INSERT INTO channels (channel_id) VALUES($1) returning *"
        return await self.execute(sql, channel_id, fetchrow=True)
    
    async def select_all_channels(self, limit: int = 50, offset: int = 0):
        sql = "SELECT * FROM Channels LIMIT $1 OFFSET $2"
        return await self.execute(sql, limit, offset, fetch=True)
    
    async def delete_channel(self, channel_id):
        sql = "DELETE FROM Channels WHERE channel_id = $1"
        return await self.execute(sql, channel_id, execute=True)
    
    async def select_all_nominations(self):
        sql = "SELECT * FROM Nominations"
        return await self.execute(sql, fetch=True)
    
    async def nominate_by_id(self, nomination_id):
        sql = "SELECT * FROM Nominations WHERE id=$1"
        return await self.execute(sql, nomination_id, fetchrow=True)
    
    async def is_exists_vote(self, user_id, nomination_id):
        sql = "SELECT * FROM Votes WHERE user_id=$1 AND nomination_id=$2"
        return await self.execute(sql, user_id, nomination_id, fetchrow=True)
    
    async def add_vote(self, user_id, nomination_id):
        if await self.is_exists_vote(user_id, nomination_id):
            return False
        sql = "INSERT INTO Votes (user_id, nomination_id) VALUES($1, $2) returning *"
        return await self.execute(sql, user_id, nomination_id, fetchrow=True)
    
    async def count_votes(self, nomination_id):
        sql = "SELECT COUNT(*) as count_votes FROM Votes WHERE nomination_id=$1"
        return await self.execute(sql, nomination_id, fetchval=True)
    
    async def get_nomination_rank(self, nomination_id):
        # Barcha nominatsiyalar va ularning ovozlari sonini olish (created_at bo'yicha ham tartiblangan)
        sql = """
        SELECT nomination_id, COUNT(*) as vote_count, MAX(created_at) as last_vote_time
        FROM Votes
        GROUP BY nomination_id
        ORDER BY vote_count DESC, last_vote_time ASC, nomination_id ASC
        """
        nominations = await self.execute(sql, fetch=True)
        
        # Debugging: nominations'ni chiqarish
        print(f"Nominations: {nominations}")

        # Nominatsiya uchun rankni aniqlash
        for rank, nomination in enumerate(nominations, start=1):
            if nomination['nomination_id'] == nomination_id:
                return rank

        # Agar nominatsiya topilmasa, 0 qaytadi
        return 0
    
    async def get_nominations_ranking(self):
        # Define Tashkent timezone
        tashkent_tz = pytz.timezone("Asia/Tashkent")

        # SQL query to get all nominations and their vote count
        sql = """
        SELECT 
            n.id, 
            n.title, 
            COUNT(v.id) as vote_count, 
            MAX(v.created_at) as last_vote_time
        FROM 
            Nominations n
        LEFT JOIN 
            Votes v ON n.id = v.nomination_id
        GROUP BY 
            n.id, n.title
        ORDER BY 
            vote_count DESC, last_vote_time ASC, n.id ASC
        """
        
        # Fetch results
        nominations = await self.execute(sql, fetch=True)
        
        # Create the ranking
        ranking = []
        for rank, nomination in enumerate(nominations, start=1):
            last_vote_time = nomination['last_vote_time']
            
            # If `last_vote_time` is not None and is a datetime object
            if last_vote_time:
                # Convert to Tashkent time zone
                last_vote_time_tashkent = last_vote_time.replace(tzinfo=pytz.UTC).astimezone(tashkent_tz)
                formatted_time = last_vote_time_tashkent.strftime("%d.%m.%Y %H:%M")
            else:
                formatted_time = " "

            ranking.append({
                "rank": rank,
                "nomination_id": nomination['id'],
                "title": nomination['title'],
                "vote_count": nomination['vote_count'],
                "last_vote_time": formatted_time
            })
        
        return ranking
    



