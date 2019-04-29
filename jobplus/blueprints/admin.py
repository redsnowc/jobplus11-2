'''
Admin蓝图
'''

from flask import (Blueprint, render_template, flash, redirect, url_for,
                   request, current_app, abort)
from jobplus.decorators import admin_required
from jobplus.models import User, CompanyInfo, Job, db, UserInfo
from jobplus.forms import (CompanyInfoForm, EditCompanyForm, EditJobForm, 
                           AdminEditUserForm, AdminUserInfoForm)


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@admin_required
def index():
    return render_template('admin/index.html')

@admin_bp.route('/jobs')
@admin_required
def jobs():
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.paginate(
            page=page,
            per_page=current_app.config['COMPANY_PER_PAGE'],
            error_out=False
        )
    return render_template('admin/jobs.html', pagination=pagination)

@admin_bp.route('/edit-job/<int:job_id>', methods=['GET', 'POST'])
@admin_required
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    form = EditJobForm(obj=job)
    if form.validate_on_submit():
        form.update_job(job)
        flash('职位更新成功', 'success')
        return redirect(url_for('admin.jobs'))
    return render_template('admin/edit_job.html', form=form, job=job)

@admin_bp.route('/del-job/<int:job_id>', methods=['GET', 'POST'])
@admin_required
def del_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash('职位已删除', 'success')
    return redirect(url_for('admin.jobs'))

@admin_bp.route('/users')
@admin_required
def users():
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.filter_by(role=10).paginate(
            page=page,
            per_page=current_app.config['COMPANY_PER_PAGE'],
            error_out=False
        )
    return render_template('admin/users.html', pagination=pagination)

@admin_bp.route('/edit-user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = AdminEditUserForm(obj=user)
    if form.validate_on_submit():
        form.update_user(user)
        flash('用户更新成功', 'success')
        if user.role == 10:
            return redirect(url_for('.users'))
        else:
            return redirect(url_for('.companies'))
    return render_template('admin/edit_user.html', form=form, user=user)
    
@admin_bp.route('/edit-userinfo/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_userinfo(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 10:
        user_info = user.user_info
        form = AdminUserInfoForm(obj=user_info)
    else:
        abort(404)
    if form.validate_on_submit():
        if user_info:
            form.update_userinfo(user_info, user)
            flash('用户信息更新成功', 'success')
            return redirect(url_for('.users'))
        else:
            user_info = UserInfo()
            form.update_userinfo(user_info, user)
            flash('用户信息更新成功', 'success')
            return redirect(url_for('.users'))
    return render_template('admin/edit_userinfo.html', form=form, user=user)

@admin_bp.route('/del-user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def del_user(user_id):
    user = User.query.get_or_404(user_id)
    role = user.role
    db.session.delete(user)
    db.session.commit()
    flash('用户已删除', 'success')
    if role == 10:
        return redirect(url_for('.users'))
    else:
        return redirect(url_for('.companies'))

@admin_bp.route('/companies')
@admin_required
def companies():
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.filter_by(role=20).paginate(
            page=page,
            per_page=current_app.config['COMPANY_PER_PAGE'],
            error_out=False
        )
    return render_template('admin/companies.html', pagination=pagination)

@admin_bp.route('/edit-companyinfo/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_companyinfo(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 20:
        company_info = user.company_info
        form = CompanyInfoForm(obj=company_info)
    else:
        abort(404)
    if form.validate_on_submit():
        if company_info:
            form.update_companyinfo(company_info)
            flash('企业信息更新成功', 'success')
            return redirect(url_for('.companies'))
        else:
            form.create_companyinfo(user)
            flash('企业信息更新成功', 'success')
            return redirect(url_for('.companies'))
    return render_template('admin/edit_companyinfo.html',
                           form=form, user=user)

