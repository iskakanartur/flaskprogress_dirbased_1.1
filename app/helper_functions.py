from app import app, db
from app.models import *
from sqlalchemy import func,  and_      ### to combine db queries in past Mo to su function 
from calendar import monthrange  ### to combine db queries in past Mo to su function 
from datetime import date, datetime, timedelta






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


 