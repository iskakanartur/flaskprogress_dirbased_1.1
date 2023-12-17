from flask import render_template
from app import app, db
from app.models import *
from flask import Flask, render_template, request, redirect, url_for, flash

# @app.route('/')
# def index():
    # users = User.query.all()
    # return render_template('base.html', users=users)



@app.route('/')
def index():
    learn_query_all = Learn.query.order_by(Learn.date_added.asc()).all()


    return render_template('index.html', learn_query_all=learn_query_all )
                           



###### ADD
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
    


                           
