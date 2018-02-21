import pandas as pd

from app import app
from app import db
from app.models import User

df = pd.read_csv('oscars_data_set.csv')
for i, row in df.iterrows():
    u = User(username=row['username'],
             email=row['email'],
             first_name=row['first_name'],
             last_name=row['last_name'],
             pickup_address=row['pickup_address'],
             pickup_city=row['pickup_city'],
             pickup_state=row['pickup_state'])
    db.session.add(u)

db.session.commit()
