import os
from json import dump, load
from aiogram.utils.formatting import Bold, as_list, as_marked_section
from settings import *
from logger import file_logger
from core.types import AvailableLanguages
from locale import get_locale
from core.types import InfoMessage


def make_bioms_list(game_version_or_uuid: str):
    """Декоратор, позволяющий создать json-файл на основе списка биомов.
    В качестве аргументов принимает версию игры и файл, куда нужно сохранить список."""

    def outer_decor(func):
        def inner_decor(*args, **kwargs):
            if len(game_version_or_uuid) == 36:
                path = PATH_TO_PLAYERS_PROGRESS + game_version_or_uuid + '.json'
            else:
                path = PATH_TO_MC_BIOMS + ADVANCEMENTS_FILE_NAME + game_version_or_uuid + '.json'
                if is_file_exists(path):
                    raise FileExistsError
            with open(path, 'w') as file:
                bioms_list = func(*args, **kwargs)
                bioms_dict = {'biom_names': bioms_list}
                dump(bioms_dict, file, indent=4)
            file_logger.info(f'The file has been created in path: {path}')

        return inner_decor

    return outer_decor


def get_bioms_list(advancement_file_path: str):
    """Функция, которая создает список биомов на основе переданного json-файла"""
    with open(advancement_file_path, 'r') as advancements:
        bioms_row = load(advancements)['minecraft:adventure/adventuring_time']['criteria'].keys()
        bioms_list = [biom[MOD:] for biom in bioms_row]
    delete_file(advancement_file_path)
    return bioms_list


def load_bioms_list(bioms_list_file_path: str) -> set:
    """Функция, которая загружает и создает множество из списка биомов.
Принимает json-файл, содержащий список биомов."""
    with open(bioms_list_file_path, 'r') as file:
        json_file = load(file)
        return set(json_file['biom_names'])


def generate_content(explored: set, unexplored: set, language: AvailableLanguages) -> as_list:
    """Generates a content for "map_list" bot function """

    percent = (len(explored) / (len(explored) + len(unexplored))) * 100
    progress_bar = '🟩' * int(percent / 10) + '🟥' * (10 - int(percent / 10)) + f' {percent:.1f}%'
    content = as_list(
        as_marked_section(
            Bold(get_locale(InfoMessage.GENERAL_PROGRESS, language)),
            get_locale(InfoMessage.QTY_EXPLORED_BIOMS, language).format(explored_bioms=len(explored)),
            get_locale(InfoMessage.QTY_UNEXPLORED_BIOM, language).format(unexplored_bioms=len(unexplored)),
            progress_bar,
            marker='🔹'
        ),
        as_marked_section(
            Bold(get_locale(InfoMessage.EXPLORED_BIOMS, language)),
            *explored,
            marker='✅'
        ),
        as_marked_section(
            Bold(get_locale(InfoMessage.UNEXPLORED_BIOM, language)),
            *unexplored,
            marker='❌'
        ),
        sep='\n\n'
    )
    return content


def delete_file(path: str):
    os.remove(path)
    file_logger.info(f"The file in path: {path=} has been deleted")


def is_file_exists(file_path: str):
    return os.path.exists(file_path)


def main():
    pass


if __name__ == '__main__':
    main()
