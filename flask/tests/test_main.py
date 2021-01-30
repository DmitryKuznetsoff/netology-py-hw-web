# conftest.py
import pytest
# from advertisement.views import AdvertisementAPI
from flask import url_for

from app import app


@pytest.fixture
def example_client():
    with app.app_context():
        yield app.test_client()


# test_something.py
def test_smth(example_client):
    # url = 'http://127.0.0.1:5000/api/v1/advertisement/'
    url = url_for('advertisement.advertisement_api')
    resp = example_client.get(url)
    assert resp.status_code == 200
