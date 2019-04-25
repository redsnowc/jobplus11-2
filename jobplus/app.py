'''
注册蓝图、初始化数据库、定义 create_app 函数
'''

from flask import Flask
from flask_migrate import Migrate
from jobplus.config import configs
from jobplus.blueprints import home_bp
from jobplus.models import db


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
