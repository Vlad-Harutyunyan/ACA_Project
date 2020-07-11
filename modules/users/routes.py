from flask import (
    Blueprint,
    url_for,
    redirect,
    render_template
)


users = Blueprint(
    'users',
    __name__,
    template_folder='templates',
    url_prefix='/user'
)


@users.route('/')
def test_route():
    return render_template('main_page.html')

