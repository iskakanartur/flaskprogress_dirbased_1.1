from flask import render_template
from app import app, db
from app.models import *            
from app.helper_functions import *  ## pay attention to imports  -- from helper_functions import * won't work 
from flask import Flask, render_template, request, redirect, url_for, flash

from sqlalchemy import and_      ### to combine db queries in past Mo to su function 
from calendar import monthrange  ### to combine db queries in past Mo to su function 
from datetime import date, datetime, timedelta


######## For Multi Plot Progress Bar
from app.visualization import *

from sqlalchemy import cast, Date




from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields  import DateTimeLocalField
from wtforms.validators import DataRequired
from datetime import datetime

from wtforms.fields import DateTimeLocalField






############################################### Views for Goal Tracking App ###################################

@app.route('/')
def index():
    learn_query_all = Learn.query.order_by(Learn.date_added.asc()).all()


    return render_template('index.html', learn_query_all=learn_query_all )
                           



###### ADD LEARNING SESSION or a TASK 
@app.route('/add/', methods = ['POST'])
def insert_subject():
    if request.method =='POST':
        session = Learn(
            subject =    request.form.get('subject'),
            duration =   request.form.get('duration'),
            comment =    request.form.get('comment'),
            date_added = request.form.get('date_added')
            

        )
        db.session.add(session)
        db.session.commit()
        flash("Ձեր գոնումը հայտնվեց շտեմարանում, Շնորհակալութոյւն")
        return redirect(url_for('index'))
    



##### UPDATE
@app.route('/update/', methods = ['POST'])
def update():
    if request.method == "POST":
        my_data = Learn.query.get(request.form.get('id'))

        my_data.subject = request.form['subject']
        my_data.duration = request.form['duration']
        my_data.date_added = request.form['date_added']
        my_data.comment = request.form['comment']
        
        db.session.commit()
        flash("Գնումը Գրանցված է")
        return redirect(url_for('index'))
    

##### Set Weekly Learning Goal from Navbar
@app.route('/week_goal/', methods = ['POST'])
def wkly_goal():
    if request.method =='POST':
    
        goal = various(
            datetime = request.form.get('datetime'),
            week_goal = request.form.get('week_goal')
        )
        db.session.add(goal)
        db.session.commit()
        flash("Ձեր գոնումը հայտնվեց շտեմարանում, Շնորհակալութոյւն")
        return redirect(url_for('index'))
    




#####  LAST WEEK sunday to monday
## see helper_functions for the query 
@app.route('/mo_su')
def past_mo_to_sun ():    

    mo_to_sun = mo_su_query()

    return render_template('mo_su.html', mo_to_sun=mo_to_sun )





#### Multi Plot Progress Bar 
@app.route('/multi_progress_plot')
def multi_progress_plot ():

    multi_progress_plot_viz () ## see visualization.py 
    sun_mon_plot = mo_su_query()
    

    return render_template('multi_progress_plot.html', 
                           url='/static/images/multi_progress_plot.png', sun_mon_plot= sun_mon_plot)




############################################## Views for Goal Fitness  App ###################################
@app.route('/fitness_overview')
def fitness_overview():

    fit_query_all = fit.query.order_by(fit.date_added.asc()).all()


    return render_template('fit_overview.html', fit_query_all=fit_query_all )



##### ADD FITNESS EVENT
@app.route('/add_fitness/', methods = ['POST'])
def insert_fitness():
    if request.method =='POST':
        session = fit(
            exercise =    request.form.get('exercise'),
            count =   request.form.get('count'),
            comment =    request.form.get('comment'),
            date_added = request.form.get('date_added')
            

        )
        db.session.add(session)
        db.session.commit()
        flash("Ձեր գոնումը հայտնվեց շտեմարանում, Շնորհակալութոյւն")
        return redirect(url_for('fitness_overview'))


##### UPDATE FIT
@app.route('/update_fitness/', methods = ['POST'])
def update_fitness():
    if request.method == "POST":
        my_data = fit.query.get(request.form.get('id'))

        my_data.exercise = request.form['exercise']
        my_data.count = request.form['count']
        my_data.comment = request.form['comment']
        my_data.date_added = request.form['date_added']
        
        
        db.session.commit()
        flash("Գնումը Գրանցված է")
        return redirect(url_for('fitness_overview'))
        # return redirect(url_for('index'))
        



############################################## Views for Nutrition  App ###################################
## Class NutritionForm(FlaskForm) and WTF is used for the ability to 
## Manually insert datetime If a meal was eaten at earlier time than Database NOW()


class NutritionForm(FlaskForm):
    meal = StringField('Meal', validators=[DataRequired()])
    drink = StringField('Drink', validators=[DataRequired()])
    drink_count = StringField('Drink Count', validators=[DataRequired()])
    date_added = DateTimeLocalField('Date Added', format='%Y-%m-%dT%H:%M:%S', default=datetime.now, render_kw={"placeholder": "Optional"})
    comment = StringField('Comment')
    submit = SubmitField('Add Nutrition')

@app.route('/nutrition_index')
def nutrition_index():
    nutrition_query_all = eat.query.order_by(eat.date_added.asc()).all()
    return render_template('nutrition_index.html', nutrition_query_all=nutrition_query_all )

@app.route('/add_nutrition/', methods = ['POST'])
def insert_nutrition():
    exists = db.session.query(
    db.session.query(eat).filter(cast(eat.date_added, Date) >= datetime.now().date()).exists()).scalar()

    if exists:
        if request.method =='POST':
            session = eat(
                meal =    request.form.get('meal'),
                drink =   request.form.get('drink'),
                drink_count =   request.form.get('drink_count'),
                # or is used to insert now() if the field is empty
                date_added=request.form.get('date_added') or func.now(), 
                comment =    request.form.get('comment')
                    )
            db.session.add(session)
            db.session.commit()
            return redirect(url_for('nutrition_index'))
        
    else:
        
        if request.method =='POST':
            session = eat(
                meal =    request.form.get('meal'),
                drink =   request.form.get('drink'),
                drink_count =   request.form.get('drink_count'),
                date_added = request.form.get('date_added')  or func.now(),
                comment =    request.form.get('comment')
                    )
            db.session.add(session)
            db.session.commit()
            query_fasted_time ()
            return redirect(url_for('nutrition_index'))

    

##### UPDATE NUTRITION !!!!!!!!!! ATTENTION ERROR HANDLING !!!!!!
            
@app.route('/update_nutrition/', methods = ['POST'])
def update_nutrition():
    if request.method == "POST":
        # my_data = eat.query.get(request.form('id')) ## This is index methid square vs just brackets
        my_data = eat.query.get( request.form['id'] ) ## Compare this to the index


        my_data.meal = request.form['meal']
        my_data.drink = request.form['drink']
        my_data.drink_count = request.form['drink_count']
        my_data.date_added = request.form['date_added']
        my_data.comment = request.form['comment']
        
        db.session.commit()
        flash("Գնումը Գրանցված է")
        return redirect(url_for('nutrition_index'))
    

#### Delete Nutrition 
@app.route('/delete_nutrition/<int:id>', methods=['POST'])
def delete_nutrition(id):
    eat_to_delete = eat.query.get_or_404(id)
    if request.method == 'POST':
        if request.form.get('confirm') == 'Yes':
            db.session.delete(eat_to_delete)
            db.session.commit()
            flash('Row deleted successfully', 'success')
        else:
            flash('Deletion cancelled', 'warning')
        return redirect(url_for('nutrition_index'))
    return render_template('delete_nutrition.html', eat_to_delete=eat_to_delete)

    


############################################## Views for BODY  App ###################################
    
@app.route('/body_index')
def body_index():

    body_query_all = body.query.order_by(body.date_added.asc()).all()

    return render_template('body_index.html', body_query_all=body_query_all )

    
##### ADD  BODY PARAMS
@app.route('/add_body/', methods = ['POST'])
def insert_body():
    if request.method =='POST':
        session = body(
            weight =    request.form.get('weight'),
            weist =     request.form.get('weist'),
            bicep =     request.form.get('bicep'),
            glucose =   request.form.get('glucose'),
            date_added = request.form.get('date_added'),
            comment =    request.form.get('comment')
        )
        db.session.add(session)
        db.session.commit()
        flash("Ձեր գոնումը հայտնվեց շտեմարանում, Շնորհակալութոյւն")
        return redirect(url_for('body_index'))


##### UPDATE BODY
@app.route('/update_body/', methods = ['POST'])
def update_body():
    if request.method == "POST":
        my_data = body.query.get( request.form['id'] ) ## Compare this to the index

        my_data.weight = request.form['weight']
        my_data.weist = request.form['weist']
        my_data.bicep = request.form['bicep']
        my_data.glucose = request.form['glucose']
        
        my_data.date_added = request.form['date_added']
        my_data.comment = request.form['comment']
        
        
        db.session.commit()
        flash("Գնումը Գրանցված է")
        return redirect(url_for('body_index'))
        # return redirect(url_for('index'))
    

def lo ():
    exists = db.session.query(
        db.session.query(eat).filter(cast(eat.date_added, Date) >= datetime.now().date()).exists()).scalar()
    print (exists)
        



    
    


    

    

    




    


                           
