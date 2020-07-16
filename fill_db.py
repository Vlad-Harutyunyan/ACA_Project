from lib.db import db
from scripts.api import meals, ingredient, meal_ingredient, area, categories
import pandas as pd
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy


if __name__ == "__main__":

    # Program entry point
    dbms = db.MyDatabase(db.SQLITE, dbname='mydb_new.sqlite')
    # Create Tables
    dbms.create_db_tables()

    for i in meals:
        query=f'INSERT INTO meals (id, name, category_id, area_id, like_count, instructions,img_link, tags,video_link) VALUES {tuple(i)};'
        dbms.sample_insert(query)
        print(i)

    for i in area:
        query = f'INSERT INTO area (id, name) VALUES {tuple(i)};'
        dbms.sample_insert(query)


    for i in ingredient:
        query = f'INSERT INTO ingredient (id, name, description) VALUES {tuple(i)};'
        dbms.sample_insert(query)


    for i in categories:
        query = f'INSERT INTO categories (id, name, img_link, description) VALUES {tuple(i)};'
        dbms.sample_insert(query)

    # for i in meal_ingredient:
    #     query = f'INSERT INTO meal_ingredient (meal_id, ingredient_id) VALUES {tuple(i)}'
    #     dbms.sample_insert(query)



    # dbms.sample_delete('MEALS')
    # dbms.sample_delete('AREA')

    # df = pd.DataFrame(meals)
    # df.to_excel("meals.xlsx")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb_new.sqlite'
db = SQLAlchemy(app)


@app.route('/meals/')
def init_meals():

    query = f'SELECT * FROM meals '
    data=dbms.sample_query(query)
    for i in data:
        print(i)

    return render_template("init_meals.html", data=data)



@app.route('/category/<name>')
def category(name):
    query = f'SELECT name, img_link,description FROM categories WHERE name = "{name}"'
    data=dbms.sample_query(query)

    name=f"{name.lower()}.png"


    return render_template("category.html", data=data,name=name)

#
@app.route('/meals/<name>')
def meals(name):

    query = f'SELECT name,  area_id, instructions, img_link FROM meals WHERE name = "{name}"'
    data=dbms.sample_query(query)

    return render_template("meals.html", data=data)

if __name__=="__main__":
    app.run(debug = True, port = 8080)
