from datetime import datetime
from secrets import token_urlsafe
from sqlalchemy import select, join

from db.schema import Token, User

TOKEN_MODEL = Token
USER_MODEL = User

token_table = Token.__table__
user_table = USER_MODEL.__table__


async def create_user_token(conn, user):
    created = datetime.now()
    key = token_urlsafe(90)
    user_id = user.id
    async with conn as c:
        await c.execute(token_table.insert().values(created=created, key=key, user_id=user_id))
        return key


def get_token_from_headers(request):
    return request.headers.get('Authorization')


async def auth_by_token(conn, request):
    key = get_token_from_headers(request)
    async with conn as c:
        j = join(user_table, token_table, user_table.c.id == token_table.c.user_id)
        query = await c.execute(select(user_table, token_table).select_from(j).where(token_table.c.key == key))
        return await query.fetchone() or None
