from aiohttp import web

from db.db import init_db, close_db
from utils.config_parser import app_config
from utils.route_dispatcher import register_routes


def init_app():
    app = web.Application()
    app['config'] = app_config
    app.on_startup.append(init_db)
    app.on_cleanup.append(close_db)
    register_routes(app)
    return app


if __name__ == '__main__':
    app = init_app()
    web.run_app(app, **app['config']['api'])
