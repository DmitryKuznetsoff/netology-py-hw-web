from aiohttp import web
from aiohttp.web_response import json_response


class BaseView(web.View):
    """
    Базовый view класс
    Содержит методы для обработки get, post, patch и delete запросов
    """
    URL_PATH = str
    MODEL = None
    SERIALIZER = None
    RESPONSE_HEADER = str
    ALLOWED_FIELDS = []  # поля, доступные для изменения в patch-запросе

    def to_json(self, data):
        return self.SERIALIZER.dump(data)

    @property
    def db(self):
        return self.request.app['db']

    @property
    def conn(self):
        return self.db.acquire()

    @property
    def table(self):
        return self.MODEL.__table__

    def get_response(self, data, status):
        return json_response({self.RESPONSE_HEADER: data}, status=status)

    async def get_obj_by_id(self, obj_id):
        async with self.conn as c:
            query = await c.execute(self.table.select().where(self.table.c.id == obj_id))
            return await query.fetchall()

    async def get_all_objs(self):
        async with self.conn as c:
            query = await c.execute(self.table.select())
            return await query.fetchall()

    async def check_obj_id_existence(self):
        obj_id = self.request.match_info.get('id')

        try:
            obj_id = int(obj_id)
        except ValueError:
            return False
        existing_ids = [obj.id for obj in await self.get_all_objs()]

        return obj_id if obj_id in existing_ids else False

    async def prepare_request_data(self, data):
        """
        Подготовка данных из тела запроса перед записью в БД
        Переопределите в классах-потомках с учётом специфики каждой модели
        """
        return data

    async def get(self):
        obj_id = self.request.match_info.get('id')
        if obj_id:
            records = await self.get_obj_by_id(obj_id)
        else:
            records = await self.get_all_objs()
        data = [self.to_json(r) for r in records]
        return self.get_response(data, 200)

    async def post(self):
        request_data = await self.request.json()
        data = await self.prepare_request_data(request_data)
        if data:
            async with self.conn as c:
                await c.execute(self.table.insert().values(**data))
                return json_response({self.RESPONSE_HEADER: '201: Created'}, status=201)

    async def patch(self):
        obj_id = await self.check_obj_id_existence()
        if not obj_id:
            return json_response({self.RESPONSE_HEADER: '404: Not Found'}, status=404)

        request_data = await self.request.json()
        for data in request_data:
            if data not in self.ALLOWED_FIELDS:
                del request_data[data]

        async with self.conn as c:
            await c.execute(self.table.update().values(**request_data).where(self.table.c.id == obj_id))
            return json_response({self.RESPONSE_HEADER: '200: OK'}, status=200)

    async def delete(self):
        obj_id = await self.check_obj_id_existence()
        if not obj_id:
            return web.Response(body='404: Not Found', status=404)

        async with self.conn as c:
            await c.execute(self.table.delete().where(self.table.c.id == obj_id))
            return json_response({self.RESPONSE_HEADER: '204: No Content'}, status=204)
