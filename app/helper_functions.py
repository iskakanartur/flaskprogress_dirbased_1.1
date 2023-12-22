from app import app, db
from app.models import *
import sqlalchemy

from sqlalchemy import func, text
from datetime import timedelta, date, datetime

from sqlalchemy import and_      ### to combine db queries in past Mo to su function 
from calendar import monthrange  ### to combine db queries in past Mo to su function 






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

def query_fasted_time ():

    subquery = db.session.query(
    eat.date_added.cast(db.Date).label('date'),
    func.min(eat.date_added).label('first_record'),
    func.max(eat.date_added).label('last_record') ).group_by('date').subquery()

    query = db.session.query(subquery.c.date, 
                             (subquery.c.first_record - 
                            func.lag(subquery.c.last_record).over(order_by=subquery.c.date)).label('time_delta')
                           )
    

    # Get time delta in seconds to calculated total fasted time
    for row in query:
        if row.time_delta is not None:
        # Convert the time delta to hours and minutes
            total_seconds = row.time_delta.total_seconds()
            hours, remainder = divmod(total_seconds, 3600)
            minutes, _ = divmod(remainder, 60)

            # print(f"Date: {row.date}, Time Delta: {int(hours)} hours and {int(minutes)} minutes")


    # Write time delta to the DB, optimize or change later 
    today = datetime.now().date()
    # Get the first record of today
    record = db.session.query(eat).filter(func.date(eat.date_added) == today).order_by(eat.date_added).first()
    ## Count number of rows if one row for meal means it is OMAD
    record_count =  db.session.query(eat).filter(func.date(eat.date_added) == today).order_by(eat.date_added).count()
    if record:
        # Update the time_delta field with total_seconds
        record.time_delta = timedelta(seconds=total_seconds)
        # Commit the changes
        db.session.commit()

    # print (record_count)
    


