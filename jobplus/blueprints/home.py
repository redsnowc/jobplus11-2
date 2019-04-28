'''
首页蓝图
'''

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required
from jobplus.models import User, Job, db
from jobplus.forms import LoginForm, UserRegisterForm, CompanyRegisterForm

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    jobs = db.session.query(Job).order_by(Job.create_at.desc()).limit(15).all()
    return render_template('index.html', jobs=jobs)

@home_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, form.remember_me.data)
        return redirect(url_for('.index'))
    return render_template('login.html', form=form)

@home_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出登录', 'success')
    return redirect(url_for('.index'))

@home_bp.route('/user-register', methods=['GET', 'POST'])
def user_register():
    form = UserRegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功，请登录！', 'success')
        return redirect(url_for('.login'))
    return render_template('user_register.html', form=form)

@home_bp.route('/company-register', methods=['GET', 'POST'])
def company_register():
    form = CompanyRegisterForm()
    if form.validate_on_submit():
        form.create_company()
        flash('注册成功，请登录！', 'success')
        return redirect(url_for('.login'))
    return render_template('company_register.html', form=form)
   
