from settings import PATH_TO_TRANSLATE
from core.types import *
from json import load


def get_locale(message: MessageHandlersAnswers | CallbackQueriesAnswers
               , language: AvailableLanguages) -> str:
    """Returns localized text"""
    translate_file_path = PATH_TO_TRANSLATE + language.value + '.json'
    with open(translate_file_path, 'r') as file:
        translation = load(file)
        text = translation[message.value]
        return text


if __name__ == '__main__':
    print(get_locale(MessageHandlersAnswers.SELECT_MAP_FOR_DELETING, AvailableLanguages.RU))


