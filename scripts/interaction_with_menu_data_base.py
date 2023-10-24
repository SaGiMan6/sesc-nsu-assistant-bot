import aiosqlite


async def check_menu_id(date):
    db = await aiosqlite.connect("data_bases/menu_data_base.db")

    await db.execute("CREATE TABLE IF NOT EXISTS Menus (date TEXT PRIMARY KEY, id TEXT)")

    cursor = await db.execute(f"SELECT date, id FROM Menus WHERE date = ?", (str(date),))
    result = await cursor.fetchone()

    await db.close()

    return result


async def add_menu_id(date, id_string: str):
    db = await aiosqlite.connect("data_bases/menu_data_base.db")

    await db.execute("INSERT INTO Menus (date, id) VALUES (?, ?)", (str(date), id_string))

    await db.commit()
    await db.close()
