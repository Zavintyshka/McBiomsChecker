from uuid import uuid4
from aiogram import Dispatcher
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from bot_initialize import bot
from db_funcs import user_db, maps_db
from settings import PATH_TO_TEMP_FILES
from keyboardbuilder import make_cancel_button
from core.types import AvailableLanguages, UserFSMLocalization
from locale import get_locale

__all__ = ['registrate_user_fsm_handlers', 'add_map']


# add_map
class AddMap(StatesGroup):
    map_name = State()
    map_version = State()
    json_file = State()


async def add_map(msg_or_callback: Message | CallbackQuery, state: FSMContext, language: AvailableLanguages):
    builder = make_cancel_button(language)
    text = get_locale(UserFSMLocalization.INPUT_MAP_NAME, language)
    if isinstance(msg_or_callback, CallbackQuery):
        tg_id = msg_or_callback.from_user.id
        if user_db.is_user_exists(tg_id):
            await msg_or_callback.message.answer(text, reply_markup=builder.as_markup())
            await state.set_state(AddMap.map_name)

    elif isinstance(msg_or_callback, Message):
        tg_id = msg_or_callback.from_user.id
        if user_db.is_user_exists(tg_id):
            await msg_or_callback.answer(text, reply_markup=builder.as_markup())
            await state.set_state(AddMap.map_name)
        else:
            text = get_locale(UserFSMLocalization.USE_START_COMMAND_BEFORE, language)
            await msg_or_callback.answer(text)


async def map_version(msg: Message, state: FSMContext, language: AvailableLanguages):
    await state.update_data(map_name=msg.text)
    builder = make_cancel_button(language)
    text = get_locale(UserFSMLocalization.INPUT_MAP_VERSION, language)
    await msg.answer(text, reply_markup=builder.as_markup())
    await state.set_state(AddMap.map_version)


async def json_file(msg: Message, state: FSMContext, language: AvailableLanguages):
    builder = make_cancel_button(language)
    await state.update_data(map_version=msg.text)
    text = get_locale(UserFSMLocalization.INPUT_MAP_JSON, language)
    await msg.answer(text, reply_markup=builder.as_markup())
    await state.set_state(AddMap.json_file)


async def end_add_map(msg: Message, state: FSMContext, language: AvailableLanguages):
    await state.update_data(json_file=msg.document.file_id)
    map_data = await state.get_data()
    tg_id = msg.from_user.id

    _map_name = map_data['map_name']
    _map_version = map_data['map_version']
    _user_uuid = user_db.get_user_uuid(tg_id)
    _json_file = map_data['json_file']
    path = PATH_TO_TEMP_FILES + f'{str(uuid4())}.json'
    await bot.download(_json_file, path)
    maps_db.add_map(_map_name, _map_version, _user_uuid, path)
    text = get_locale(UserFSMLocalization.MAP_SUCCESSFULLY_ADDED, language)
    await msg.answer(text)
    await state.clear()


def registrate_user_fsm_handlers(dp: Dispatcher):
    dp.message.register(add_map, StateFilter(None), Command(commands='add_map'))
    dp.message.register(map_version, StateFilter(AddMap.map_name))
    dp.message.register(json_file, StateFilter(AddMap.map_version))
    dp.message.register(end_add_map, StateFilter(AddMap.json_file))
