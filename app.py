from flask import (
    Flask,
    g,
    url_for,
    redirect,
    render_template
)

from modules.meals.routes import meals
from modules.users.routes import users



app = Flask(__name__)
app.config.from_pyfile('config.py')

app.register_blueprint(meals)
app.register_blueprint(users)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
