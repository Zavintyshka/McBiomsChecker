import sqlite3 as sq
from uuid import uuid1

from logger import user_logger
from settings import *
from general_func import make_bioms_list, get_bioms_list


class DbInterfaceMain:
    __instances = []

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        cls.__instances.append(instance)
        return instance

    def __init__(self):
        self.__base = sq.connect(DB_PATH)

    def __del__(self):
        if len(self.__instances) == 1:
            self.__base.close()
            print('закрытие БД')
        self.__instances.remove(self)

    @property
    def instances(self):
        return self.__instances

    @property
    def base(self):
        return self.__base


class AdminDB(DbInterfaceMain):
    def get_game_file_path(self, game_version: str):
        query = 'SELECT path_to_json FROM {} WHERE game_version=?'.format(DB_ADMIN_TABLE_NAME)
        data = self.base.execute(query, (game_version,)).fetchall()
        return data[0][0]

    def create_game_record(self, game_version: str, json_path: str):
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


class UserDB(DbInterfaceMain):
    def create_user(self, tg_id, user_language: str, is_admin: bool):
        user_uuid = str(uuid1())
        query = 'INSERT INTO {} (user_uuid, tg_id, user_language, admin) VALUES (?,?,?,?)'.format(DB_USER_TABLE_NAME)
        self.base.execute(query, (user_uuid, tg_id, user_language, is_admin))
        self.base.commit()

    def get_user_uuid(self, tg_id: str):
        query = 'SELECT user_uuid FROM {} WHERE tg_id={}'.format(DB_USER_TABLE_NAME, tg_id)
        return self.base.execute(query).fetchall()[0][0]
        # TODO сделать обработку ^


class MapsDB(DbInterfaceMain):
    def add_map(self, map_name: str, map_version: str, user_uuid: str, json_file: str):
        map_uuid = str(uuid1())
        make_bioms_list(map_uuid)(get_bioms_list)(json_file)
        query = 'INSERT INTO {} (map_uuid, map_name, user_uuid, map_version) VALUES (?,?,?,?)'
        query = query.format(DB_USER_MAP_TABLE_NAME)
        self.base.execute(query, (map_uuid, map_name, user_uuid, map_version))
        self.base.commit()

    def delete_map(self, map__uuid):
        query = 'DELETE FROM {} WHERE map_uuid = ?'.format(DB_USER_MAP_TABLE_NAME)
        self.base.execute(query, (map__uuid,))
        self.base.commit()

    def get_map_list(self, tg_id: str):
        user_uuid = user_db.get_user_uuid(tg_id)
        query = "SELECT map_name, map_uuid, map_version FROM {} WHERE user_uuid = '{}'".format(DB_USER_MAP_TABLE_NAME,
                                                                                               user_uuid)
        response = self.base.execute(query).fetchall()
        return response


user_db = UserDB()
maps_db = MapsDB()
admin_db = AdminDB()


def main():
    pass
    # print(maps_db.get_map_list('720262392'))
    # user_db.create_user(tg_id='720262393', user_language='EN')
    # maps_db.add_map('some_map2', '1.20', '9c61bf10-b195-11ee-a34d-9a9045ac45ee', 'temp/user_data2.json')
    # print(user_db.get_user_map_list('720262392'))
    # print(maps_db.get_map_progress('aa91c114-b192-11ee-8374-9a9045ac45ee'))


if __name__ == '__main__':
    main()
