from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import *



app = Flask(__name__)

## See .env that's where you change it to prod dev or test
## Change Depneding on Prod Test or Dev
# app.config.from_object(DevelopmentConfig)



if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object(ProductionConfig)

elif os.getenv('FLASK_ENV') == 'testing':
    app.config.from_object(TestingConfig)
else:
    # Default config
    app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)


#### Put This above and you have Circular Import Error
from app import views, models


with app.app_context():
    db.create_all()