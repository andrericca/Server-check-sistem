from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlite3 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/andreyoshdia/Desktop/Monitoring/alerts.db'
db = SQLAlchemy(app)
#Script to create DB to receive alerts and time.
conn = sqlite3.connect('alerts.db')
print ("Opened database successfully")

conn.execute('CREATE TABLE alerts (id INTEGER PRIMARY KEY AUTOINCREMENT,alert TEXT, host TEXT, time DATETIME)')
print ("Table created successfully")
conn.close()

class alerts(db.Model):
    id = db.Column ( 'id', db.Integer,primary_key=True)
    alert = db.Column('alert', db.String(80), unique=True, nullable=False)
    host = db.Column('host', db.String(80), unique=True, nullable=False)
    time = db.Column('time', db.DateTime, unique=True, nullable=False)

    def __repr__(self):
        return f"data('{self.id}','{self.host}','{self.time}')"