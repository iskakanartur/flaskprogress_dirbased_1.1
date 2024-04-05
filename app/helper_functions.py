from app import app, db
from app.models import *
import sqlalchemy

from sqlalchemy import func, text
from datetime import timedelta, date, datetime

from sqlalchemy import and_      ### to combine db queries in past Mo to su function 
from calendar import monthrange  ### to combine db queries in past Mo to su function 


from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import matplotlib.pyplot as plt
import io
import base64

from sqlalchemy import func, desc
from sqlalchemy.sql import text

from sqlalchemy import case

    




from dateutil.relativedelta import relativedelta, MO ## for helper function to query fit



######################### Query Past Monday to Sunday Results  #########################
def mo_su_query():
    # <= in the first clause (func.date_tunc) makes it monday to monday
    mo_su = db.session.query(Learn).filter (and_
                (Learn.date_added <= func.date_trunc('week', func.now( ) ), 
                 Learn.date_added >= func.date_trunc('week', func.now( ) ) - timedelta(days=7))).order_by(Learn.date_added )
    return (mo_su)



## get last updated weekly learning goal 
def get_last_weekly_goal():
    last_record = various.query.order_by(various.datetime.desc()).first()
    # Accessing the columns of the last record
    if last_record:
        last_record_goal = last_record.week_goal
        # Access other columns as needed
    else:
        last_record_goal = None

    return (last_record_goal)



######################## Get All SUbject Names
def get_subjects ():
    # subject_names = [subj.subject for subj in Learn.query.all()]
    subject_names = [subj for subj in db.session.query(Learn.subject).distinct()]
    subject_names = [i[0] for i in subject_names]
    return (subject_names)





###################### OPTIMIZE LATER DISTINCT SUBJECTS & TOTAL HOURS LEARNED EACH sunday to monday 
def subj_total ():
    from sqlalchemy import and_ ### to combine db queries below
    distinct_subjects = get_subjects()
    res = []
    subj_total_sum_mo_su = []
    for subject in distinct_subjects:
        qry_res = db.session.query(Learn).filter (and_( 
        Learn.date_added < func.date_trunc('week', func.now( ) ), 
        Learn.date_added >= func.date_trunc('week', func.now( ) ) - timedelta(days=7),
        Learn.subject== subject)).with_entities(func.sum(Learn.duration)).scalar()

        res.append(qry_res)
        subj_total_sum_mo_su.append((subject, qry_res))

    
    return (subj_total_sum_mo_su)




################################ Helpers For The Nutrition Module ######################
from datetime import datetime, timedelta

def query_fasted_time():
    total_seconds = 0  # Initialize total_seconds here

    # Check if there are any records in the 'eat' table
    if not eat.query.first():
        print("No records found. Skipping calculation.")
        # Write time delta to the DB if there are no records
        today = datetime.now().date()
        most_recent_eat = eat.query.order_by(eat.date_added.desc()).first()
        if most_recent_eat:
            most_recent_eat.time_delta = timedelta(seconds=total_seconds)
            db.session.commit()
        return

    subquery = db.session.query(
        eat.date_added.cast(db.Date).label('date'),
        func.min(eat.date_added).label('first_record'),
        func.max(eat.date_added).label('last_record')
    ).group_by('date').subquery()

    query = db.session.query(subquery.c.date,
                             (subquery.c.first_record -
                              func.lag(subquery.c.last_record).over(order_by=subquery.c.date)).label('time_delta')
                             )

    # Get time delta in seconds to calculate total fasted time
    for row in query:
        if row.time_delta is not None:
            # Convert the time delta to hours and minutes
            total_seconds += row.time_delta.total_seconds()  # Accumulate total seconds

    # Convert accumulated total_seconds to hours and minutes outside the loop
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    print(f"Total Fasted Time: {int(hours)} hours and {int(minutes)} minutes")

    # Write time delta to the DB, optimize or change later
    today = datetime.now().date()
    most_recent_eat = eat.query.order_by(eat.date_added.desc()).first()
    if most_recent_eat:
        most_recent_eat.time_delta = timedelta(seconds=total_seconds)
        db.session.commit()



################# FOR FIT SUMMARY STATISTICS
def fit_exercise_stats_past_mo_su ():

    # <= in the first clause (func.date_tunc) makes it monday to monday
    mo_su = db.session.query(fit).filter (and_
                (fit.date_added <= func.date_trunc('week', func.now( ) ), 
                 Learn.date_added >= func.date_trunc('week', func.now( ) ) - timedelta(days=7))).order_by(fit.date_added )
    
    # Print the results
    for record in mo_su:
        print(f"ID: {record.id}, Exercise: {record.exercise}, Count: {record.exercise_count}, Date Added: {record.date_added}, Comment: {record.comment}")






def query_fit_mo_now ():

    
    query = db.session.query(fit).filter(and_(fit.date_added >= func.date_trunc('week', func.current_date()),
                                              fit.date_added <= func.now())).order_by(fit.date_added)
    
    
    # Print the results
    for record in query:
        print(f"ID: {record.id}, Exercise: {record.exercise}, Count: {record.exercise_count}, Date Added: {record.date_added}, Comment: {record.comment}")





# from app.helper_functions import fit_mo_now_stats


def fit_mo_now_stats():
    import pandas as pd
    query = db.session.query(
        func.to_char(fit.date_added, 'Day').label('day_of_week'),
        fit.exercise,
        func.sum(fit.exercise_count).label('total_exercise_count')
    ).filter(
        fit.date_added >= text("date_trunc('week', CURRENT_DATE)"),
        fit.date_added <= text("CURRENT_DATE + interval '1 day'")
    ).group_by(
        'day_of_week',
        fit.exercise
    ).order_by(
        'day_of_week',
        desc('total_exercise_count')
    )

    # Execute the query
    result = query.all()

    # Print the results
    #for row in result:
        #print(row)

    # Convert the result to a Pandas DataFrame
    columns = ['day_of_week', 'exercise', 'total_exercise_count']
    df = pd.DataFrame(result, columns=columns)

    # Print or further manipulate the DataFrame
    print(df)
    print ('************************************')

    # Pivot the data
    pivot_df = df.pivot(index='day_of_week', columns='exercise', values='total_exercise_count')

    # Replace NaN values with 0
    pivot_df = pivot_df.fillna(0)
    print (pivot_df)

    # Plot
    pivot_df.plot(kind='bar', stacked=False)

    # Show the plot
    plt.show()


############################################# Week Day Correct Try  DOESNT WORK TRY WITH NUMBERS THEY YOULL CONVERT THEM TO DAYS
    
# from app.helper_functions import fit_mo_now_stats_vis

def fit_mo_now_stats_vis ():

    from sqlalchemy import func, text, extract
    from sqlalchemy.sql import label
    from flask_sqlalchemy import SQLAlchemy
    from datetime import datetime, timedelta
    import matplotlib.pyplot as plt
    import numpy as np



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
    plt.savefig('app/static/images/line_plot_fit.png')

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
    plt.savefig('app/static/images/bar_plot_fit.png')

    plt.tight_layout()
    plt.show()


