from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable

from redis import Redis
from db_funcs import user_db
from core.types import *

redis_client = Redis(host='localhost', port=6379)


class LanguageMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.language_from_tg: str | None = None
        self.language: str | None = None
        self.tg_id: str | None = None

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]) -> Any:

        self.tg_id = event.from_user.id
        self.language_from_tg = event.from_user.language_code

        redis_response: bytes | None = redis_client.get(name=f'tg_id:{self.tg_id}')

        if redis_response:
            self.language: str = redis_response.decode()
            print("Язык из памяти")
        else:
            user_language: AvailableLanguages | None = user_db.get_user_language(self.tg_id)
            await self.record_to_redis(user_language)

        data['language'] = self.language
        return await handler(event, data)

    async def record_to_redis(self, user_language: AvailableLanguages | None) -> None:
        """Makes record in redis storage and changes language of middleware instance"""
        self.language = user_language.value if isinstance(user_language,
                                                          AvailableLanguages) else self.language_from_tg.upper()

        redis_record = redis_client.set(name=f'tg_id:{self.tg_id}', value=self.language)
        print(f'tg_id={self.tg_id} -- {self.language}')
