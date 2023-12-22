from sqlalchemy import func, text
from datetime import timedelta

from app import app, db
from app.models import *
import sqlalchemy


# Get the date of each record
subquery = db.session.query(
    eat.date_added.cast(db.Date).label('date'),
    func.min(eat.date_added).label('first_record'),
    func.max(eat.date_added).label('last_record')
).group_by('date').subquery()

# Calculate the time delta between the last record of each day and the first record of the next day
query = db.session.query(
    subquery.c.date,
    (subquery.c.first_record - func.lag(subquery.c.last_record).over(order_by=subquery.c.date)).label('time_delta')
)

for row in query:
    if row.time_delta is not None:
        print(f"Date: {row.date}, Time Delta: {row.time_delta.total_seconds()} seconds")



