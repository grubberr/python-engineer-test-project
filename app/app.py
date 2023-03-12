from apiflask import APIFlask

from app.model import db
from app.teams import api
from app.command import command_cli

app = APIFlask(__name__)
app.config.from_prefixed_env()
db.init_app(app)
app.register_blueprint(api)
app.cli.add_command(command_cli)


def main():
    app.run()


if __name__ == '__main__':
    main()
