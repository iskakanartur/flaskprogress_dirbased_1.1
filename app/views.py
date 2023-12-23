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
    
@app.route('/nutrition_overview')
def nutrition_overview():

    nutrition_query_all = eat.query.order_by(eat.date_added.asc()).all()


    return render_template('nutrition_overview.html', nutrition_query_all=nutrition_query_all )



##### ADD NUTRITION 
## ADD FUnctionality to trigger   query_fasted_time ()
## IF It is the first record of today RUn the function.
@app.route('/add_nutrition/', methods = ['POST'])
def insert_nutrition():

    # Check if there are any records in the Eat model as of the current time
    # Create a subquery from the Select object
    #exists = db.session.query(eat.query.filter(cast(eat.date_added, Date) >= datetime.now().date())).exists()

    exists = db.session.query(
    db.session.query(eat).filter(cast(eat.date_added, Date) >= datetime.now().date()).exists()).scalar()

    if exists:
    # No need to trigger Fasting Time Calc function query_fasted_time ()
        if request.method =='POST':
            session = eat(
                meal =    request.form.get('meal'),
                drink =   request.form.get('drink'),
                drink_count =   request.form.get('drink_count'),
                date_added = request.form.get('date_added'),
                comment =    request.form.get('comment')
                    )
            db.session.add(session)
            db.session.commit()
            flash("Ձեր գոնումը հայտնվեց շտեմարանում, Շնորհակալութոյւն")
            return redirect(url_for('nutrition_overview'))
        
    else: # Calculate Fasting Time
        
        if request.method =='POST':
            session = eat(
                meal =    request.form.get('meal'),
                drink =   request.form.get('drink'),
                drink_count =   request.form.get('drink_count'),
                date_added = request.form.get('date_added'),
                comment =    request.form.get('comment')
                    )
            db.session.add(session)
            db.session.commit()
            flash("Fasting Time Calculated")
            query_fasted_time () # Calculate Fasting Time
        
        
            return redirect(url_for('nutrition_overview'))
        
         

        




       
    

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
        return redirect(url_for('nutrition_overview'))
    
    


    

    

    




    


                           
