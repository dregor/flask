# manage.py

from flask.ext.script import Manager, prompt_bool
from flask.ext.migrate import Migrate, MigrateCommand
from app import app, models, views


migrate = Migrate(app, models.db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
@manager.option('-n', '--name', help='Your name')
def hello(name='user'):
    print("hello " + name)


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to lose all your data?"):
        models.db.drop_all()


if __name__ == "__main__":
    manager.run()
