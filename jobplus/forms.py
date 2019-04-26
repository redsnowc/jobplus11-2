from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, BooleanField, 
                     IntegerField, TextAreaField, ValidationError)
from wtforms.validators import (Length, Email, EqualTo, DataRequired, 
                                AnyOf, URL, NumberRange)
from jobplus.models import db, User, Company


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField(
            '密码', validators=[DataRequired(), Length(6, 24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validata_email(self, field):
        if not User.query.filter_by(email=field.data).first() \
           or not Company.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱未注册')

    def validata_password(self, field):
        user = User.query.filter_by(email=field.data).first()
        company = Company.query.filter_by(email=field.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')
        elif company and not company.check_password(field.data):
            raise ValidationError('密码错误')


class UserRegisterForm(FlaskForm):
    username = StringField(
            '用户名', validators=[DataRequired(), Length(3, 24)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField(
            '密码', validators=[DataRequired(), Length(6, 24)])
    repeat_password = PasswordField(
            '重复密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('提交')

    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first() \
           or Company.query.filter_by(company_name=field.data).first():
            raise ValidationError('用户名已存在')

    def validata_email(self, field):
        if User.query.filter_by(email=field.data).first() \
           or Company.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已存在')


class CompanyRegisterForm(UserRegisterForm):
    username = StringField(
            '企业名称', validators=[DataRequired(), Length(3, 64)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField(
            '密码', validators=[DataRequired(), Length(6, 24)])
    repeat_password = PasswordField(
            '重复密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('提交')

    def create_company(self):
        company = Company()
        company.company_name = self.username.data
        company.email = self.email.data
        company.password = self.password.data
        db.session.add(company)
        db.session.commit()
        return company

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first() \
           or Company.query.filter_by(company_name=field.data).first():
            raise ValidationError('企业名已存在')

    def validata_email(self, field):
        if User.query.filter_by(email=field.data).first() \
           or Company.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已存在')

