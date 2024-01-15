from os import getenv
from dotenv import load_dotenv
from settings import ENV_PATH
from aiogram import Bot

load_dotenv(ENV_PATH)
bot = Bot(token=getenv('TOKEN'))