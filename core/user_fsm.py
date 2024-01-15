from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from aiogram import Dispatcher
from db_funcs import user_db, maps_db
from check_conditions import is_user_exist
from settings import PATH_TO_TEMP_FILES
from bot_initialize import bot
from keyboardbuilder import make_cancel_button


# add_map
class AddMap(StatesGroup):
    map_name = State()
    map_version = State()
    json_file = State()


async def add_map(msg: Message, state: FSMContext):
    tg_id = msg.from_user.id
    builder = make_cancel_button()
    if is_user_exist(tg_id):
        await msg.answer('Введите название вашей карты', reply_markup=builder.as_markup())
        await state.set_state(AddMap.map_name)
    else:
        await msg.answer('У вас нет личного кабинета. Используйте команду /create_user, чтобы создать личный кабинет.')


async def map_version(msg: Message, state: FSMContext):
    await state.update_data(map_name=msg.text)
    builder = make_cancel_button()
    await msg.answer('Введите версию игры', reply_markup=builder.as_markup())
    await state.set_state(AddMap.map_version)


async def json_file(msg: Message, state: FSMContext):
    builder = make_cancel_button()
    await state.update_data(map_version=msg.text)
    await msg.answer('Загрузите json_file вашей карты', reply_markup=builder.as_markup())
    await state.set_state(AddMap.json_file)


async def end_add_map(msg: Message, state: FSMContext):
    await state.update_data(json_file=msg.document.file_id)
    map_data = await state.get_data()
    tg_id = msg.from_user.id

    _map_name = map_data['map_name']
    _map_version = map_data['map_version']
    _user_uuid = user_db.get_user_uuid(tg_id)
    _json_file = map_data['json_file']
    path = PATH_TO_TEMP_FILES + 'temp1.json'
    await bot.download(_json_file, path)
    maps_db.add_map(_map_name, _map_version, _user_uuid, path)
    await msg.answer('Карта была добавлена в ваш личный кабинет')
    await state.clear()


def register_fsm_handlers(dp: Dispatcher):
    dp.message.register(add_map, StateFilter(None), Command(commands='add_map'))
    dp.message.register(map_version, StateFilter(AddMap.map_name))
    dp.message.register(json_file, StateFilter(AddMap.map_version))
    dp.message.register(end_add_map, StateFilter(AddMap.json_file))
