from flask_login import current_user
from jobplus.models import SendCV


def count_unread():
    unread_num = len(SendCV.query.filter_by(receiver_id=current_user.id,
                     status=10).all())
    return unread_num

