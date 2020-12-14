from datetime import datetime
from secrets import token_urlsafe

from app import db, errors
from app.models import BaseModelMixin
from user.models import User


class Token(db.Model, BaseModelMixin):
    __tablename__ = 'token'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(120), nullable=False, unique=True)
    created = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship(User, uselist=False, back_populates='token')

    def __init__(self, *args, **kwargs):
        super(Token, self).__init__(*args, **kwargs)
        self.key = token_urlsafe(90)

    def __repr__(self):
        return self.key

    @staticmethod
    def auth_user_by_token(token: str) -> User:
        user_instance = Token.query.filter(Token.key == token).first().user
        if user_instance:
            return user_instance
        raise errors.Forbidden
