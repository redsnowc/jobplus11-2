'''
注册蓝图、初始化数据库、定义 create_app 函数
'''

from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from jobplus.config import configs
from jobplus.models import db, User
from jobplus.blueprints import (home_bp, user_bp, company_bp, job_bp, 
                                firm_bp, admin_bp)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    register_blueprints(app)
    register_extensions(app)
    return app


def register_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(job_bp)
    app.register_blueprint(firm_bp)
    app.register_blueprint(admin_bp)


def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)

    login_manager.login_view = 'front.login'

