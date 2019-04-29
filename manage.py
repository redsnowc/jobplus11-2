from jobplus.app import create_app
from flask import render_template


app = create_app('development')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404
