"""
Модуль для создания маршрутизации на основе
свойства URL_PATH у классов, указанных в API_VIEWS
"""

from api.handlers import HANDLERS

API_URL_PREFIX = r'/api/v1/'


def register_routes(app):
    for handler in HANDLERS:
        app.router.add_route('*', API_URL_PREFIX + handler.URL_PATH, handler)
