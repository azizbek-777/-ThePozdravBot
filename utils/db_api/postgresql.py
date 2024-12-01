from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config

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
            username VARCHAR(255) NULL,
            telegram_id BIGINT NOT NULL UNIQUE,
            locale VARCHAR(255) NULL,
            timezone VARCHAR(255) NOT NULL DEFAULT '+5',
            birthday DATE NULL,
            created_at DATE NOT NULL DEFAULT CURRENT_DATE,
            updated_at DATE NOT NULL DEFAULT CURRENT_DATE
        ); 
        """  
        await self.execute(sql, execute=True)
    
    async def create_table_groups(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Groups (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT NOT NULL UNIQUE,
            created_at DATE NOT NULL DEFAULT CURRENT_DATE,
            updated_at DATE NOT NULL DEFAULT CURRENT_DATE
        );
        """
        await self.execute(sql, execute=True)
    
    async def create_table_reminder_groups(self):
        sql = """
        CREATE TABLE IF NOT EXISTS ReminderGroups (
            id SERIAL PRIMARY KEY,
            group_id BIGINT NOT NULL,
            user_id BIGINT NOT NULL,
            created_at DATE NOT NULL DEFAULT CURRENT_DATE,
            updated_at DATE NOT NULL DEFAULT CURRENT_DATE
        );
        """
        await self.execute(sql, execute=True)
        
    async def create_all_tables(self):
        await self.create_table_users() 
        await self.create_table_groups()
        await self.create_table_reminder_groups()

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())
    
    async def add_group(self, telegram_id):
        sql = "INSERT INTO groups (telegram_id) VALUES($1) returning *"
        return await self.execute(sql, telegram_id, fetchrow=True)
    
    async def reminder_group_exists(self, group_id, user_id):
        sql = "SELECT * FROM ReminderGroups WHERE group_id=$1 AND user_id=$2"
        return await self.execute(sql, group_id, user_id, fetchrow=True)
    
    async def add_reminder_group(self, group_id, user_id):
        sql = "INSERT INTO ReminderGroups (group_id, user_id) VALUES($1, $2) returning *"
        return await self.execute(sql, group_id, user_id, fetchrow=True)
    
    async def get_users_for_reminder(self):
        query = """
        SELECT 
            telegram_id,
            birthday,
            timezone
        FROM 
            users
        """
        return await self.execute(query, fetch=True)
        
    async def my_reminder_groups(self, user_id):
        query = """
        SELECT 
            rg.id, 
            rg.group_id, 
            rg.user_id
        FROM 
            public.remindergroups rg
        WHERE
            rg.user_id = $1
        """
        return await self.execute(query, user_id, fetch=True)

    
    async def get_reminder_groups_with_users(self):
        query = """
        SELECT 
            rg.group_id, 
            rg.user_id, 
            u.birthday, 
            u.timezone 
        FROM 
            public.remindergroups rg
        JOIN 
            users u 
        ON 
            rg.user_id = u.telegram_id
        """
        return await self.execute(query, fetch=True)
    
        
    async def get_reminder_groups_with_users_where_group_id(self, group_id):
        query = """
            SELECT 
                rg.group_id, 
                rg.user_id, 
                u.birthday, 
                u.timezone 
            FROM 
                public.remindergroups rg
            JOIN 
                users u 
            ON 
                rg.user_id = u.telegram_id
            WHERE
                rg.group_id = $1
            ORDER BY
                u.birthday DESC
        """
        return await self.execute(query, group_id, fetch=True)

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)
    
    async def get_user_locale(self, telegram_id):
        sql = "SELECT locale FROM Users WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, fetchval=True)
    
    async def set_user_locale(self, locale, telegram_id):
        sql = "UPDATE Users SET locale=$1 WHERE telegram_id=$2"
        return await self.execute(sql, locale, telegram_id, execute=True)
    
    async def set_user_birthdate(self, birthday, telegram_id):
        sql = "UPDATE Users SET birthday=$1 WHERE telegram_id=$2"
        return await self.execute(sql, birthday, telegram_id, execute=True)
    
    async def get_user_birthday(self, telegram_id):
        sql = "SELECT birthday FROM Users WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, fetchval=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

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