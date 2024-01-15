from aiogram import Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from logger import user_logger
from db_funcs import maps_db, admin_db
from keyboardbuilder import make_reg_inline_keyboard, make_map_list_keyboard, make_advancement_list_keyboard
from check_conditions import is_user_exist, is_admin


async def create_user(msg: Message):
    tg_id = msg.from_user.id
    if is_user_exist(tg_id):
        await msg.answer(f'Ваш {tg_id} уже зарегистрирован')
    else:
        builder = make_reg_inline_keyboard()
        await msg.answer('Выберете язык', reply_markup=builder.as_markup())


async def map_list(msg: Message):
    tg_id = msg.from_user.id
    response = maps_db.get_map_list(tg_id)
    if not response:
        await msg.answer('Похоже у вас еще нет добавленных карт 😜.\nСамое время добавить их с помощью команды /add_map')
    else:
        builder = make_map_list_keyboard(response, 'map-list')
        await msg.answer('Ваш список карт:', reply_markup=builder.as_markup())


async def delete_map_menu(msg: Message):
    tg_id = msg.from_user.id
    maps = maps_db.get_map_list(tg_id)
    if maps:
        builder = make_map_list_keyboard(maps, 'delete-map')
        await msg.answer('Выберете карту для удаления', reply_markup=builder.as_markup())
    else:
        await msg.answer('Похоже у вас еще нет карт для удаления.')



async def delete_advancement(msg: Message):
    if is_admin(msg.from_user.id):
        records = admin_db.get_all_records()
        builder = make_advancement_list_keyboard(records)
        await msg.answer('Выберете версию игры, эталонный файл которой будет удален', reply_markup=builder.as_markup())
    else:
        await msg.answer('Вы не являетесь администратором, чтобы пользоваться этой функцией.')


async def new_user(msg: Message):
    await msg.answer('Привет, я бот, который поможет тебе выполнить достижение adventuring time')
    await msg.answer_animation('CgACAgIAAxkBAAIEImWlDVVMAc7p_YX5YuESYKSRwWB_AAK9QAACEzooSVjNCvuQxg3JNAQ')


def register_handlers(dp: Dispatcher):
    dp.message.register(create_user, Command(commands='create_user'))
    dp.message.register(map_list, Command(commands='map_list'))
    dp.message.register(delete_map_menu, Command(commands='delete_map'))
    dp.message.register(delete_advancement, Command(commands=['delete_advancement', 'del_advancement']))
    dp.message.register(new_user, CommandStart)
