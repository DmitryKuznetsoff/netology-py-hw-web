import contextlib
import time
from copy import copy

import docker as docker
import flask_migrate
import psycopg2
import pytest
from app import app, Config

TEST_DB_USER = 'flask-test'
TEST_DB_PWD = 'flask-test'
TEST_DB_NAME = 'flask-test'
TEST_DB_PORT = 5433


def wait_success(message, f, *, timeout=30, interval=0.01):
    start = time.monotonic()
    exception = None
    while time.monotonic() < start + timeout:
        try:
            f()
        except Exception as e:
            exception = e
            time.sleep(interval)
        else:
            return
    raise TimeoutError(f"{message} failed with last exception {exception}")


@contextlib.contextmanager
def container_finalization(container):
    try:
        yield
    finally:
        container.kill()


def _get_container_port(container):
    container.reload()
    ports = container.attrs["NetworkSettings"]["Ports"]
    ports = {k:v for k, v in ports.items() if v is not None}

    if len(ports) != 1:
        raise RuntimeError(f"Expect exactly one exposed port, got {ports}")
    desc, *_ = ports.values()
    if len(desc) != 1:
        raise RuntimeError(f"Expect exactly one attached port, got {desc}")
    return desc[0]["HostPort"]


@pytest.fixture(scope="session")
def _docker():
    return docker.from_env()


@pytest.fixture(scope="session", autouse=True)
def _test_network(_docker):
    network = _docker.networks.create('test-network')
    yield network
    network.remove()


@pytest.fixture(scope="session", autouse=True)
def _postgres_container(_docker, _test_network):
    container_name = 'pytest-temp-postgres'
    postgres = _docker.containers.run(
        image="postgres:11.0-alpine",
        auto_remove=True,
        remove=True,
        detach=True,
        name=container_name,
        ports={5432: TEST_DB_PORT},
        environment=dict(
            POSTGRES_USER=TEST_DB_USER,
            POSTGRES_DB=TEST_DB_NAME
        ),
        network='test-network',
    )
    port = _get_container_port(postgres)
    with container_finalization(postgres):
        wait_success("postgres", lambda: psycopg2.connect(user=TEST_DB_USER, host='localhost',
                                                          port=port, connect_timeout=1))
        yield postgres


@pytest.fixture(scope="session", autouse=True)
def app_config(_postgres_container):
    test_config = copy(Config)
    test_config.TESTING = True
    test_config.LOGIN_DISABLED = True
    test_config.SQLALCHEMY_DATABASE_URI = (
        f'postgresql://{(TEST_DB_USER)}:{TEST_DB_PWD}@'
        f'localhost:{TEST_DB_PORT}/{TEST_DB_NAME}'
    )
    app.config.from_object(test_config)
    with app.app_context():
        flask_migrate.upgrade(directory=f'{app.config["BASE_PATH"]}/migrations')


@pytest.fixture
def client(app_config):
    with app.app_context():
        yield app.test_client()
