from os import getenv
from settings import ENV_FILE
from aiogram import Bot

bot = Bot(token=getenv('TELEGRAM_TOKEN'), parse_mode='HTML')
