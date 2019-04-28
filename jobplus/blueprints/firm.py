'''
Job蓝图
'''

from flask import (Blueprint, render_template, flash, redirect, url_for,
                   request, current_app)
from jobplus.models import Job
from jobplus.forms import *


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

@firm_bp.route('/<int:
