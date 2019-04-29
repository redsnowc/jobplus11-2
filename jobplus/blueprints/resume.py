from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user
from jobplus.models import Resume, User


resume_bp = Blueprint('resume', __name__, url_prefix='/resume')

@resume_bp.route('/send-resume')
def send_resume()
