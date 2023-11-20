import os

from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from flask_migrate import Migrate

from .src.accounts.views import auth
from .src.database.simple_models import UserSite
from .src.settings import settings
from .src.university.views import view


"""
    Flask app (run command: flask run --reload)
    ORM: flask-sqlalchemy
    DB: sqlite
    migrations: flask_migrate (commands: flask db init -> flask db migrate -> flask db upgrade)
    auth: flask_login    
"""

template_dir = os.path.abspath('templates/')
app = Flask(import_name="app", template_folder=template_dir)
app.config['SECRET_KEY'] = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLITE_URL
app.config.update(
    DEBUG=True,
    SECRET_KEY="secret_sauce",
    SESSION_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Strict",
)
app.register_blueprint(blueprint=auth)
app.register_blueprint(blueprint=view)

db = settings.db_lite.init_app(app=app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return UserSite.query.get(int(user_id))


migrate = Migrate(app=app, db=db)
admin = Admin(app=app)
# admin.add_view(ModelView(Student, db.session))
# admin.add_view(ModelView(University, db.session))



