from app import app, db
from app.models import *
from sqlalchemy import func,  and_      ### to combine db queries in past Mo to su function 
from calendar import monthrange  ### to combine db queries in past Mo to su function 
from datetime import date, datetime, timedelta








## get last updated weekly learning goal 
## relates to the POSTGRES table various
## and the view/query past su_mo, multi plot




##  SUM OF sunday to monday  Learning Hours
## query sunday to monday 
def mo_su_query():
    # <= in the first clause (func.date_tunc) makes it monday to monday
    mo_su = db.session.query(Learn).filter (and_
                (Learn.date_added <= func.date_trunc('week', func.now( ) ), 
                 Learn.date_added >= func.date_trunc('week', func.now( ) ) - timedelta(days=7))).order_by(Learn.date_added )
    return (mo_su)


 