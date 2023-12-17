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


    


                           
