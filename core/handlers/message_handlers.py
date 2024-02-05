from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from db_funcs import maps_db, admin_db, user_db
from keyboardbuilder import make_reg_inline_keyboard, make_map_list_keyboard, make_advancement_list_keyboard, \
    first_map_keyboard
from logger import db_logger
from locale import get_locale
from core.types import AvailableLanguages, MessageHandlersAnswers

__all__ = ['registrate_message_handlers']


async def new_user(msg: Message, language: AvailableLanguages):
    tg_id = msg.from_user.id
    if user_db.is_user_exists(tg_id):
        answer = get_locale(MessageHandlersAnswers.ALREADY_AUTHORIZED, language)
        await msg.answer(answer)
    else:
        answer = get_locale(MessageHandlersAnswers.GREETINGS_MSG, language)
        await msg.answer(answer)
        await msg.answer_animation('CgACAgIAAxkBAAIEImWlDVVMAc7p_YX5YuESYKSRwWB_AAK9QAACEzooSVjNCvuQxg3JNAQ')
        builder = make_reg_inline_keyboard()
        answer = get_locale(MessageHandlersAnswers.SELECT_LANGUAGE, language)
        await msg.answer(answer, reply_markup=builder.as_markup())


async def help_command(msg: Message, language: AvailableLanguages):
    answer = get_locale(MessageHandlersAnswers.HELP_MSG, language)
    await msg.answer(answer)


async def map_list(msg: Message, language: AvailableLanguages):
    tg_id = msg.from_user.id
    response = maps_db.get_map_list(tg_id)
    db_logger.info(f'Receiving map list for user: id ={tg_id}')

    if not response:
        builder = first_map_keyboard(language)
        answer = get_locale(MessageHandlersAnswers.NO_MAP_LETS_ADD_MSG, language)
        await msg.answer(answer, reply_markup=builder.as_markup())
    else:
        builder = make_map_list_keyboard(response, 'map-list')
        answer = get_locale(MessageHandlersAnswers.YOUR_MAP_LIST, language)
        await msg.answer(answer, reply_markup=builder.as_markup())


async def delete_map_menu(msg: Message, language: AvailableLanguages):
    tg_id = msg.from_user.id
    maps = maps_db.get_map_list(tg_id)
    if maps:
        builder = make_map_list_keyboard(maps, 'delete-map')
        answer = get_locale(MessageHandlersAnswers.SELECT_MAP_FOR_DELETING, language)
        await msg.answer(answer, reply_markup=builder.as_markup())
    else:
        answer = get_locale(MessageHandlersAnswers.NO_MAP_FOR_DELETING, language)
        await msg.answer(answer)


async def delete_advancement(msg: Message, language: AvailableLanguages):
    if admin_db.is_admin(msg.from_user.id):
        records = admin_db.get_all_records()
        builder = make_advancement_list_keyboard(records)
        answer = get_locale(MessageHandlersAnswers.SELECT_STANDARD_MAP_FOR_DELETING, language)
        await msg.answer(answer, reply_markup=builder.as_markup())
    else:
        answer = get_locale(MessageHandlersAnswers.YOURE_NOT_AN_ADMIN, language)
        await msg.answer(answer)


async def change_language(msg: Message, language: AvailableLanguages):
    builder = make_reg_inline_keyboard()
    answer: str = get_locale(MessageHandlersAnswers.CHANGE_LANGUAGE_MSG, language)
    await msg.answer(answer, reply_markup=builder.as_markup())


def registrate_message_handlers(dp: Dispatcher):
    dp.message.register(new_user, Command(commands='start'))
    dp.message.register(change_language, Command(commands='change_language'))
    dp.message.register(help_command, Command(commands='help'))
    dp.message.register(map_list, Command(commands='map_list'))
    dp.message.register(delete_map_menu, Command(commands=['delete_map', 'del_map']))
    dp.message.register(delete_advancement, Command(commands=['delete_advancement', 'del_advancement']))
