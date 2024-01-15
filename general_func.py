import json
from os import remove
from aiogram.utils.formatting import Bold, as_list, as_marked_section
from settings import *
from logger import file_logger


def make_bioms_list(game_version_or_uuid: str):
    """Декоратор, позволяющий создать json-файл на основе списка биомов.
В качестве аргументов принимает версию игры и файл, куда нужно сохранить список."""

    def outer_decor(func):
        def inner_decor(*args, **kwargs):
            if len(game_version_or_uuid) == 36:
                path = PATH_TO_PLAYERS_PROGRESS + game_version_or_uuid + '.json'
            else:
                path = PATH_TO_MC_BIOMS + ADVANCEMENTS_FILE_NAME + game_version_or_uuid + '.json'
            with open(path, 'w') as file:
                bioms_list = func(*args, **kwargs)
                bioms_dict = {'biom_names': bioms_list}
                json.dump(bioms_dict, file, indent=4)
            file_logger.info(f'Создан файл эталона по пути {path}')

        return inner_decor

    return outer_decor


# General Parts
def get_bioms_list(advancement_file_path: str):
    """Функция, которая создает список биомов на основе переданного json-файла"""
    with open(advancement_file_path, 'r') as advancements:
        bioms_row = json.load(advancements)['minecraft:adventure/adventuring_time']['criteria'].keys()
        bioms_list = [biom[10:] for biom in bioms_row]
    remove(advancement_file_path)
    return bioms_list


def load_bioms_list(bioms_list_file_path: str) -> set:
    """Функция, которая загружает и создает множество из списка биомов.
Принимает json-файл, содержащий список биомов."""
    with open(bioms_list_file_path, 'r') as file:
        return set(json.load(file)['biom_names'])


def generate_content(explored: set, unexplored: set) -> as_list:
    percent = (len(explored) / (len(explored) + len(unexplored))) * 100
    progress_bar = '🟩' * int(percent / 10) + '🟥' * (10 - int(percent / 10)) + f' {percent:.1f}%'
    content = as_list(
        as_marked_section(
            Bold('Общий прогресс:\n'),
            f"Количество найденных биомов - {len(explored)}",
            f"Количество ненайденных биомов - {len(unexplored)}",
            progress_bar,
            marker='🔹'
        ),
        as_marked_section(
            Bold('Найденные биомы:\n'),
            *explored,
            marker='✅'
        ),
        as_marked_section(
            Bold('Ненайденные биомы:\n'),
            *unexplored,
            marker='❌'
        ),
        sep='\n\n'
    )
    return content


def delete_player_map(map_uuid: str):
    remove(PATH_TO_PLAYERS_PROGRESS + map_uuid + '.json')


def delete_file(path_to_file: str):
    remove(path_to_file)


def main():
    pass


if __name__ == '__main__':
    main()
