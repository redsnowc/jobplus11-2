'''
企业蓝图
'''

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user
from jobplus.decorators import company_required
from jobplus.models import User, CompanyInfo
from jobplus.forms import CompanyInfoForm, EditCompanyForm


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
        
