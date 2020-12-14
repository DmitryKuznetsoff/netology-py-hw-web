from app import db
from sqlalchemy import exc
from app import errors


class BaseModelMixin:

    @classmethod
    def by_id(cls, obj_id):
        obj = cls.query.get(obj_id)
        if obj:
            return obj
        else:
            raise errors.NotFound

    def add(self):
        db.session.add(self)
        self.try_to_commit()

    def del_obj(self):
        db.session.delete(self)
        self.try_to_commit()

    def upd_obj(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)
        self.try_to_commit()

    @staticmethod
    def try_to_commit():
        try:
            db.session.commit()
        except exc.IntegrityError:
            raise errors.BadLuck
