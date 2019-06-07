
import os, sys, subprocess, requests, json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlite3 as sql
from datetime import datetime, date, timedelta, time
#Function to check ping and insert alerts into DB.
def main():
    hosts = ["192.168.100.180", "192.168.100.29"]
    today = datetime.today().replace(second=0, microsecond=0)

    for hostname in hosts:
        x = "ping -c1 " + hostname
        cmd = os.system(x)
#Alert = 0 means server is up and =1 means it`s down.
        if cmd != 0:
                con=sql.connect("alerts.db") 
                cur = con.cursor()
                cur.execute("INSERT INTO alerts (alert,host,time) VALUES (?,?,?)",(1,hostname,today))
                ping = cur.execute("SELECT * from alerts WHERE host= ? ORDER BY id DESC LIMIT 10",(hostname,))
                con.commit()
                print("Record successfully added")
        else:
            with sql.connect("alerts.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO alerts (alert,host,time) VALUES (?,?,?)",(0,hostname,today))
                con.commit()
                print("Record successfully added")
        print(cmd)

    return hostname

if __name__=='__main__':
    sys.exit(main())