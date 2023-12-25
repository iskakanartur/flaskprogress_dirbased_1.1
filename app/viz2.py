

import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import func
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from datetime import datetime, timedelta


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'  # Use your own URI
db = SQLAlchemy(app)

class fit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise = db.Column(db.String(150), nullable=False)
    count = db.Column(db.Integer)
    date_added = db.Column(db.DateTime(timezone=True), server_default=func.now())
    comment = db.Column(db.String(150), nullable=True)

# Get the date a week ago
week_ago = datetime.now() - timedelta(days=7)

# Query the database
data = db.session.query(fit.exercise, func.sum(fit.count)).filter(fit.date_added >= week_ago).group_by(fit.exercise).all()

# Convert the data to a DataFrame
df = pd.DataFrame(data, columns=['Exercise', 'Count'])

# Create the plot
df.plot(kind='bar', x='Exercise', y='Count', legend=False)
plt.ylabel('Count')
plt.title('Exercise Count in the Past Week')

# Show the plot
plt.show()







