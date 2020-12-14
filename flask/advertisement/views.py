from flask import Blueprint, request, make_response
from flask.views import MethodView

from advertisement.models import Advertisement
from advertisement.schema import ADV_CREATE, ADV_UPDATE
from app.validator import validate
from app.views import BaseViewMixin
from authtoken.models import Token
from authtoken.views import get_token_from_headers

advertisement = Blueprint('advertisement/', __name__)


class AdvertisementAPI(MethodView, BaseViewMixin):
    json_title = 'advertisements'
    json_attrs = ['id', 'title', 'description', 'created', 'user_id', ]
    json_read_only_attrs = ['id', 'created', 'user_id', ]

    @staticmethod
    def get_user_instance():
        token = get_token_from_headers()
        user_instance = Token.auth_user_by_token(token)
        return user_instance

    def get(self, advertisement_id=None):
        if advertisement_id:
            adv = Advertisement.by_id(advertisement_id)
        else:
            adv = Advertisement.query.all()
        response = self.jsonify_instance(self.json_title, adv, self.json_attrs)
        return make_response(response, 200)

    @validate('json', ADV_CREATE)
    def post(self):
        user_instance = self.get_user_instance()

        data = self.get_attrs(request.json, ['title', 'description'])

        create_adv = Advertisement(**data, user=user_instance)
        Advertisement.add(create_adv)

        response = self.jsonify_instance(self.json_title, create_adv, self.json_attrs)
        return make_response(response, 201)

    @validate('json', ADV_UPDATE)
    def patch(self, advertisement_id):
        user_instance = self.get_user_instance()
        adv = Advertisement.by_id(advertisement_id)
        if adv.check_adv_user(user_instance):
            allowed_attrs = set(self.json_attrs) - set(self.json_read_only_attrs)
            data = {attr: request.json[attr] for attr in allowed_attrs if attr in request.json.keys()}
            adv.upd_obj(**data)
        response = self.jsonify_instance(self.json_title, adv, self.json_attrs)
        return make_response(response, 200)

    def delete(self, advertisement_id):
        user_instance = self.get_user_instance()
        adv = Advertisement.by_id(advertisement_id)

        if adv.check_adv_user(user_instance):
            adv.del_obj()
            return make_response({}, 204)


advertisement_view = AdvertisementAPI.as_view('advertisement_api')
advertisement.add_url_rule(advertisement.name, view_func=advertisement_view,
                           methods=['GET'])
advertisement.add_url_rule(advertisement.name, view_func=advertisement_view, methods=['POST'])
advertisement.add_url_rule(f'{advertisement.name}<int:advertisement_id>/', view_func=advertisement_view,
                           methods=['GET', 'PATCH', 'DELETE'])
