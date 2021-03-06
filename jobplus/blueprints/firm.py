'''
Firm蓝图
'''

from flask import (Blueprint, render_template, flash, redirect, url_for,
                   request, current_app, abort)
from jobplus.models import Job, User


firm_bp = Blueprint('firm', __name__, url_prefix='/firms')

@firm_bp.route('/')
def firms():
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.filter_by(role=20).paginate(
            page=page,
            per_page=current_app.config['HOME_PER_PAGE'],
            error_out=False
        )
    return render_template('firms/firms.html', pagination=pagination)

@firm_bp.route('/<int:user_id>')
def detail(user_id):
    firm = User.query.get_or_404(user_id)
    if firm.role != 20:
        abort(404)
    else:
        jobs_num = len(Job.query.filter_by(company_id=firm.id, 
            status=Job.ONLINE).all())
        return render_template('firms/detail.html', firm=firm, jobs_num=jobs_num)

@firm_bp.route('/<int:user_id>/jobs')
def jobs(user_id):
    firm = User.query.get_or_404(user_id)
    if firm.role != 20:
        abort(404)
    else:
        jobs = Job.query.filter_by(company_id=firm.id, status=Job.ONLINE).all()
        return render_template('firms/jobs.html', jobs=jobs, firm=firm)
