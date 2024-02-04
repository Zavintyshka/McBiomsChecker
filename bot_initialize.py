from os import getenv
from dotenv import load_dotenv
from settings import ENV_FILE
from aiogram import Bot

load_dotenv(ENV_FILE)
bot = Bot(token=getenv('TOKEN'), parse_mode='HTML')
