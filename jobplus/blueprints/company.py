'''
企业蓝图
'''

from flask import (Blueprint, render_template, flash, redirect, url_for,
                   request, current_app, abort)
from flask_login import current_user
from jobplus.decorators import company_required
from jobplus.models import User, CompanyInfo, Job, db
from jobplus.forms import CompanyInfoForm, EditCompanyForm, PostJobForm, EditJobForm


company_bp = Blueprint('company', __name__, url_prefix='/company')

@company_bp.route('/')
@company_required
def index():
    return render_template('company/index.html')

@company_bp.route('/info')
@company_required
def company_info():
    user = User.query.filter_by(username=current_user.username).first()
    return render_template('company/company_info.html', user=user)

@company_bp.route('/edit-companyinfo', methods=['GET', 'POST'])
@company_required
def edit_companyinfo():
    user = User.query.filter_by(username=current_user.username).first()
    company_info = user.company_info
    form = CompanyInfoForm(obj=company_info)
    if not company_info:
        if form.validate_on_submit():
            form.create_companyinfo(user)
            flash('信息更新成功！', 'success')
            return redirect(url_for('.company_info'))
    else:
        if form.validate_on_submit():
            form.update_companyinfo(company_info)
            flash('信息更新成功！', 'success')
            return redirect(url_for('.company_info'))
    return render_template('company/edit_companyinfo.html', form=form)

@company_bp.route('/edit-company', methods=['GET', 'POST'])
@company_required
def edit_company():
    user = User.query.filter_by(username=current_user.username).first()
    form = EditCompanyForm(obj=user)
    if form.validate_on_submit():
        form.update_user(user)
        flash('信息更新成功！', 'success')
        return redirect(url_for('.company_info'))
    return render_template('company/edit_company.html', form=form)
        
@company_bp.route('/post-job', methods=['GET', 'POST'])
@company_required
def post_job():
    form = PostJobForm()
    if form.validate_on_submit():
        form.create_job()
        flash('职位发布成功！', 'success')
        return redirect(url_for('.index'))
    return render_template('company/post_job.html', form=form)

@company_bp.route('/jobs')
@company_required
def jobs():
    user = User.query.filter_by(username=current_user.username).first()
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.with_parent(user).paginate(
                page=page,
                per_page=current_app.config['COMPANY_PER_PAGE'],
                error_out=False
        )
    return render_template('company/jobs.html', pagination=pagination)

@company_bp.route('/edit-job/<int:job_id>', methods=['GET', 'POST'])
@company_required
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.company.username == current_user.username:
        form = EditJobForm(obj=job)
        if form.validate_on_submit():
            form.update_job(job)
            flash('职位更新成功', 'success')
            return redirect(url_for('company.index'))
    else:
        abort(404)
    return render_template('company/edit_job.html', form=form, job=job)

@company_bp.route('/del-job/<int:job_id>', methods=['GET', 'POST'])
@company_required
def del_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.company.username == current_user.username:
        db.session.delete(job)
        db.session.commit()
        flash('职位已删除', 'success')
        return redirect(url_for('company.index'))
    else:
        abort(404)
