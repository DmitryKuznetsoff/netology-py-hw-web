from flask import Blueprint, request, make_response
from flask import jsonify
from flask.views import MethodView

from app import errors
from authtoken.models import Token
from user.models import User

authtoken = Blueprint('authtoken', __name__)


def get_token_from_headers() -> str:
    headers = request.headers.environ
    try:
        _, token = headers['HTTP_AUTHORIZATION'].split(' ')
    except KeyError:
        raise errors.Forbidden
    return token


class TokenAPI(MethodView):

    def get(self) -> jsonify:
        user_instance = User.auth_user_by_pwd(request.json)
        response = jsonify({'token': user_instance.token.key if user_instance.token else None})
        return make_response(response, 200)

    def post(self) -> jsonify:
        user_instance = User.auth_user_by_pwd(request.json)
        create_token = Token(user_id=user_instance.id)
        Token.add(create_token)
        response = jsonify({'token': create_token.key})
        return make_response(response, 201)


token_view = TokenAPI.as_view('token_api')
authtoken.add_url_rule(f'{authtoken.name}/', view_func=token_view, methods=['POST'])
authtoken.add_url_rule(f'{authtoken.name}/', view_func=token_view, methods=['GET'])
