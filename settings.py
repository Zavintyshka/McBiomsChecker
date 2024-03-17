# DB
DB_NAME = 'mc_bioms_checker'
DB_ADMIN_TABLE_NAME = 'mc_bioms'
DB_USER_TABLE_NAME = 'users'
DB_USER_MAP_TABLE_NAME = 'users_map'
ADVANCEMENTS_FILE_NAME = 'bioms_for_'

# Logging
ADMIN_LOGGER_FILE_NAME = 'AdminLogs.log'
USER_LOGGER_FILE_NAME = 'UserLogs.log'
BOT_LOGGER_FILE_NAME = 'BotLogs.log'
DB_LOGGER_FILE_NAME = 'dbLogs.log'
FILE_LOGGER_FILE_AME = 'FileLogs.log'

# PATHS
BASE_DIR = 'files/'
PATH_TO_TRANSLATE = 'translation/'
DB_PATH = BASE_DIR + DB_NAME
PATH_TO_MC_BIOMS = BASE_DIR + 'game_bioms/'
PATH_TO_PLAYERS_PROGRESS = BASE_DIR + 'player_maps/'
PATH_TO_LOGS = BASE_DIR + 'logs/'
PATH_TO_TEMP_FILES = BASE_DIR + 'temp/'

# MISC
ENV_FILE = BASE_DIR + '.env'
DEFAULT_LANGUAGE = 'EN'
DEBUG = True  # Debug mode for additional logs with INFO logging level

# put admins tg id here.
ADMIN_ID_SET: tuple[str] = {}
