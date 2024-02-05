import sqlite3
from uuid import uuid4
from aiogram import Dispatcher
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from db_funcs import admin_db
from settings import *
from bot_initialize import bot
from general_funcs import get_bioms_list, make_bioms_list
from logger import db_logger
from keyboardbuilder import make_cancel_button
from core.types import AvailableLanguages, MessageHandlersAnswers, UserFSMLocalization, AdminFSMLocalization
from locale import get_locale

__all__ = ['registrate_admin_fsm_handlers']


class AddAdvancement(StatesGroup):
    game_version = State()
    json_file_id = State()


async def add_advancement(msg: Message, state: FSMContext, language: AvailableLanguages):
    if admin_db.is_admin(msg.from_user.id):
        builder = make_cancel_button(language)
        text = get_locale(UserFSMLocalization.INPUT_MAP_VERSION, language)
        await msg.answer(text, reply_markup=builder.as_markup())
        await state.set_state(AddAdvancement.game_version)
    else:
        text = get_locale(MessageHandlersAnswers.YOURE_NOT_AN_ADMIN, language)
        await msg.answer(text)


async def receive_json_file(msg: Message, state: FSMContext, language: AvailableLanguages):
    await state.update_data(game_version=msg.text)
    builder = make_cancel_button(language)
    text = get_locale(AdminFSMLocalization.INPUT_STANDARD_JSON, language)
    await msg.answer(text, reply_markup=builder.as_markup())
    await state.set_state(AddAdvancement.json_file_id)


async def end_add_advancement(msg: Message, state: FSMContext, language: AvailableLanguages):
    file_id = msg.document.file_id
    await state.update_data(json_file_id=file_id)
    map_data = await state.get_data()
    _game_version = map_data['game_version']
    _file_id = map_data['json_file_id']
    path = PATH_TO_TEMP_FILES + f'{uuid4()}.json'
    await bot.download(_file_id, path)
    try:
        make_bioms_list(_game_version)(get_bioms_list)(path)
        await admin_db.create_game_record(_game_version, ADVANCEMENTS_FILE_NAME + _game_version + '.json')
    except (sqlite3.IntegrityError, FileExistsError):
        text = get_locale(AdminFSMLocalization.STANDARD_FILE_ALREADY_EXISTS, language)
        await msg.answer(text.format(_game_version=_game_version))
    else:
        db_logger.info(f'The standard record {_game_version=} has been added by admin id={msg.from_user.id}')
        text = get_locale(AdminFSMLocalization.STANDARD_FILE_SUCCESSFULLY_ADDED, language)
        await msg.answer(text.format(_game_version=_game_version))
    finally:
        await state.clear()


def registrate_admin_fsm_handlers(dp: Dispatcher):
    dp.message.register(add_advancement, StateFilter(None), Command(commands='add_advancement'))
    dp.message.register(receive_json_file, StateFilter(AddAdvancement.game_version))
    dp.message.register(end_add_advancement, StateFilter(AddAdvancement.json_file_id))
