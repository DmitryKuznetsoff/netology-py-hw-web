import hashlib

from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, Text, ForeignKey
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# class BaseModel(Base):
#     __abstract__ = True
#
#     @classmethod
#     def by_id(cls, obj_id):
#         obj = cls.query.get(obj_id)
#         if obj:
#             return obj
#         else:
#             raise Exception('Not Found')


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(64), nullable=False)
    email = Column(String, nullable=False, unique=True)
    username = Column(String)
    created = Column(DateTime)
    is_admin = Column(Boolean, nullable=False, default=False)

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

    @classmethod
    async def get_by_field(cls, conn, field, value):
        table = cls.__table__
        async with conn as c:
            query = await c.execute.table.select().where(table.getattr(field) == value)
            records = await query.fetchall()
            if records:
                return records
            raise Exception('Object not found')


class Token(Base):
    __tablename__ = 'token'

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(120), nullable=False, unique=True)
    created = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    user = relationship(User, uselist=False, backref='token')

    def __repr__(self):
        return self.key


class Advertisement(Base):
    __tablename__ = 'advertisement'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    created = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref='advertisement')

    def __repr__(self):
        return f'{self.id}\n{self.title}\n{self.description}\n{self.created}\n{self.user_id}>'

    def check_owner(self, user_instance):
        if self.user == user_instance:
            return self
        raise Exception('Forbidden')
