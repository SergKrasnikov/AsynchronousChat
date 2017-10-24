from settings import log

import peewee as pw
from db import BaseMySQLModel


class UserMySQL(BaseMySQLModel, ):

    id = pw.PrimaryKeyField(primary_key=True, null=False, )

    is_admin = pw.BooleanField(default=False, )
    login = pw.CharField(max_length=50, null=True, )
    password = pw.CharField(max_length=50, null=True, )
    email = pw.CharField(max_length=50, null=True, )

    class Meta:
        db_table = 'tbl_user'

    def __init__(self, data={}, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if data:
            self._login = data.get('login', False, )
            self._password = data.get('password', False, )

            self._is_admin = data.get('is_admin', False, )

            self._id = data.get('id', 0, )
            self._email = data.get('email', False, )

    async def check_user(self, **kw):
        try:
            return self.get(login=self._login, password=self._password, )
        except self.DoesNotExist:
            return False
        except Exception as e:
            log.debug(e)
            return False

    async def get_user_by_id(self, **kw):
        try:
            return self.get(id=self._id, )
        except self.DoesNotExist:
            return False
        except Exception as e:
            log.debug(e)
            return False

    async def create_user(self, **kw):
        user = await self.check_user()

        if not user:
            with self._meta.database.transaction():
                user = self.create(login=self._login, password=self._password, email=self._email, )
            return user

        else:
            result = 'User exists'
            return result
