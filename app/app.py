from apiflask import APIFlask

from app.command import command_cli
from app.model import db
from app.teams import api
from app.teams.auth import login_api

app = APIFlask(__name__)
app.config.from_prefixed_env()
db.init_app(app)
app.register_blueprint(api)
app.register_blueprint(login_api)
app.cli.add_command(command_cli)


def main():
    app.run()


if __name__ == '__main__':
    main()
