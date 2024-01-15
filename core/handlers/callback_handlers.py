from aiogram import Dispatcher, F
from aiogram.types import CallbackQuery
from logger import db_logger, file_logger
from db_funcs import user_db, maps_db, admin_db
from general_func import load_bioms_list, delete_file
from settings import *
from keyboardbuilder import make_back_btn, make_map_list_keyboard
from general_func import generate_content, delete_player_map
from aiogram.fsm.context import FSMContext


async def language_buttons(callback: CallbackQuery):
    _, language = callback.data.split('_')
    tg_id = str(callback.from_user.id)
    user_db.create_user(tg_id, language, tg_id in ADMIN_ID_SET)
    await callback.message.delete()
    await callback.message.answer('Ваша учетная запись успешна добавлена на сервер')


async def info_about_maps_buttons(callback: CallbackQuery):
    _, map_uuid, map_version = callback.data.split('_')
    builder = make_back_btn()
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
    await callback.answer(f'будем удалять карту с {map_uuid=}')

    maps_db.delete_map(map_uuid)
    delete_player_map(map_uuid)

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
    file_logger.info(f'Удален файл эталона по пути file {path}')
    admin_db.del_data(game_version)
    db_logger.info(f'Удален из БД эталон версии {game_version} администратором с id={callback.from_user.id}')
    await callback.message.delete()
    await callback.message.answer(f'Эталонный файл {file} был удален')


async def reset_fsm_button(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.answer('Действие отменено')


def register_callback_handlers(dp: Dispatcher):
    dp.callback_query.register(language_buttons, F.data.contains('language'))
    dp.callback_query.register(info_about_maps_buttons, F.data.contains('map-list'))
    dp.callback_query.register(delete_map_buttons, F.data.contains('delete-map'))
    dp.callback_query.register(delete_record_buttons, F.data.contains('del-advancement'))
    dp.callback_query.register(back_to_map_list, F.data == 'back_to_menu')
    dp.callback_query.register(reset_fsm_button, F.data == 'cancel')
