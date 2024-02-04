import sqlite3 as sq
from uuid import uuid1
from settings import *
from general_funcs import make_bioms_list, get_bioms_list
from logger import db_logger, admin_logger

from core.types import AvailableLanguages


class DbInterface:
    """The parent class for database management"""
    __instances = []

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        cls.__instances.append(instance)
        return instance

    def __init__(self):
        if not hasattr(self.instances[0], 'base'):
            self.__base = sq.connect(DB_PATH)
        else:
            self.__base = self.instances[0].base

    def __del__(self):
        if len(self.instances) == 1:
            self.base.close()
            db_logger.info('DB closing')
        self.instances.remove(self)

    @property
    def instances(self):
        return self.__instances

    @property
    def base(self):
        return self.__base


class AdminDB(DbInterface):
    """ Child class of DbInterface that helps manage db's admin part"""

    def get_game_file_path(self, game_version: str):
        query = 'SELECT path_to_json FROM {} WHERE game_version=?'.format(DB_ADMIN_TABLE_NAME)
        data = self.base.execute(query, (game_version,)).fetchall()
        return data[0][0]

    async def create_game_record(self, game_version: str, json_path: str):
        query = 'INSERT INTO {} VALUES(?,?)'.format(DB_ADMIN_TABLE_NAME)
        self.base.execute(query, (game_version, json_path))
        self.base.commit()

    def get_all_records(self):
        query = 'SELECT * FROM {}'.format(DB_ADMIN_TABLE_NAME)
        response = self.base.execute(query).fetchall()
        return response

    def del_data(self, game_version: str):
        query = 'DELETE FROM {} WHERE game_version=?'.format(DB_ADMIN_TABLE_NAME)
        self.base.execute(query, (game_version,))
        self.base.commit()
        return f'Запись с {game_version=} успешно удалена'

    @staticmethod
    def is_admin(tg_id: str | int) -> bool:
        query = 'SELECT admin FROM {} WHERE tg_id =?'.format(DB_USER_TABLE_NAME)
        response = admin_db.base.execute(query, (str(tg_id),)).fetchall()[0][0]
        return bool(response)


class UserDB(DbInterface):
    """ Child class DbInterface that helps user interact with DB"""

    def create_user(self, tg_id, user_language: str, is_admin: bool):
        user_uuid = str(uuid1())
        query = 'INSERT INTO {} (user_uuid, tg_id, user_language, admin) VALUES (?,?,?,?)'.format(DB_USER_TABLE_NAME)
        self.base.execute(query, (user_uuid, tg_id, user_language, is_admin))
        self.base.commit()
        if is_admin:
            db_logger.info(f'The new user has been created: ({user_uuid=}, {tg_id=}, {user_language=}, {is_admin=})')
            admin_logger.warning(
                f'The new admin has been created: ({user_uuid=}, {tg_id=}, {user_language=}, {is_admin=})')
        else:
            db_logger.info(f'The new user has been created: ({user_uuid=}, {tg_id=}, {user_language=}, {is_admin=})')

    def get_user_uuid(self, tg_id: str):
        query = 'SELECT user_uuid FROM {} WHERE tg_id={}'.format(DB_USER_TABLE_NAME, tg_id)
        return self.base.execute(query).fetchall()[0][0]
        # TODO сделать обработку ^

    def get_user_language(self, tg_id: str) -> AvailableLanguages | None:
        query = 'SELECT user_language FROM {} WHERE tg_id=?'.format(DB_USER_TABLE_NAME)
        raw_response = self.base.execute(query, (tg_id,)).fetchall()
        db_logger.info(f'Get language for {tg_id}')
        if not raw_response:
            return None
        else:
            language: str = raw_response[0][0]
            return AvailableLanguages(language)

    def change_language(self, tg_id: str, language: str):
        query = 'UPDATE {} SET user_language = ? WHERE tg_id = ?'.format(DB_USER_TABLE_NAME)
        self.base.execute(query, (language, tg_id))
        self.base.commit()

    @staticmethod
    def is_user_exists(tg_id) -> bool:
        query = user_db.base.execute(
            "SELECT user_uuid FROM {} WHERE tg_id={}".format(DB_USER_TABLE_NAME, tg_id)).fetchall()
        return bool(query)


class MapsDB(DbInterface):
    """ Child class of DbInterface that helps keep user map records in DB"""

    def add_map(self, map_name: str, map_version: str, user_uuid: str, json_file: str):
        map_uuid = str(uuid1())
        make_bioms_list(map_uuid)(get_bioms_list)(json_file)
        query = 'INSERT INTO {} (map_uuid, map_name, user_uuid, map_version) VALUES (?,?,?,?)'
        query = query.format(DB_USER_MAP_TABLE_NAME)
        self.base.execute(query, (map_uuid, map_name, user_uuid, map_version))
        db_logger.info(
            f'The player\'s map record has been created: ({map_uuid=}, {map_name=}, {user_uuid=}, {map_version=})')
        self.base.commit()

    def delete_map(self, map_uuid):
        query = 'DELETE FROM {} WHERE map_uuid = ?'.format(DB_USER_MAP_TABLE_NAME)
        self.base.execute(query, (map_uuid,))
        self.base.commit()
        db_logger.info(f"The player's map record with {map_uuid=} has been deleted")

    def get_map_list(self, tg_id: str):
        user_uuid = user_db.get_user_uuid(tg_id)
        query = 'SELECT map_name, map_uuid, map_version FROM {} WHERE user_uuid = \'{}\''.format(DB_USER_MAP_TABLE_NAME,
                                                                                                 user_uuid)
        response = self.base.execute(query).fetchall()
        return response


user_db = UserDB()
maps_db = MapsDB()
admin_db = AdminDB()


def main():
    print(user_db.get_user_language('720262392'))


if __name__ == '__main__':
    main()
