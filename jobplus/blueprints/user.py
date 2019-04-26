'''
用户蓝图
'''

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from jobplus.models import User, UserInfo
from jobplus.forms import UserInfoForm, EditUserForm


user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/')
@login_required
def index():
    user = User.query.filter_by(username=current_user.username).first()
    return render_template('user/index.html', user=user)

@user_bp.route('/edit-userinfo', methods=['GET', 'POST'])
@login_required
def edit_userinfo():
    user = User.query.filter_by(username=current_user.username).first()
    user_info = user.user_info
    form = UserInfoForm(obj=user_info)
    if form.validate_on_submit():
        form.update_userinfo(user)
        flash('信息更新成功！', 'success')
        return redirect(url_for('.index'))
    return render_template('user/edit_userinfo.html', form=form)

@user_bp.route('/edit-user', methods=['GET', 'POST'])
@login_required
def edit_user():
    user = User.query.filter_by(username=current_user.username).first()
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        form.update_user(user)
        flash('信息更新成功！', 'success')
        return redirect(url_for('.index'))
    return render_template('user/edit_userinfo.html', form=form)
        
