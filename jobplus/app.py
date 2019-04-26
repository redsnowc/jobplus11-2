'''
注册蓝图、初始化数据库、定义 create_app 函数
'''

from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from jobplus.config import configs
from jobplus.blueprints import home_bp
from jobplus.models import db, User, Company


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    register_blueprints(app)
    register_extensions(app)
    return app


def register_blueprints(app):
    app.register_blueprint(home_bp)


def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        company = Company.query.get(id)
        user = User.query.get(id)
        if user:
            return user
        elif company:
            return company

    login_manager.login_view = 'front.login'

