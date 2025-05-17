import aiosqlite

DB_MAIN = "main.sql"

async def enable_foreign_keys(db):
    await db.execute("PRAGMA foreign_keys = ON")

async def init_db():
    async with aiosqlite.connect(DB_MAIN) as db:
        await enable_foreign_keys(db)
        await db.execute('''
                        CREATE TABLE IF NOT EXISTS categories(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        name TEXT )
''')
        await db.execute('''
                        CREATE TABLE IF NOT EXISTS expences(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        category_id INTEGER,
                        amount REAL,
                        date TEXT,
                        FOREIGN KEY(category_id) REFERENCES categories(id))
''')
        await db.commit()

async def add_category(user_id, name):
    async with aiosqlite.connect(DB_MAIN) as db:
        await enable_foreign_keys(db)
        await db.execute('''
                        INSERT INTO categories (user_id, name)
                        VALUES (?,?)
''', (user_id, name))
        await db.commit()
        

async def get_amount(user_id):
    async with aiosqlite.connect(DB_MAIN) as db:
        await enable_foreign_keys(db)
        cursor = await db.execute('''
                                SELECT e.amount, e.date, c.name
                                FROM expenses e
                                JOIN categories c ON e.category_id = c.id
                                WHERE user_id = ?
                                ORDER BY e.date DESC
''', (user_id))
        return await cursor.fetchall()
    

async def add_expenses(user_id, category_id, amount, date):
    async with aiosqlite.connect(DB_MAIN) as db:
        await enable_foreign_keys(db)
        await db.execute('''
                        INSERT INTO expenses(user_id, category_id, amount, date)
                         VALUES(?,?,?,?)
''')
        await db.commit()


async def update_categories(category_id, new_name):
    async with aiosqlite.connect(DB_MAIN) as db:
        cursor = await db.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
        row = await cursor.fetchone()
        if not row:
            print(f"❌ Категорії з id={category_id} не існує!")
            return
        await db.execute("UPDATE categories SET name = ? WHERE id = ?",(new_name, category_id))
        await db.commit()
        print(f"✅ Категорію з id={category_id} оновлено до '{new_name}'")

async def del_categories(user_id):
    async with aiosqlite.connect(DB_MAIN) as db:
        await enable_foreign_keys(db)
        await db.execute("DELETE FROM categories WHERE user_id = ?", (user_id,))
        await db.execute("DELETE FROM sqlite_sequence WHERE name = 'categories'")
        await db.commit()
        print("Категорії видаленні")