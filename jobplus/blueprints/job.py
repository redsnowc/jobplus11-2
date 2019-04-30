'''
Job蓝图
'''

from flask import (Blueprint, render_template, flash, redirect, url_for,
                   request, current_app)
from jobplus.models import Job, SendCV, User
from flask_login import current_user
from jobplus.forms import *


job_bp = Blueprint('job', __name__, url_prefix='/jobs')

@job_bp.route('/')
def jobs():
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.paginate(
            page=page,
            per_page=current_app.config['HOME_PER_PAGE'],
            error_out=False
        )
    return render_template('jobs/jobs.html', pagination=pagination)

@job_bp.route('/<int:job_id>')
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    sendcv = SendCV()
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id).first()
        return render_template('jobs/detail.html', job=job, 
                                sendcv=sendcv, user=user)
    else:
        return render_template('jobs/detail.html', job=job)
