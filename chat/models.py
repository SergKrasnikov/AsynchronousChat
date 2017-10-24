from datetime import datetime
import peewee as pw

from auth.models import UserMySQL
from db import BaseMySQLModel

from settings import log


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

    async def get_room_by_id(self, id, *args, **kwargs):
        try:
            return self.get(id=int(id), )
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

    def __init__(self, data={}, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if data:
            self._user_id = data.get('user_id', False, )
            self._room_id = data.get('room_id', False, )

            self._msg = data.get('msg', False, )

            self._id = data.get('id', 0, )

    async def get_messages(self, room_id=None, ):
        return self.select().join(RoomMySQL).where(RoomMySQL.id == int(room_id) if room_id else int(self._room_id))

    async def insert_message_to_db(self, msg, *args,  **kwargs):
        message = self.insert(user=self._user_id, room=self._room_id, msg=msg, )
        return message.execute()
