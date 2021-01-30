from flask import url_for

from user.models import User


def test_create_user(client, app_config):
    assert User.query.filter_by(email='tst@tst.ts').first() is None

    url = url_for('users.user_api')
    resp = client.post(url, json={'email': 'tst@tst.ts', 'password': 'pwd'})
    assert resp.status_code == 201

    user = User.query.filter_by(email='tst@tst.ts').first()
    assert user.username == 'tst@tst.ts'
