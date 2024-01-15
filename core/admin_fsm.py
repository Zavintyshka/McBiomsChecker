from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from aiogram import Dispatcher
from db_funcs import admin_db
from check_conditions import is_admin
from settings import *
from bot_initialize import bot
from uuid import uuid4
from general_func import get_bioms_list, make_bioms_list
from logger import db_logger
from keyboardbuilder import make_cancel_button


class AddAdvancement(StatesGroup):
    game_version = State()
    json_file_id = State()


async def add_advancement(msg: Message, state: FSMContext):
    if is_admin(msg.from_user.id):
        builder = make_cancel_button()
        await msg.answer('Введите версию игры', reply_markup=builder.as_markup())
        await state.set_state(AddAdvancement.game_version)
    else:
        await msg.answer('Вы не являетесь администратором, чтобы пользоваться этой функцией.')


async def receive_json_file(msg: Message, state: FSMContext):
    await state.update_data(game_version=msg.text)
    builder = make_cancel_button()
    await msg.answer('Загрузите эталонный json-файл', reply_markup=builder.as_markup())
    await state.set_state(AddAdvancement.json_file_id)


async def end_add_advancement(msg: Message, state: FSMContext):
    file_id = msg.document.file_id
    await state.update_data(json_file_id=file_id)
    map_data = await state.get_data()
    _game_version = map_data['game_version']
    _file_id = map_data['json_file_id']
    path = PATH_TO_TEMP_FILES + f'{uuid4()}.json'
    await bot.download(_file_id, path)
    make_bioms_list(_game_version)(get_bioms_list)(path)

    admin_db.create_game_record(_game_version, ADVANCEMENTS_FILE_NAME + _game_version + '.json')
    db_logger.info(f'Добавлен в БД эталон версии {_game_version} администратором c id={msg.from_user.id}')
    await msg.answer(f'Карта с версией {_game_version} была добавлена в архив версий')

    await state.clear()


def registrate_admin_fsm_handlers(dp: Dispatcher):
    dp.message.register(add_advancement, StateFilter(None), Command(commands='add_advancement'))
    dp.message.register(receive_json_file, StateFilter(AddAdvancement.game_version))
    dp.message.register(end_add_advancement, StateFilter(AddAdvancement.json_file_id))
