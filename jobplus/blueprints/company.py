'''
企业蓝图
'''

from flask import (Blueprint, render_template, flash, redirect, url_for,
                   request, current_app, abort, g)
from flask_login import current_user
from jobplus.decorators import company_required
from jobplus.models import User, CompanyInfo, Job, db, SendCV
from jobplus.forms import CompanyInfoForm, EditCompanyForm, PostJobForm, EditJobForm


company_bp = Blueprint('company', __name__, url_prefix='/company')

@company_bp.route('/')
@company_required
def index():
    g.unread_num = len(SendCV.query.filter_by(receiver_id=current_user.id, 
                 status=10).all())
    return render_template('company/index.html', unread_num=g.unread_num)

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

@company_bp.route('/unread-cv')
@company_required
def unread_cv():
    page = request.args.get('page', default=1, type=int)
    pagination = SendCV.query.filter_by(
            receiver_id=current_user.id, status=10).paginate(
                page=page,
                per_page=current_app.config['COMPANY_PER_PAGE'],
                error_out=False
        )
    return render_template('company/unread_cv.html', 
            pagination=pagination)

@company_bp.route('/accept-cv')
@company_required
def accept_cv():
    page = request.args.get('page', default=1, type=int)
    pagination = SendCV.query.filter_by(
            receiver_id=current_user.id, status=30).paginate(
                page=page,
                per_page=current_app.config['COMPANY_PER_PAGE'],
                error_out=False
        )
    return render_template('company/accept_cv.html', 
            pagination=pagination)

@company_bp.route('/refuse-cv')
@company_required
def refuse_cv():
    page = request.args.get('page', default=1, type=int)
    pagination = SendCV.query.filter_by(
            receiver_id=current_user.id, status=20).paginate(
                page=page,
                per_page=current_app.config['COMPANY_PER_PAGE'],
                error_out=False
        )
    return render_template('company/refuse_cv.html', 
            pagination=pagination)

@company_bp.route('/refuse/<int:job_id>/<int:user_id>', methods=['GET', 'POST'])
@company_required
def refuse(job_id, user_id):
    send_cv = SendCV.query.filter_by(job_id=job_id, sender_id=user_id).first_or_404()
    send_cv.status = 20
    db.session.add(send_cv)
    db.session.commit()
    return redirect(url_for('.unread_cv'))

@company_bp.route('/accept/<int:job_id>/<int:user_id>', methods=['GET', 'POST'])
@company_required
def accept(job_id, user_id):
    send_cv = SendCV.query.filter_by(job_id=job_id, sender_id=user_id).first_or_404()
    send_cv.status = 30
    db.session.add(send_cv)
    db.session.commit()
    return redirect(url_for('.accept_cv'))


