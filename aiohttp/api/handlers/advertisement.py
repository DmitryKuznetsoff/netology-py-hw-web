from datetime import datetime

from aiohttp.web_response import json_response

from db.schema import Advertisement
from utils.token import auth_by_token
from .base_handler import BaseView
from api.schema import AdvertisementSchema


class AdvertisementView(BaseView):
    URL_PATH = r'advertisement/{id:\d*}'
    MODEL = Advertisement
    SERIALIZER = AdvertisementSchema()
    RESPONSE_HEADER = 'advertisement'
    ALLOWED_FIELDS = ['title', 'description', ]

    @property
    async def owner(self):
        return await auth_by_token(self.conn, self.request)

    async def check_owner(self):
        adv_id = self.request.match_info.get('id')
        adv = await self.get_obj_by_id(adv_id)
        owner = await self.owner
        return adv[0].user_id == owner.id

    async def prepare_request_data(self, data):
        data['created'] = datetime.now()
        owner = await self.owner
        data['user_id'] = owner.id
        return data

    async def get(self):
        return await super().get()

    async def post(self):
        if await self.owner:
            return await super().post()
        return json_response({self.RESPONSE_HEADER: '401: Unauthorized'}, status=401)

    async def patch(self):
        if await self.owner:
            if await self.check_owner():
                return await super().patch()
            return json_response({self.RESPONSE_HEADER: '403: Forbidden'}, status=403)
        return json_response({self.RESPONSE_HEADER: '401: Unauthorized'}, status=401)

    async def delete(self):
        if await self.owner:
            if await self.check_owner():
                return await super().delete()
            return json_response({self.RESPONSE_HEADER: '403: Forbidden'}, status=403)
        return json_response({self.RESPONSE_HEADER: '401: Unauthorized'}, status=401)
