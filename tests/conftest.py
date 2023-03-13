import time

import docker
import pytest
from apiflask import APIFlask
from sqlalchemy_utils.functions import create_database, drop_database

from app.command import command_cli
from app.model import db
from app.teams import api
from app.teams.auth import login_api

POSTGRES_PASSWORD = "password"
POSTGRES_USER = "postgres"
POSTGRES_DATABASE = "centralnicgroup_test"


@pytest.fixture(scope="session")
def database_service():
    client = docker.from_env()

    container = client.containers.run(
        "postgres:14",
        detach=True,
        remove=True,
        environment={"POSTGRES_PASSWORD": POSTGRES_PASSWORD},
        ports={"5432/tcp": None},
    )

    # There is a better way to wait initialization
    time.sleep(5)

    container.reload()
    yield container.ports["5432/tcp"][0]["HostPort"]
    container.stop()


@pytest.fixture
def database(database_service):
    url = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{database_service}/{POSTGRES_DATABASE}"
    create_database(url)
    yield url
    drop_database(url)


@pytest.fixture
def app(database):
    app = APIFlask(__name__)
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": database,
        "SECRET_KEY": "d90f9df0d56adc2b058b89585d5cb38306864b7e6988fb46",
    })

    db.init_app(app)
    app.register_blueprint(api)
    app.register_blueprint(login_api)
    app.cli.add_command(command_cli)
    with app.app_context():
        db.create_all()
    yield app
