import asyncio

from utils.db_api.postgresql import Database


async def test():
    db = Database()
    await db.create()

    print("Users jadvalini yaratamiz...")
    # await db.drop_users()
    await db.create_table_users()
    print("Yaratildi")


# asyncio.run(test())