import logging
import datetime
from settings import PATH_TO_LOGS

# loggers
admin_logger = logging.getLogger('admin_logger')
user_logger = logging.getLogger('user_logger')
bot_logger = logging.getLogger('bot_logger')
db_logger = logging.getLogger('db_logger')
file_logger = logging.getLogger('file_logger')

# handlers
file_handler_admin = logging.FileHandler(PATH_TO_LOGS + 'AdminLogs.log')
file_handler_user = logging.FileHandler(PATH_TO_LOGS + 'UserLogs.log')
file_handler_bot = logging.FileHandler(PATH_TO_LOGS + 'BotLogs.log')
file_handler_db = logging.FileHandler(PATH_TO_LOGS + 'dbLogs.log')
file_handler_file = logging.FileHandler(PATH_TO_LOGS + 'FileLogs.log')
console_handler = logging.StreamHandler()

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
admin_logger.setLevel(logging.INFO)

# setup user_loger
user_logger.addHandler(file_handler_user)
user_logger.addHandler(console_handler)
user_logger.setLevel(logging.INFO)

# setup bot_loger
bot_logger.addHandler(file_handler_bot)
bot_logger.addHandler(console_handler)
bot_logger.setLevel(logging.DEBUG)

# setup db_loger
db_logger.addHandler(file_handler_db)
db_logger.addHandler(console_handler)
db_logger.setLevel(logging.INFO)

# setup file_logger
file_logger.addHandler(file_handler_file)
file_logger.addHandler(console_handler)
file_logger.setLevel(logging.INFO)
