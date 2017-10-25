import peewee_async
import peewee as pw
from settings import DB_HOST,DB_PORT, DB_LOGIN, DB_PASSWD, DB_NAME,\
    ADMIN_LOGIN, ADMIN_PASSWD, ADMIN_EMAIL

db = peewee_async.MySQLDatabase(host=DB_HOST, port=DB_PORT,
                                user=DB_LOGIN, password=DB_PASSWD,
                                database=DB_NAME, )


class BaseMySQLModel(pw.Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = db


__all__ = [BaseMySQLModel, ]

# Connect to our database.
db.connect()

from auth.models import UserMySQL
from chat.models import RoomMySQL, MessageMySQL

# Only create the tables if they do not exist.
db.create_tables([UserMySQL, RoomMySQL, MessageMySQL, ], safe=True)

user = UserMySQL(login=ADMIN_LOGIN, password=ADMIN_PASSWD, email=ADMIN_EMAIL, is_admin=True)
user.create_user()
