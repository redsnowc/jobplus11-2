from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, BooleanField, 
                     IntegerField, TextAreaField, ValidationError)
from wtforms.validators import (Length, Email, EqualTo, DataRequired, 
                                AnyOf, URL, NumberRange)
from jobplus.models import db, User, UserInfo


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField(
            '密码', validators=[DataRequired(), Length(6, 24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validata_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱未注册')

    def validata_password(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user and not user.check_password(field.data):
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
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已存在')


class CompanyRegisterForm(FlaskForm):
    username = StringField(
            '企业名称', validators=[DataRequired(), Length(3, 64)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField(
            '密码', validators=[DataRequired(), Length(6, 24)])
    repeat_password = PasswordField(
            '重复密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('提交')

    def create_company(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        user.role = 20
        db.session.add(user)
        db.session.commit()
        return user

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('企业名已存在')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已存在')


class UserInfoForm(FlaskForm):
    name = StringField(
            '真实姓名', validators=[DataRequired(), Length(3, 64)])
    phone_number = StringField(
            '手机号', validators=[DataRequired(), Length(11)])
    experience = IntegerField('工作年限', validators=[DataRequired()])
    resume = StringField('简历地址', validators=[DataRequired(), URL()])
    submit = SubmitField('提交')

    def validate_phone_number(self, field):
        if UserInfo.query.filter_by(phone_number=field.data).first():
            raise ValidationError('手机号已存在')
   
    def create_userinfo(self, user):
        user_info = UserInfo()
        user_info.name = self.name.data
        user_info.phone_number = self.phone_number.data
        user_info.resume = self.resume.data
        user_info.experience = self.experience.data
        user_info.user = user
        db.session.add(user_info)
        db.session.commit()
        return user_info

    def update_userinfo(self, user_info):
        self.populate_obj(user_info)
        db.session.add(user_info)
        db.session.commit()
        return user_info


class EditUserForm(UserRegisterForm):
    
    def update_user(self, user):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已存在')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')
