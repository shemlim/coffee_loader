# import logging
# path_err = "/home/wsladmin/Flask_EzeePasar/"
# logging.basicConfig(level=logging.ERROR,filename=path_err+"error.log",filemode='w')

import gunicorn
from flask import Flask
# from model.turicreate_file import model_predict,model_predict_popularity,connected,recommend
# from model.credit_scoring import load_all,getEzeepasar_API
import numpy as np
import time
# from sklearn.model_selection import train_test_split
import psycopg2
import sys
import logging

import pandas as pd
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:Shemlim12#@localhost:5432/usersantuy'

def connection():
    conn = psycopg2.connect(
        host="localhost",
        database="usersantuy",
        user='postgres',
        password='Shemlim12#')
    cur = conn.cursor()

    return [conn,cur]

def create_db():
    conn,cur = connection()
    try:
        
        cur.execute("select * from information_schema.tables where table_name=%s", ('users',))
        if bool(cur.rowcount) == False:
            print("d",bool(cur.rowcount))
            cur.execute('CREATE TABLE users (order_id serial PRIMARY KEY ,'
                                            'order_name varchar (150) NOT NULL,'
                                            'order_details varchar (50) NOT NULL,'
                                            'order_barista varchar (50) ,'
                                            'order_status int,'
                                            'order_date date DEFAULT CURRENT_TIMESTAMP);'
                                            )
            conn.commit()

            cur.close()
            conn.close()
        else:
            print("d",bool(cur.rowcount))
    except Exception as e:
        print("asd {} ".format(e))
        pass

def insert_db():
    conn,cur = connection()
    sql = "insert into users(order_name,order_details,order_barista,order_status) values('shem','0,0,1',null,0);"
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def select_db(head=5):
    conn,cur = connection()
    sql = "select * from users;"
    cur.execute(sql)

    mobile_records = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return mobile_records

logging.basicConfig(stream=sys.stderr)
# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/')
def success():
    print("nice")
    create_db()
    # insert_db()
    all_data = select_db()


    return str(all_data)
    
if __name__ == '__main__':
    app.run()