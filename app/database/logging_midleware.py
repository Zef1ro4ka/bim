from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable,Any,Dict,Awaitable

class LoggingMidleWare(BaseMiddleware):
    async def __call__(
            self,
            hendler: Callable[[Any,Dict[str,Any]], Awaitable[Any]],
            event: Any,
            data: Dict[str, Any]
    ):
        if isinstance(event, Message):
            print(f"[MESSAGE] {event.from_user.id} ({event.from_user.id}): {event.text}")
        elif isinstance(event, CallbackQuery):
            print(f"[CALLBACK] {event.from_user.id} ({event.from_user.full_name}) {event.data}")

        return await hendler(event, data)
  
