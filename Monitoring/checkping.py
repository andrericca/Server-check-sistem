
import os, sys, subprocess, requests, json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlite3 as sql
from datetime import datetime, date, timedelta, time

#Send message function.
def msg2slack(msg):
#Url from slack to indicate the channel.
    url = slack url
    payload = {
               "text": msg,
               "icon_emoji": ":computer:"}
    r = requests.post(url, json=payload)
    result = r.text
    print(result)


#Function to check ping and insert alerts into DB.
def main():
    hosts = [ip]
    today = datetime.today().replace(second=0, microsecond=0)

    for hostname in hosts:
        x = "ping -c1 " + hostname
        cmd = os.system(x)
#Alert = 0 means server is up and = 1 means it`s down.
        if cmd != 0:
                con=sql.connect("alerts.db") 
                cur = con.cursor()
                cur.execute("INSERT INTO alerts (alert,host,time) VALUES (?,?,?)",(1,hostname,today))
                con.commit()
                print("Record successfully added")
        else:
            with sql.connect("alerts.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO alerts (alert,host,time) VALUES (?,?,?)",(0,hostname,today))
                con.commit()
                print("Record successfully added")
        print(cmd)
    message()
    return hostname



#Function to analyze DB with alerts and check if send or not send a alert message.
def message():
    hosts = [ip]
    today = datetime.today().replace(second=0, microsecond=0)
    con = sql.connect("alerts.db")
    conn=sql.connect("momento.db")
    curr=conn.cursor()
    cur = con.cursor()
    for hostname in hosts:
        ping = cur.execute("SELECT * from alerts WHERE host= ? ORDER BY id DESC LIMIT 10",(hostname,))
        data = curr.execute("SELECT * from momento WHERE hostname= ? ORDER by id DESC LIMIT 1",(hostname,))
        count=[]  
        for rows in ping:          
            h=str (rows[1])
            count.append(h)
        ocorrencia = count.count("1")
        x=timedelta(minutes=0)
        for rows in data:
            dia=datetime.strptime(rows[1], '%Y-%m-%d %H:%M:%S')
            x = (today - dia)
        print(x)
        print(ocorrencia)
        print(count)
        z=count[0]
        if ocorrencia >= 10 and (x > timedelta(minutes=10) or x==timedelta(minutes=0)):
            print("o "+str (x)+" entrou")
            msg2slack(msg="%s cannot be reached" % hostname)
            curr.execute("INSERT INTO momento (dma,hostname) VALUES (?,?)",(today,hostname))
        if ocorrencia == 1 and (z=="1"):
            msg2slack(msg="%s cannot be reached" % hostname)
        conn.commit()




if __name__=='__main__':
    sys.exit(main())
