'''
用户蓝图
'''

from flask import (Blueprint, render_template, flash, redirect, 
                   url_for, abort, request, current_app)
from flask_login import current_user
from jobplus.decorators import user_required
from jobplus.models import User, UserInfo, SendCV, Job, db
from jobplus.forms import UserInfoForm, EditUserForm


user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/')
@user_required
def index():
    return render_template('user/index.html')

@user_bp.route('/info')
@user_required
def userinfo():
    user = User.query.filter_by(username=current_user.username).first()
    return render_template('user/user_info.html', user=user)

@user_bp.route('/edit-userinfo', methods=['GET', 'POST'])
@user_required
def edit_userinfo():
    user = User.query.filter_by(username=current_user.username).first()
    user_info = user.user_info
    form = UserInfoForm(obj=user_info)
    if not user_info:
        if form.validate_on_submit():
            form.create_userinfo(user)
            flash('信息更新成功！', 'success')
            return redirect(url_for('.index'))
    else:
        if form.validate_on_submit():
            form.update_userinfo(user_info)
            flash('信息更新成功！', 'success')
            return redirect(url_for('.index'))
    return render_template('user/edit_userinfo.html', form=form)

@user_bp.route('/edit-user', methods=['GET', 'POST'])
@user_required
def edit_user():
    user = User.query.filter_by(username=current_user.username).first()
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        form.update_user(user)
        flash('信息更新成功！', 'success')
        return redirect(url_for('.index'))
    return render_template('user/edit_user.html', form=form)
        
@user_bp.route('/send-cv/<int:job_id>/<int:company_id>', methods=['GET', 'POST'])
@user_required
def send_cv(job_id, company_id):
    job = Job.query.filter_by(id=job_id).first_or_404()
    user = User.query.filter_by(username=current_user.username).first()
    company = User.query.filter_by(id=company_id).first()
    send_cv = SendCV() 
    send_cv.sender = user
    send_cv.job = job
    send_cv.receiver = company
    db.session.add(send_cv)
    db.session.commit()
    flash('简历投递成功！', 'success')
    return redirect(url_for('job.jobs'))
    
@user_bp.route('/sent-cv')
@user_required
def sent_cv():
    page = request.args.get('page', default=1, type=int)
    pagination = SendCV.query.filter_by(
            sender_id=current_user.id).paginate(
                page=page,
                per_page=current_app.config['COMPANY_PER_PAGE'],
                error_out=False
        )
    return render_template('user/sent_cv.html', 
            pagination=pagination)

@user_bp.route('/del-cv/<int:job_id>', methods=['GET', 'POST'])
@user_required
def del_cv(job_id):
    send_cv = SendCV.query.filter_by(job_id=job_id, 
            sender_id=current_user.id).first_or_404()
    db.session.delete(send_cv)
    db.session.commit()
    return redirect(url_for('.sent_cv'))

@user_bp.route('/unread-cv')
@user_required
def unread_cv():
    page = request.args.get('page', default=1, type=int)
    pagination = SendCV.query.filter_by(
            sender_id=current_user.id, status=10).paginate(
                page=page,
                per_page=current_app.config['COMPANY_PER_PAGE'],
                error_out=False
        )
    return render_template('user/unread_cv.html', 
            pagination=pagination)

@user_bp.route('/accept-cv')
@user_required
def accept_cv():
    page = request.args.get('page', default=1, type=int)
    pagination = SendCV.query.filter_by(
            sender_id=current_user.id, status=30).paginate(
                page=page,
                per_page=current_app.config['COMPANY_PER_PAGE'],
                error_out=False
        )
    return render_template('user/accept_cv.html', 
            pagination=pagination)

@user_bp.route('/refuse-cv')
@user_required
def refuse_cv():
    page = request.args.get('page', default=1, type=int)
    pagination = SendCV.query.filter_by(
            sender_id=current_user.id, status=20).paginate(
                page=page,
                per_page=current_app.config['COMPANY_PER_PAGE'],
                error_out=False
        )
    return render_template('user/refuse_cv.html', 
            pagination=pagination)

