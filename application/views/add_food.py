__package__ = "application.views"

from .. import app
from ..database import get_db
from flask import render_template,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

class FoodCategoryForm(FlaskForm):
    food_name = StringField('Food name',validators=[InputRequired()])
    protein = StringField('Protein',validators=[InputRequired()])
    carbohydrates = StringField('Carbohydrates',validators=[InputRequired()])
    fat = StringField('Fat',validators=[InputRequired()])

@app.route('/add_food',methods=["GET","POST"])
def add_food():
    db = get_db()
    food_category_form = FoodCategoryForm()

    if food_category_form.validate_on_submit():
        name = food_category_form.food_name.data
        protein = int(food_category_form.protein.data)
        carbohydrates = int(food_category_form.carbohydrates.data)
        fat = int(food_category_form.fat.data)
        print name,protein,carbohydrates,fat
        calories = protein * 4 + carbohydrates * 4 + fat * 9
        db.execute("insert into food(name,protein,carbohydrates,fat,calories) values(?,?,?,?,?)",[name,protein,
        carbohydrates,fat,calories])
        db.commit()
        return redirect(url_for('add_food'))

    cur = db.execute('select name,protein,carbohydrates,fat,calories from food')
    results = cur.fetchall()
    return render_template('add_food.html',results=results,form=food_category_form)