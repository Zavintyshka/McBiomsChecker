import logging
from settings import *


def debug(setLevel_func):
    if DEBUG:
        setLevel_func(logging.DEBUG)
    else:
        setLevel_func(logging.INFO)


# loggers
admin_logger = logging.getLogger('admin_logger')
user_logger = logging.getLogger('user_logger')
bot_logger = logging.getLogger('bot_logger')
db_logger = logging.getLogger('db_logger')
file_logger = logging.getLogger('file_logger')

# handlers
file_handler_admin = logging.FileHandler(PATH_TO_LOGS + ADMIN_LOGGER_FILE_NAME)
file_handler_user = logging.FileHandler(PATH_TO_LOGS + USER_LOGGER_FILE_NAME)
file_handler_bot = logging.FileHandler(PATH_TO_LOGS + BOT_LOGGER_FILE_NAME)
file_handler_db = logging.FileHandler(PATH_TO_LOGS + DB_LOGGER_FILE_NAME)
file_handler_file = logging.FileHandler(PATH_TO_LOGS + FILE_LOGGER_FILE_AME)
console_handler = logging.StreamHandler()

if DEBUG:
    console_handler.setLevel(logging.DEBUG)
else:
    console_handler.setLevel(logging.WARNING)

# formatter and its set
formatter = logging.Formatter(f'%(name)s [%(levelname)s] -- %(asctime)s -- %(message)s', '%d-%m-%Y %H:%M:%S')

file_handler_admin.setFormatter(formatter)
file_handler_user.setFormatter(formatter)
file_handler_bot.setFormatter(formatter)
file_handler_db.setFormatter(formatter)
file_handler_file.setFormatter(formatter)
console_handler.setFormatter(formatter)

# setup admin_loger
admin_logger.addHandler(file_handler_admin)
admin_logger.addHandler(console_handler)
debug(admin_logger.setLevel)

# setup user_loger
user_logger.addHandler(file_handler_user)
user_logger.addHandler(console_handler)
debug(user_logger.setLevel)

# setup bot_loger
bot_logger.addHandler(file_handler_bot)
bot_logger.addHandler(console_handler)
debug(bot_logger.setLevel)

# setup db_loger
db_logger.addHandler(file_handler_db)
db_logger.addHandler(console_handler)
debug(db_logger.setLevel)

# setup file_logger
file_logger.addHandler(file_handler_file)
file_logger.addHandler(console_handler)
debug(file_logger.setLevel)
