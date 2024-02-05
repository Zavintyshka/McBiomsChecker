from aiogram import Dispatcher, F
from aiogram.types import CallbackQuery
from logger import db_logger, file_logger
from db_funcs import user_db, maps_db, admin_db
from settings import *
from keyboardbuilder import back_keyboard, make_map_list_keyboard
from general_funcs import load_bioms_list, generate_content, delete_file
from aiogram.fsm.context import FSMContext
from core.fsm import *

from core.in_memory_store import redis_client
from core.types import *
from locale import get_locale

__all__ = ['registrate_callback_handlers']


async def language_buttons(callback: CallbackQuery):
    tg_id = str(callback.from_user.id)
    _, language = callback.data.split('_')
    redis_client.set(name=f'tg_id:{tg_id}', value=language)

    if user_db.is_user_exists(tg_id):
        user_db.change_language(tg_id, language)
        answer = get_locale(MessageAnswers.CHOSEN_LANGUAGE, AvailableLanguages(language))
        await callback.message.delete()
        await callback.message.answer(answer.format(language=language))
    else:
        user_db.create_user(tg_id, language, tg_id in ADMIN_ID_SET)
        await callback.message.delete()
        answer = get_locale(MessageAnswers.CHOSEN_LANGUAGE_HINT, AvailableLanguages(language))
        await callback.message.answer(answer)


async def info_about_maps_buttons(callback: CallbackQuery):
    _, map_uuid, map_version = callback.data.split('_')
    builder = back_keyboard()
    try:
        game_data = load_bioms_list(PATH_TO_MC_BIOMS + admin_db.get_game_file_path(map_version))
    except IndexError:
        await callback.message.answer(f"К сожалению, в нашей базе данных нет Minecraft версии {map_version}")
    else:
        player_data = load_bioms_list(PATH_TO_PLAYERS_PROGRESS + map_uuid + '.json')
        explored = game_data.intersection(player_data)
        unexplored = game_data.difference(player_data)
        content = generate_content(explored, unexplored)
        await callback.message.delete()
        await callback.message.answer(**content.as_kwargs(), reply_markup=builder.as_markup())


async def delete_map_buttons(callback: CallbackQuery):
    _, map_uuid, _ = callback.data.split('_')
    maps_db.delete_map(map_uuid)
    path = PATH_TO_PLAYERS_PROGRESS + map_uuid + '.json'
    delete_file(path)
    await callback.message.delete()
    await callback.message.answer('Карта успешно удалена')


async def back_to_map_list(callback: CallbackQuery):
    tg_id = callback.from_user.id
    response = maps_db.get_map_list(tg_id)
    builder = make_map_list_keyboard(response, 'map-list')
    await callback.message.edit_text('Ваш список карт:', reply_markup=builder.as_markup())


async def delete_record_buttons(callback: CallbackQuery):
    _, game_version, file = callback.data.split('+')
    path = PATH_TO_MC_BIOMS + file
    delete_file(path)
    file_logger.info(f'The standard file in path {path} has been deleted')
    admin_db.del_data(game_version)
    db_logger.info(f'The standard record {game_version=} has been deleted by admin id={callback.from_user.id}')
    db_logger.info(f'The standard file {game_version=} has been deleted by admin id={callback.from_user.id}')
    await callback.message.delete()
    await callback.message.answer(f'Эталонный файл {file} был удален')


async def reset_fsm_button(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.answer('Действие отменено')


async def first_map_btn(callback: CallbackQuery, state: FSMContext):
    await add_map(callback, state)


def registrate_callback_handlers(dp: Dispatcher):
    dp.callback_query.register(language_buttons, F.data.contains('language'))
    dp.callback_query.register(info_about_maps_buttons, F.data.contains('map-list'))
    dp.callback_query.register(delete_map_buttons, F.data.contains('delete-map'))
    dp.callback_query.register(delete_record_buttons, F.data.contains('del-advancement'))
    dp.callback_query.register(back_to_map_list, F.data == 'back_to_menu')
    dp.callback_query.register(reset_fsm_button, F.data == 'cancel')
    dp.callback_query.register(first_map_btn, F.data == 'first_map')
