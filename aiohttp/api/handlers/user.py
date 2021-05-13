import hashlib
from datetime import datetime

from aiohttp.web_response import json_response

from api.handlers.base_handler import BaseView
from api.schema import UserSchema
from db.schema import User
from utils.token import create_user_token, auth_by_token


class UserView(BaseView):
    URL_PATH = r'users/{id:\d*}'
    MODEL = User
    SERIALIZER = UserSchema()
    RESPONSE_HEADER = 'users'
    ALLOWED_FIELDS = ['username', 'email', 'password', ]

    def prepare_request_data(self, data):
        data['created'] = datetime.now()
        data['is_admin'] = False
        raw_pwd = data['password']
        data['password'] = self.get_password_hash(raw_pwd)
        return data

    async def get_by_username(self, username):
        async with self.conn as c:
            query = await c.execute(self.table.select().where(self.table.c.username == username))
            return await query.fetchone()

    @staticmethod
    def get_password_hash(raw_password: str) -> str:
        return hashlib.sha256(raw_password.encode()).hexdigest()

    def get(self):
        return super().get()

    async def post(self):
        await super().post()

        request_data = await self.request.json()
        username = request_data.get('username')
        user = await self.get_by_username(username)
        token = await create_user_token(self.conn, user)

        return self.get_response({'token': token}, 201)

    async def patch(self):
        if await auth_by_token(self.conn, self.request):
            return await super().patch()
        return json_response({self.RESPONSE_HEADER: '403: Forbidden'}, status=403)

    async def delete(self):
        if await auth_by_token(self.conn, self.request):
            return await super().delete()
        return json_response({self.RESPONSE_HEADER: '403: Forbidden'}, status=403)
