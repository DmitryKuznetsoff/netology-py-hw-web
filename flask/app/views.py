from typing import List

from flask import jsonify


class BaseViewMixin:

    @staticmethod
    def get_attrs(source, attrs: List[str]) -> dict:
        """
        Возвращает словарь с атрибутами attrs объекта source
        """
        if isinstance(source, dict):
            return {attr: source.get(attr) for attr in attrs}
        else:
            return {attr: getattr(source, attr) for attr in attrs}

    def jsonify_instance(self, title: str, instance: object, attrs: List[str]) -> jsonify:
        """
        Возвращает json для объекта instance с атрибутами attrs и заголовком title
        """
        instance_list = [instance] if not isinstance(instance, list) else instance
        return jsonify(
            {
                title: [self.get_attrs(obj, attrs) for obj in instance_list]
            }
        )
