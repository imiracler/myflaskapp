from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.models.music import Music
from myflaskapp import app


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://kejie:Kejiedai123@@118.25.135.109:3306/Miracle'

from app.models import db

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
