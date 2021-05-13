"""
Модуль с инструментами для управления БД
"""

from aiopg.sa import create_engine


async def init_db(app):
    pg_conf = app['config']['postgres']

    engine = await create_engine(

        database=pg_conf['database'],
        user=pg_conf['user'],
        password=pg_conf['password'],
        host=pg_conf['host'],
        port=pg_conf['port'],
        minsize=pg_conf['minsize'],
        maxsize=pg_conf['maxsize']
    )
    app['db'] = engine


async def close_db(app):
    app['db'].close()
    await app['db'].wait_closed()
