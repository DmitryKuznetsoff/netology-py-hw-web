import hashlib
from datetime import datetime

from app import db, errors
from app.models import BaseModelMixin


class User(db.Model, BaseModelMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String)
    created = db.Column(db.DateTime, default=datetime.now())
    token = db.relationship('Token', uselist=False, back_populates='user')

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.password = self.get_password_hash(kwargs['password'])
        username = kwargs.get('username')
        self.username = username if username else self.email

    def __repr__(self) -> str:
        return f'<User id: {self.id}, email: {self.email}>'

    @staticmethod
    def get_password_hash(raw_password: str) -> str:
        return hashlib.sha256(raw_password.encode()).hexdigest()

    def check_password(self, raw_password: str):
        return self.password == self.get_password_hash(raw_password)

    @staticmethod
    def auth_user_by_pwd(request_data: dict):
        email = request_data.get('email')
        password = request_data.get('password')

        user_instance = User.query.filter(User.email == email).first()
        if user_instance:
            if user_instance.check_password(password):
                return user_instance
            raise errors.Forbidden
        raise errors.NotFound
