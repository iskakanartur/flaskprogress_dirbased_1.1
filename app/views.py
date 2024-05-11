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

from sqlalchemy import distinct





from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields  import DateTimeLocalField
from wtforms.validators import DataRequired
from datetime import datetime

from wtforms.fields import DateTimeLocalField


from flask import Flask, render_template
# from flask_matplotlib import Matplotlib






############################################### Views for Goal Tracking App ###################################

#@app.route('/')
#def index():
    #learn_query_all = learn.query.order_by(learn.date_added.asc()).all()


    #return render_template('index.html', learn_query_all=learn_query_all )

PER_PAGE = 10  # Adjust the number of items per page as needed

@app.route('/', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    learn_query_all = learn.query.paginate(page=page, per_page=PER_PAGE)
    return render_template('index.html', pagination=learn_query_all)


###### ADD learnING SESSION or a TASK 
@app.route('/add/', methods = ['POST'])
def insert_subject():
    if request.method =='POST':
        session = learn(
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
        my_data = learn.query.get(request.form.get('id'))

        my_data.subject = request.form['subject']
        my_data.duration = request.form['duration']
        my_data.date_added = request.form['date_added']
        my_data.comment = request.form['comment']
        
        db.session.commit()
        flash("Գնումը Գրանցված է")
        return redirect(url_for('index'))
    

##### Set Weekly learning Goal from Navbar
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
@app.route('/fitness_index')
def fitness_index():

    fit_query_all = fit.query.order_by(fit.date_added.asc()).all()


    return render_template('fitness_index.html', fit_query_all=fit_query_all )



##### ADD FITNESS EVENT
@app.route('/add_fitness/', methods = ['POST'])
def insert_fitness():
    if request.method =='POST':
        session = fit(
            exercise =    request.form.get('exercise'),
            exercise_count =   request.form.get('exercise_count'),
            comment =    request.form.get('comment'),
            date_added = request.form.get('date_added')
            

        )
        db.session.add(session)
        db.session.commit()
        flash("Ձեր գոնումը հայտնվեց շտեմարանում, Շնորհակալութոյւն")
        return redirect(url_for('fitness_index'))


##### UPDATE FIT
@app.route('/update_fitness/', methods = ['POST'])
def update_fitness():
    if request.method == "POST":
        my_data = fit.query.get( request.form['id'] ) ## Compare this to the index

        my_data.exercise = request.form['exercise']
        my_data.exercise_count = request.form['exercise_count']
        my_data.comment = request.form['comment']
        my_data.date_added = request.form['date_added']
        
        
        db.session.commit()
        flash("Գնումը Գրանցված է")
        return redirect(url_for('fitness_index'))
        # return redirect(url_for('index'))
    

##### Visualize Daily Exercise Stats WOrking version in temp
import io
import base64
import matplotlib.pyplot as plt

def get_base64_encoded_plot(fig):
    from sqlalchemy import func, text, extract
    from sqlalchemy.sql import label
    from flask_sqlalchemy import SQLAlchemy
    from datetime import datetime, timedelta
    import matplotlib.pyplot as plt
    import numpy as np

    from flask import Flask, render_template
    import matplotlib.pyplot as plt
    import io
    import base64



    # Current date and start of the week
    current_date = datetime.now()
    start_of_week = current_date - timedelta(days=current_date.weekday())

    # Query
    query = db.session.query(
        label('day_of_week', extract('isodow', fit.date_added)),
        fit.exercise,
        label('total_exercise_count', func.sum(fit.exercise_count))
    ).filter(
        fit.date_added >= start_of_week,
        fit.date_added <= current_date + timedelta(days=1)
    ).group_by(
        'day_of_week',
        fit.exercise
    ).order_by(
        'day_of_week',
        text('total_exercise_count DESC')
    )

    # Execute the query
    result = query.all()

    # Print the results and prepare data for visualization
    data = {}
    for row in result:
        print(f"Day of Week: {row[0]}, Exercise: {row[1]}, Total Exercise Count: {row[2]}")
        if row[1] not in data:
            data[row[1]] = [0]*7
        data[row[1]][int(row[0])-1] = row[2]

    # Visualization
    # Visualization
    fig, ax = plt.subplots(2, 1, figsize=(10, 10))

    # Line plot
    for exercise, counts in data.items():
        ax[0].plot(range(1, 8), counts, label=exercise)
    ax[0].set_xlabel('Day of Week')
    ax[0].set_ylabel('Total Exercise Count')
    ax[0].set_title('Exercise Count by Day of Week (Line Plot)')
    ax[0].set_xticks(range(1, 8))
    ax[0].set_xticklabels(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    ax[0].legend()

    # Bar plot
    bar_width = 0.35
    index = np.arange(1, 8)
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for i, (exercise, counts) in enumerate(data.items()):
        ax[1].bar(index + i*bar_width, counts, bar_width, label=exercise)
    ax[1].set_xlabel('Day of Week')
    ax[1].set_ylabel('Total Exercise Count')
    ax[1].set_title('Exercise Count by Day of Week (Bar Plot)')
    # ax[1].set_xticks(index + bar_width / 2)
    ax[1].set_xticks(index + bar_width/500 )
    ax[1].set_xticklabels(days_of_week, rotation=45)
    ax[1].legend()

    plt.tight_layout()
    #plt.show()



    # Convert Matplotlib figure to bytes
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    encoded_image = base64.b64encode(image_stream.read()).decode('utf-8')

    # Return the base64-encoded image directly
    return encoded_image





###### ALTERNATIVE VIEW 
@app.route('/daily_fit_stats_viz')
def daily_fit_stats_viz():
 # Matplotlib code executed in the main thread
    

    # Return the plot as HTML
    return render_template('daily_fit_stats_viz.html', encoded_image=encoded_image)









############################################## Views for Nutrition  App ###################################
## Class NutritionForm(FlaskForm) and WTF is used for the ability to 
## Manually insert datetime If a meal was eaten at earlier time than Database NOW()


class NutritionForm(FlaskForm):
    meal = StringField('Meal', validators=[DataRequired()])
    comment = StringField('Comment')
    date_added = DateTimeLocalField('Date Added', format='%Y-%m-%dT%H:%M:%S', default=datetime.now, render_kw={"placeholder": "Optional"})
    weight = StringField('Drink Count', validators=[DataRequired()])
    submit = SubmitField('Add Nutrition')

@app.route('/nutrition_index')
def nutrition_index():
    nutrition_query_all = eat.query.order_by(eat.date_added.asc()).all()
    return render_template('nutrition_index.html', nutrition_query_all=nutrition_query_all )

@app.route('/add_nutrition/', methods=['POST'])
def insert_nutrition():
    exists = db.session.query(
        db.session.query(eat).filter(cast(eat.date_added, Date) >= datetime.now().date()).exists()
    ).scalar()

    if request.method == 'POST':
        meal = request.form.get('meal')
        comment = request.form.get('comment')
        date_added = request.form.get('date_added') or func.now()

        # Check if weight is provided; if not, set it to None
        weight = request.form.get('weight')
        weight = float(weight) if weight else None

        session = eat(
            meal=meal,
            comment=comment,
            date_added=date_added,
            weight=weight
        )
        db.session.add(session)
        db.session.commit()

        if not exists:
            query_fasted_time()  # Calculate time delta if no records for today

    return redirect(url_for('nutrition_index'))


    

##### UPDATE NUTRITION !!!!!!!!!! ATTENTION ERROR HANDLING !!!!!!
            
@app.route('/update_nutrition/', methods=['POST'])
def update_nutrition():
    if request.method == "POST":
        my_data = eat.query.get(request.form['id'])

        my_data.meal = request.form['meal']
        my_data.comment = request.form['comment']

        # Check if date_added field is provided in the form
        date_added = request.form['date_added']
        if date_added:
            my_data.date_added = date_added

        my_data.weight = request.form['weight']

        db.session.commit()
        flash("Nutrition Data Updated")
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
            weight =    request.form.get('weight') if request.form.get('weight') else None,
            weist =     request.form.get('weist') if request.form.get('weist') else None,
            bicep =     request.form.get('bicep') if request.form.get('bicep') else None,
            glucose =   request.form.get('glucose') if request.form.get('glucose') else None,
            
            # or is used to insert now() if the field is empty
            date_added=request.form.get('date_added') or func.now(), 
            comment =   request.form.get('comment') if request.form.get('comment') else None
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
    

#### Delete Body Element  
@app.route('/delete_body/<int:id>', methods=['POST'])
def delete_body(id):
    body_to_delete = body.query.get_or_404(id)
    if request.method == 'POST':
        if request.form.get('confirm') == 'Yes':
            db.session.delete(body_to_delete)
            db.session.commit()
            flash('Row deleted successfully', 'success')
        else:
            flash('Deletion cancelled', 'warning')
        return redirect(url_for('body_index'))
    return render_template('delete_body.html', body_to_delete=body_to_delete)



    
    


    

    

    




    


                           
