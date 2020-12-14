from datetime import datetime

from app import db, errors
from app.models import BaseModelMixin
from user.models import User


class Advertisement(db.Model, BaseModelMixin):
    __tablename__ = 'advertisement'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User, backref='advertisement')

    def check_adv_user(self, user_instance):
        if self.user == user_instance:
            return self
        raise errors.Forbidden

    def __repr__(self):
        return f'{self.id}\n{self.title}\n{self.description}\n{self.created}\n{self.user_id}'
