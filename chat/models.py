from datetime import datetime
import peewee as pw

from auth.models import UserMySQL
from db import BaseMySQLModel

from settings import log


class Message:

    async def save(self, user, msg, **kw):
        result = await self.collection.insert({'user': user, 'msg': msg, 'time': datetime.now()})
        return result

    async def get_messages(self):
        messages = self.collection.find().sort([('time', 1)])
        return await messages.to_list(length=None)


class RoomMySQL(BaseMySQLModel, ):

    id = pw.PrimaryKeyField(primary_key=True, null=False, )

    name = pw.CharField(null=False, )

    async def check_room(self, name, *args, **kwargs):
        try:
            return self.get(name=name, )
        except self.DoesNotExist:
            return False
        except Exception as e:
            log.debug(e)
            return False

    async def create_room(self, name, *args, **kwargs):
        room = await self.check_room(name=name, )

        if not room:
            result = self.insert(name=name, )
            result.execute()
        else:
            result = 'Room exists'

        return result

    class Meta:
        db_table = 'tbl_room'


class MessageMySQL(BaseMySQLModel, ):

    id = pw.PrimaryKeyField(primary_key=True, null=False, )

    user = pw.ForeignKeyField(rel_model=UserMySQL, related_name='messages', )
    room = pw.ForeignKeyField(rel_model=RoomMySQL, related_name='messages', )

    msg = pw.TextField(null=True, )
    create_at = pw.DateTimeField(default=datetime.now, null=False, )

    class Meta:
        db_table = 'tbl_message'

    def __init__(self, db=False, data={}, **kw):
        if db:
            self._db = db

        if data:
            self._user_id = data.get('user_id', False, )
            self._room_id = data.get('room_id', False, )

            self._msg = data.get('msg', False, )

            self._id = data.get('id', 0, )

    async def check_user(self, **kw):
        try:
            return self.get(**{'login': self._login}, )
        except Exception:
            return False

    async def create_user(self, **kw):
        user = await self.check_user()
        if not user:
            user = self.insert(login=self._login, password=self._password, email=self._email, )
            user.execute()
        else:
            result = 'User exists'
            return result
