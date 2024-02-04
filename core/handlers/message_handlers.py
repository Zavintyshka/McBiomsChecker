from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from db_funcs import maps_db, admin_db, user_db
from keyboardbuilder import make_reg_inline_keyboard, make_map_list_keyboard, make_advancement_list_keyboard, \
    first_map_keyboard
from logger import db_logger

__all__ = ['registrate_message_handlers']


async def new_user(msg: Message):
    tg_id = msg.from_user.id
    if user_db.is_user_exists(tg_id):
        await msg.answer('Вы уже авторизованы. If know want to change language use /change_language command.')
    else:
        await msg.answer(
            'Привет, я бот, который поможет тебе выполнить достижение adventuring time.')
        await msg.answer_animation('CgACAgIAAxkBAAIEImWlDVVMAc7p_YX5YuESYKSRwWB_AAK9QAACEzooSVjNCvuQxg3JNAQ')
        builder = make_reg_inline_keyboard()
        await msg.answer('Выберете язык', reply_markup=builder.as_markup())


async def help_command(msg: Message):
    message = r"""Бот позволяет отслеживать ваш прогресс выполнения достижения <b>Adventuring Time</b>
Для начала найдите вашу карту на компьютере.
Стандартные пути
🪟Windows: C:\Users\*Имя_учетной_записи*\Appdata\Roaming\.minecraft\saves
🍎macOS: /Users/*Имя_учетной_записи*/Library/Application Support/minecraft/saves
Затем в папке saves вы увидете папку advancements, которая содержит json-файл с вашей информацией.
Этот файл необходимо скинуть боту при выполнении команды /add_map
После этого вы сможете узнать какие биомы вам нужно найти, а какие вы уже нашли 😃.
    """
    await msg.answer(message)


async def map_list(msg: Message):
    tg_id = msg.from_user.id
    response = maps_db.get_map_list(tg_id)
    db_logger.info(f'Receiving map list for user: id ={tg_id}')

    if not response:
        builder = first_map_keyboard()
        await msg.answer('Похоже у вас еще нет добавленных карт 😜.\nСамое время добавить их.',
                         reply_markup=builder.as_markup())
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
    if admin_db.is_admin(msg.from_user.id):
        records = admin_db.get_all_records()
        builder = make_advancement_list_keyboard(records)
        # TODO сделать обработку
        await msg.answer('Выберете версию игры, эталонный файл которой будет удален', reply_markup=builder.as_markup())
    else:
        await msg.answer('Вы не являетесь администратором, чтобы пользоваться этой функцией.')


translate = {'RU': "Это эхо функция", 'EN': "It's an echo function"}


async def echo_func(msg: Message, some_list: list[int]):
    some_list.append(1)
    await msg.answer(str(some_list))


async def change_language(msg: Message):
    builder = make_reg_inline_keyboard()
    await msg.answer('Choose language', reply_markup=builder.as_markup())


def registrate_message_handlers(dp: Dispatcher):
    dp.message.register(new_user, Command(commands='start'))
    dp.message.register(change_language, Command(commands='change_language'))
    dp.message.register(echo_func, Command(commands='black'))
    dp.message.register(help_command, Command(commands='help'))
    dp.message.register(map_list, Command(commands='map_list'))
    dp.message.register(delete_map_menu, Command(commands=['delete_map', 'del_map']))
    dp.message.register(delete_advancement, Command(commands=['delete_advancement', 'del_advancement']))
