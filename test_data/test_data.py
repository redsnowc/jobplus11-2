# -*- coding: UTF-8 -*-

from jobplus.models import db, User, CompanyInfo, UserInfo, Job
from random import randint, choice
from faker import Faker


fe = Faker()
fc = Faker('zh-cn')

def create_user():
    for i in range(4):
        user = User()
        user_info = UserInfo()
        user.username = fe.name()
        user.email = fe.email()
        user.password = '123456'
        user_info.name = fc.name()
        user_info.phone_number = fc.phone_number()
        user_info.experience = randint(0, 10)
        user_info.resume = fe.url()
        user_info.user = user
        db.session.add(user)
        db.session.add(user_info)
        db.session.commit()

def create_company():
    for i in range(16):
        user = User()
        company_info = CompanyInfo()
        user.username = fc.company()
        user.email = fe.email()
        user.password = '123456'
        user.role = 20
        company_info.address = fc.city()
        company_info.domain = '互联网 AI 大数据'
        company_info.intro = ''.join(fc.words(8))
        company_info.detail = fc.text()
        company_info.logo = 'https://s2.ax1x.com/2019/04/28/EMmHjH.png'
        company_info.website = fc.url()
        company_info.company = user
        db.session.add(user)
        db.session.add(company_info)
        db.session.commit()

def create_job():
    for user in User.query.filter_by(role=20).all():
        for i in range(4):
            job = Job()
            job.title = fc.job()
            job.salary_lower = randint(2, 20)
            job.salary_upper = job.salary_lower + randint(2, 10)
            job.experience_lower = randint(0, 4)
            if job.experience_lower == 0:
                job.experience_upper = 0
            else:
                job.experience_upper = job.experience_lower + randint(1,4)
            job.education = choice(['大专', '本科', '硕士', '博士', '经验不限'])
            job.tags = 'Python Flask Mysql'
            job.intro = fc.text()
            job.company = user
            db.session.add(job)
            db.session.commit()

def create_admin():
    user = User()
    user.username = 'admin'
    user.email = 'admin@admin.com'
    user.password = '123456'
    user.role = 30
    db.session.add(user)
    db.session.commit()

def run():
    create_user()
    create_company()
    create_job()
    create_admin()

