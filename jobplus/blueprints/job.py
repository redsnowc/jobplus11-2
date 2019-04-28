'''
Job蓝图
'''

from flask import (Blueprint, render_template, flash, redirect, url_for,
                   request, current_app)
from jobplus.models import Job
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
