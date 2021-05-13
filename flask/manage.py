from flask_script import Manager

from app import app
from management.commands import mailing_command, create_tables

manager = Manager(app)


@manager.command
def mailing():
    mailing_command()


@manager.command
def tables():
    create_tables()


if __name__ == '__main__':
    manager.run()
