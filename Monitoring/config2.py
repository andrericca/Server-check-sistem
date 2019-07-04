from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlite3 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/...'
db = SQLAlchemy(app)
#Script to create DB to receive information of day and hour and hostname from alert.
conn = sqlite3.connect('momento.db')
print ("Opened database successfully")

conn.execute('CREATE TABLE momento (id INTEGER PRIMARY KEY AUTOINCREMENT, dma DATETIME, hostname TEXT)')
print ("Table created successfully")
conn.close()

class alerts(db.Model):
    id = db.Column ( 'id', db.Integer,primary_key=True)
    dma = db.Column('dma', db.DateTime, unique=True, nullable=False)
    hostname = db.Column('hostname', db.String(80), unique=True, nullable=False)
    def __repr__(self):
        return f"momento('{self.id}','{self.dma}','{self.hostname}')"
