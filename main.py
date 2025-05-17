from aiogram import Dispatcher, Bot
import asyncio
from app.disp import router
from app.database.logging_midleware import LoggingMidleWare


async def main():
    bot = Bot(token='7415615009:AAEjrRdXip_f3GLUmtEg4--cZjjvK3qtQ5Q')
    dp = Dispatcher()
    dp.include_router(router)
    dp.message.middleware(LoggingMidleWare())
    dp.callback_query.middleware(LoggingMidleWare())
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        print("Work is start")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Work is end")