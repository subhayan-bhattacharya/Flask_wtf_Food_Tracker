__package__ = "application.views"

from .. import app
from ..database import get_db
from flask import render_template,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import InputRequired
from collections import defaultdict
from datetime import datetime


@app.route('/view/<date>',methods=["POST","GET"])
def view(date):
    db = get_db()
    cur = db.execute("select id,entry_date from log_date where entry_date = ?", [date])
    log_results = cur.fetchone()
    d = datetime.strptime(str(log_results['entry_date']), '%Y%m%d')
    pretty_date = datetime.strftime(d, '%B %d, %Y')
    cur = db.execute("select id,name from food")
    food_items = cur.fetchall()
    food_list = [(str(food['id']),food['name']) for food in food_items]

    class FoodForm(FlaskForm):
        pass

    setattr(FoodForm,'food',SelectField('food',choices=food_list,default=food_list[0],validators=[InputRequired()]))

    food_form = FoodForm()

    if food_form.validate_on_submit():
        food_selected = food_form.food.data
        log_date_id = log_results['id']
        db.execute("insert into food_date(food_id,log_date_id) values(?,?)", [food_selected,log_date_id])
        db.commit()
        return redirect(url_for('view',date=date))


    log_cur = db.execute('''select name,protein,carbohydrates,fat,calories 
                            from food where id in 
                            (select food_id from food_date where log_date_id = 
                            (select id from log_date where entry_date = ?))''',[date])
    food_details = log_cur.fetchall()
    total = defaultdict(int)
    for r in food_details:
        total['protein'] = total['protein'] + r['protein']
        total['carbohydrates'] = total['carbohydrates'] + r['carbohydrates']
        total['calories'] = total['calories'] + r['calories']
        total['fat'] = total['fat'] + r['fat']
    return render_template('day.html',date=pretty_date,food_items=food_items,passed_date=date,food_details=food_details,total=total,form=food_form)
