from flask_script import Manager

from app import app
from management.commands import mailing_command

manager = Manager(app)


@manager.command
def mailing():
    mailing_command()


if __name__ == '__main__':
    manager.run()
