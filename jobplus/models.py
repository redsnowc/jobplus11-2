'''
User 用户数据表
UserInfo 用户信息表
CompanyInfo 公司简介数据表
Job 职位数据表
'''

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    create_at = db.Column(
            db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class User(Base, UserMixin):
    ROLE_USER = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
            db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(
            db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    user_info = db.relationship('UserInfo', uselist=False, backref='user', 
            cascade='all, delete-orphan', passive_deletes = True)
    publish_job = db.relationship('Job', backref='company',
            cascade='all, delete-orphan', passive_deletes = True)
    company_info = db.relationship('CompanyInfo', uselist=False, 
            backref='company', cascade='all, delete-orphan', 
            passive_deletes = True)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY

    @property
    def is_user(self):
        return self.role == self.ROLE_USER


class UserInfo(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    phone_number = db.Column(db.String(11), nullable=False)
    experience = db.Column(db.Integer, default=0)
    resume = db.Column(db.String(256))
    user_id = db.Column(
            db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))


class CompanyInfo(Base):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(256))
    domain = db.Column(db.String(64))
    intro = db.Column(db.String(256))
    detail = db.Column(db.Text)
    logo = db.Column(db.String(256))
    website = db.Column(db.String(256))
    company_id = db.Column(
            db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
            

class Job(Base):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    salary_lower = db.Column(db.Integer, nullable=False)
    salary_upper = db.Column(db.Integer, nullable=False)
    experience_lower = db.Column(db.Integer, default=0)
    experience_upper = db.Column(db.Integer, default=0)
    education = db.Column(db.String(16), default='学历不限')
    tags = db.Column(db.String(128))
    intro = db.Column(db.Text)
    company_id = db.Column(
            db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))

