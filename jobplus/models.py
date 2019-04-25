'''
User 普通用户和管理员的数据表
Company 公司用户的数据表
Resume 简历数据表
CompanyInfo 公司简介数据表
Job 职位数据表
'''

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    create_at = db.Column(
            db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class User(Base):
    ROLE_USER = 10
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
            db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(
            db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    user_resume = db.relationship('Resume')


class Company(Base):
    ROLE_COMPANY = 20
    
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(
            db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(
            db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_COMPANY)
    publish_job = db.relationship('Job')
    company_info = db.relationship('CompanyInfo')


class Resume(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, nullable=False)
    email = db.Column(db.String(64), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    body = db.Column(db.Text)
    user_id = db.Column(
            db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User', uselist=False)


class CompanyInfo(Base):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(32))
    field = db.Column(db.String(64))
    intro = db.Column(db.Text)
    company_id = db.Column(
            db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'))
    company = db.relationship('Company', uselist=False)
            

class Job(Base):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    salary_lower = db.Column(db.Integer, nullable=False)
    salary_upper = db.Column(db.Integer, nullable=False)
    experience_lower = db.Column(db.Integer, default=0)
    experience_upper = db.Column(db.Integer, default=0)
    education = db.Column(db.String(16), default='学历不限')
    tags = db.Column(db.String(128))
    intro = db.Column(db.Text)
    company_id = db.Column(
            db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'))
    company = db.relationship('Company', uselist=False)

