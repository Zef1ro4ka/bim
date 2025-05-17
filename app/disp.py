from datetime import datetime
from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import aiosqlite
import app.keyboard as kb
import app.database.database as DB


router = Router()

class CategoryState(StatesGroup):
    new_categories = State()
    edit_category = State()
    delete_category = State()


@router.message(CommandStart())
async def cmd_start(message:Message):
    await DB.init_db()
    await message.answer("Hello",reply_markup=kb.main_kb())

@router.message(F.text == 'Додати витрату') 
@router.message(Command("add_expense"))
async def cmd_add_expense(message: Message):
    user_id = message.from_user.id
    await message.answer("bim bom")

@router.message(F.text == "Статистика")
@router.message(Command('statistic'))
async def cmd_statistic(message: Message):
    await message.answer("Тут буде твоя статистика", reply_markup=kb.statistic_kb())

@router.callback_query(F.data == "today")
async def cmd_today(callback: CallbackQuery):
    await callback.message.answer("today")
    await callback.answer()

@router.callback_query(F.data == "month")
async def cmd_month(callback: CallbackQuery):
    await callback.message.answer("month")
    await callback.answer()

@router.callback_query(F.data == "categories")
async def cmd_scategories(callback: CallbackQuery):
    await callback.message.answer("categories", reply_markup=kb.categories_kb())
    await callback.answer()

@router.callback_query(F.data == 'Очистити список')
async def cmd_delete_category(callback: CallbackQuery):
    pass

@router.message(F.text == 'Змінити категорію')
async def cmd_edit_category(message: Message, state: FSMContext):
    keyboard = await kb.edit_catigories_kb(message.from_user.id)
    await message.answer("Оберіть категрію для редагування", reply_markup=keyboard)


@router.callback_query(F.data.startswith("edit_category:"))
async def proccess_edit_category(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.split(":")[1])
    await state.update_data(edit_category_id = category_id)    
    await callback.message.answer("Введіть нову назву для категорії")
    await callback.answer()
    await state.set_state(CategoryState.edit_category)

@router.message(CategoryState.edit_category)
async def end_edit_category(message: Message, state: FSMContext):
    new_name = message.text
    data = await state.get_data()
    category_id = data.get("edit_category_id")
    print(f"Оновлюємо категорію ID: {category_id}, нова назва: {new_name}")
    await DB.update_categories(category_id,new_name)
    await message.answer("Категорію успішно оновленно")
    await state.clear()



@router.message(F.text == 'Додати категорію')
async def cmd_add_category(message: Message, state: FSMContext):
    await message.answer("Введіть назву нової категорії")
    await state.set_state(CategoryState.new_categories)


@router.message(CategoryState.new_categories)
async def add_category(message: Message, state: FSMContext):
    category_name = message.text.strip()
    user_id = message.from_user.id
    async with aiosqlite.connect(DB.DB_MAIN) as db:
        await db.enable_load_extension(db)
        cursor = await db.execute('SELECT id FROM categories WHERE user_id = ? AND name = ?', (user_id, category_name))
        exist = await cursor.fetchone()
        if exist:
            await message.answer("Така категорія вже існує")
            await state.clear()
            return
        await db.execute("INSERT INTO categories (user_id, name) VALUES (?,?)", (user_id, category_name))
        await db.commit()
    await message.answer(f"Категорію {category_name} сворено успішно!)")
    await state.clear()
 

@router.message(F.text == 'Список категорій')
async def list_categories(message: Message):
    user_id = message.from_user.id
    async with aiosqlite.connect(DB.DB_MAIN) as db:
        await DB.enable_foreign_keys(db)
        cursor = await db.execute(" SELECT id, name FROM categories WHERE user_id = ?", (user_id,))
        rows = await cursor.fetchall()
    for category_id, name in rows:
        await message.answer(f'{category_id}: {name}')
@router.message(F.text == 'Очистити список категорій')
@router.message(Command("clear"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    await DB.del_categories(user_id)
    await message.answer("Ваш список очищенно")