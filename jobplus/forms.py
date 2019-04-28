from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, BooleanField, 
                     IntegerField, TextAreaField, ValidationError)
from flask_login import current_user
from wtforms.validators import (Length, Email, EqualTo, DataRequired, 
                                AnyOf, URL, NumberRange, Regexp, Optional)
from jobplus.models import db, User, UserInfo, CompanyInfo, Job


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField(
            '密码', validators=[DataRequired(), Length(6, 24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱未注册')

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
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
            '手机号', validators=[DataRequired(), 
                Regexp('^1[3578]\d{9}$', message="手机号格式不正确")])
    experience = IntegerField('工作年限', validators=[DataRequired()])
    resume = StringField('简历地址', validators=[DataRequired(), URL()])
    submit = SubmitField('提交')

    def validate_phone_number(self, field):
        user_info = User.query.filter_by(
                username=current_user.username).first().user_info
        if not user_info:
            if UserInfo.query.filter_by(phone_number=field.data).first():
                raise ValidationError('手机号已存在')
        else:
            if field.data != user_info.phone_number and (
                UserInfo.query.filter_by(phone_number=field.data).first()):
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
        if field.data != current_user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已存在')

    def validate_username(self, field):
        if field.data != current_user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')
        

class CompanyInfoForm(FlaskForm):
    address = StringField('企业地址', validators=[Optional(), Length(2, 256)])
    domain = StringField('业务领域 (请使用空格分割)', validators=[Optional(), Length(2, 64)])
    intro = StringField('企业简介', validators=[Optional(), Length(20, 256)])
    detail = TextAreaField('详细介绍')
    logo = StringField('企业Logo', validators=[Optional(), URL()])
    website = StringField('企业主页', validators=[Optional(), URL()])
    submit = SubmitField('提交')

    def create_companyinfo(self, user):
        company_info = CompanyInfo()
        company_info.address = self.address.data
        company_info.domain = self.domain.data
        company_info.intro = self.intro.data
        company_info.detail = self.detail.data
        company_info.logo = self.logo.data
        company_info.website = self.website.data
        company_info.company = user
        db.session.add(company_info)
        db.session.commit()
        return company_info

    def update_companyinfo(self, company_info):
        self.populate_obj(company_info)
        db.session.add(company_info)
        db.session.commit()
        return company_info


class EditCompanyForm(EditUserForm):
    username = StringField(
            '企业名称', validators=[DataRequired(), Length(3, 64)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField(
            '密码', validators=[DataRequired(), Length(6, 24)])
    repeat_password = PasswordField(
            '重复密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('提交')


class PostJobForm(FlaskForm):
    title = StringField(
            '职位名称', validators=[DataRequired(), Length(4, 128)])
    salary_lower = IntegerField(
            '最低工资 (k)', validators=[DataRequired(), 
                        NumberRange(min=1, message=('无效输入'))])
    salary_upper = IntegerField(
            '最高工资 (k)', validators=[DataRequired(),
                        NumberRange(min=1, message=('无效输入'))])
    experience_lower = IntegerField(
            '最低工作年限', validators=[NumberRange(min=0, max=40, 
                                        message=('无效的输入'))], default=0)
    experience_upper = IntegerField(
            '最高工作年限', validators=[NumberRange(min=0, max=40, 
                                        message=('无效的输入'))], default=0)
    education = StringField(
            '学历需求', validators=[Length(2, 16)], default='学历不限')
    tags = StringField(
            '标签 (请使用空格分割)', 
            validators=[Optional(), Length(2, 128)])
    intro = TextAreaField('职位简介') 
    submit = SubmitField('提交')

    def create_job(self):
        job = Job()
        user = User.query.filter_by(username=current_user.username).first()
        self.populate_obj(job)
        job.company = user
        db.session.add(job)
        db.session.commit()
        return job

    def validate_salary_lower(self, field):
        if field.data >= self.salary_upper.data:
            raise ValidationError('错误的输入')
        
    def validate_experience_lower(self, field):
        if field.data > self.experience_upper.data:
            raise ValidationError('错误的输入')


class EditJobForm(PostJobForm):

    def update_job(self, job):
        self.populate_obj(job)
        db.session.add(job)
        db.session.commit()


class AdminEditUserForm(EditUserForm):
    username = StringField(
            '用户名', validators=[DataRequired(), Length(3, 24)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    role = IntegerField('权限', validators=[Optional(), AnyOf([10, 20, 30])])
    password = PasswordField(
            '密码', validators=[Optional(), Length(6, 24)])
    repeat_password = PasswordField(
            '重复密码', validators=[EqualTo('password')])
    submit = SubmitField('提交')

    def validate_email(self, field):
        if field.data != self.email.data and User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已存在')

    def validate_username(self, field):
        if field.data != self.username.data and User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')
    

class AdminUserInfoForm(UserInfoForm):
    name = StringField(
            '真实姓名', validators=[Optional(), Length(3, 64)])
    phone_number = StringField(
            '手机号', validators=[Optional(), 
                Regexp('^1[3578]\d{9}$', message="手机号格式不正确")])
    experience = IntegerField('工作年限', validators=[Optional()])
    resume = StringField('简历地址', validators=[Optional(), URL()])
    submit = SubmitField('提交')

    def validate_phone_number(self, field):
        if field.data != self.phone_number.data and (
            UserInfo.query.filter_by(phone_number=field.data).first()):
            raise ValidationError('手机号已存在')

    def update_userinfo(self, user_info, user):
        self.populate_obj(user_info)
        user_info.user = user
        db.session.add(user_info)
        db.session.commit()
        return user_info

