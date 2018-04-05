__package__ = "application.views"

from .. import app
from ..database import get_db
from flask import render_template,redirect,url_for
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired
from collections import defaultdict
from datetime import datetime

class IndexForm(FlaskForm):
    newDate = DateField('New Day',validators=[InputRequired()],format='%Y-%m-%d')

@app.route('/',methods=["GET","POST"])
def index():
    db = get_db()
    indexform = IndexForm()
    if indexform.validate_on_submit():
        entered_date = str(indexform.newDate.data)
        formated_entered_date = datetime.strptime(entered_date,'%Y-%m-%d')
        final_database_date = datetime.strftime(formated_entered_date,'%Y%m%d')
        db.execute("insert into log_date (entry_date) values (?)",[final_database_date])
        db.commit()
        return redirect(url_for('index'))

    cur = db.execute('select * from log_date order by entry_date DESC ')
    results = cur.fetchall()
    pretty_results = []
    dates = []

    for i in results:
        single_date = {}
        curr = db.execute('''select protein,carbohydrates,fat,calories 
                              from food where id in 
                              (select food_id from food_date where log_date_id = 
                              (select id from log_date where entry_date = ?))''',[i['entry_date']])

        food_results = curr.fetchall()
        total = defaultdict(int)
        for food in food_results:
            total['protein'] = total['protein'] + food['protein']
            total['carbohydrates'] = total['carbohydrates'] + food['carbohydrates']
            total['fat'] = total['fat'] + food['fat']
            total['calories'] = total['calories'] + food['calories']

        d = datetime.strptime(str(i['entry_date']),'%Y%m%d')
        single_date['pretty_entry_date'] = datetime.strftime(d,'%B %d, %Y')
        single_date['entry_date'] = i['entry_date']
        single_date['totals'] = total
        pretty_results.append(single_date)

    return render_template('home.html',results=pretty_results,form=indexform)

