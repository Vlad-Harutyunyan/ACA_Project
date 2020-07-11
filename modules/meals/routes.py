from flask import (
    Blueprint,
    url_for,
    redirect,
    render_template
)


meals = Blueprint(
    'meals',
    __name__,
    template_folder='templates',
    url_prefix='/meal'
)


@meals.route('/')
def test_route():
    return render_template('main_page.html')

