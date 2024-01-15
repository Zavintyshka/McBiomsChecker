from db_funcs import user_db, admin_db
from settings import DB_USER_TABLE_NAME


def is_user_exist(tg_id) -> bool:
    query = user_db.base.execute("SELECT user_uuid FROM {} WHERE tg_id={}".format(DB_USER_TABLE_NAME, tg_id)).fetchall()
    return bool(query)


def is_admin(tg_id: str | int) -> bool:
    query = 'SELECT admin FROM {} WHERE tg_id =?'.format(DB_USER_TABLE_NAME)
    response = admin_db.base.execute(query, (str(tg_id),)).fetchall()[0][0]
    return bool(response)
