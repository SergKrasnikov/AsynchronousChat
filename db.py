import peewee_async
import peewee as pw

db = peewee_async.MySQLDatabase(host='localhost', port=3306,
                                user='aiohttp', password='warning123',
                                database='aiohttp', )


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
