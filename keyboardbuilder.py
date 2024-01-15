from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from db_funcs import maps_db


def make_reg_inline_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    ru_button = InlineKeyboardButton(text='🇷🇺RU', callback_data='language_RU')
    en_button = InlineKeyboardButton(text='🇺🇸EN', callback_data='language_EN')
    builder.row(ru_button, en_button)
    return builder


def make_map_list_keyboard(map_list: maps_db.get_map_list, inline_tag: str) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    for index in range(0, len(map_list), 2):
        fst_map_name, fst_uuid, fst_version = map_list[index][0], map_list[index][1], map_list[index][2]
        fst_btn = InlineKeyboardButton(text='🗺️ ' + fst_map_name + ' ➡️',
                                       callback_data=f'{inline_tag}_{fst_uuid}_{fst_version}')
        try:
            snd_map_name, snd_uuid, snd_version = map_list[index + 1][0], map_list[index + 1][1], map_list[index + 1][2]
            snd_btn = InlineKeyboardButton(text='🗺️' + snd_map_name,
                                           callback_data=f'{inline_tag}_{snd_uuid}_{snd_version}')
        except IndexError:
            builder.row(fst_btn)
            return builder
        builder.row(fst_btn, snd_btn)
    return builder


def make_advancement_list_keyboard(advancement_list: list[tuple]) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for index in range(0, len(advancement_list), 2):
        fst_game_version, fst_file = advancement_list[index][0], advancement_list[index][1]
        fst_btn = InlineKeyboardButton(text=fst_game_version,
                                       callback_data=f'del-advancement+{fst_game_version}+{fst_file}')
        try:
            snd_game_version, snd_file = advancement_list[index + 1][0], advancement_list[index + 1][1]
            snd_btn = InlineKeyboardButton(text=snd_game_version,
                                           callback_data=f'del-advancement+{snd_game_version}+{snd_file}')
        except IndexError:
            builder.row(fst_btn)
            return builder
        builder.row(fst_btn, snd_btn)
    return builder


def make_back_btn() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    btn = InlineKeyboardButton(text='🔁назад в меню🔁', callback_data='back_to_menu')
    builder.add(btn)
    return builder


def make_cancel_button() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    cancel_btn = InlineKeyboardButton(text='🚫Отменить действие', callback_data='cancel')
    builder.add(cancel_btn)
    return builder
