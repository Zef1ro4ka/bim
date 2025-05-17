from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
InlineKeyboardButton, InlineKeyboardMarkup)
import aiosqlite
from app.database.database import DB_MAIN

def main_kb():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Додати витрату'),
         KeyboardButton(text='Статистика')],
        [KeyboardButton(text='Очистити список')]
        ],resize_keyboard = True)
    

def statistic_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='За сьогодні', callback_data='today')],
        [InlineKeyboardButton(text='За місяць', callback_data='month')],
        [InlineKeyboardButton(text='Категорії витрат', callback_data='categories')]
    ])

def categories_kb():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Додати категорію'),
        KeyboardButton(text='Змінити категорію')],
        [KeyboardButton(text='Очистити список категорій'),
        KeyboardButton(text='Список категорій')]
        ],resize_keyboard = True)


async def edit_catigories_kb(user_id):
    buttons = []
    async with aiosqlite.connect(DB_MAIN) as db:
        cursor = await db.execute("SELECT id, name FROM categories WHERE user_id = ?", (user_id,))
        categories = await cursor.fetchall()

    for cat_id, name in categories:
        btn =  InlineKeyboardButton(text=name, callback_data=f'edit_category:{cat_id}')
        buttons.append([btn])
    return InlineKeyboardMarkup(inline_keyboard=buttons)