from flask import Blueprint, request, make_response
from flask import jsonify
from flask.views import MethodView

from app.validator import validate
from app.views import BaseViewMixin
from user.models import User
from user.schema import USER_CREATE

users = Blueprint('users', __name__)


class UserAPI(MethodView, BaseViewMixin):

    json_title = 'users'
    json_attrs = ['id', 'username', 'created', ]
    json_read_only_attrs = ['id', 'created', ]

    def get(self, user_id: int = None) -> jsonify:
        if user_id:
            user = User.by_id(user_id)
        else:
            user = User.query.all()
        response = self.jsonify_instance(self.json_title, user, self.json_attrs)
        return make_response(response, 200)

    @validate('json', USER_CREATE)
    def post(self) -> jsonify:
        data = self.get_attrs(request.json, ['email', 'password', 'username'])

        create_user = User(**data)
        User.add(create_user)
        response = self.jsonify_instance(self.json_title, create_user, self.json_attrs)
        return make_response(response, 201)

    def delete(self, user_id: int) -> jsonify:
        pass

    def patch(self, user_id: int) -> jsonify:
        pass


user_view = UserAPI.as_view('user_api')
users.add_url_rule(f'{users.name}/', defaults={'user_id': None}, view_func=user_view, methods=['GET'])
users.add_url_rule(f'{users.name}/', view_func=user_view, methods=['POST'])
users.add_url_rule(f'{users.name}/<int:user_id>/', view_func=user_view, methods=['GET', 'PATCH', 'DELETE'])
