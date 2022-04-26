# import logging
# path_err = "/home/wsladmin/Flask_EzeePasar/"
# logging.basicConfig(level=logging.ERROR,filename=path_err+"error.log",filemode='w')


from flask import Flask,request,render_template,url_for
# from model.turicreate_file import model_predict,model_predict_popularity,connected,recommend
# from model.credit_scoring import load_all,getEzeepasar_API
import numpy as np
import time
# from sklearn.model_selection import train_test_split
import psycopg2
import sys,os
import logging

import pandas as pd
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:Shemlim12#@localhost:5432/usersantuy'
# postgres://modwefcfitstlx:bb286cf8d0d6adfc726eff2ee3ab8339fd8421420bd3052bc2c784303a562112@ec2-54-80-123-146.compute-1.amazonaws.com:5432/d54sfhkmvrsn1h
# postgres://mqhureykqyyrfb:4203d70494bbdc600a37641ffc08bbfba4e48ce6549b1285c042e1c56c76030f@ec2-52-86-56-90.compute-1.amazonaws.com:5432/demc2tb1r0urm0


def connection():
    conn = psycopg2.connect(
        host="ec2-52-86-56-90.compute-1.amazonaws.com",
        database="demc2tb1r0urm0",
        user='mqhureykqyyrfb',
        password='4203d70494bbdc600a37641ffc08bbfba4e48ce6549b1285c042e1c56c76030f')
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
    # create_db()
    # insert_db()
    # all_data = select_db()


    # return str(all_data)
    return "nice"

@app.route('/getcoffee/<name>',methods=['GET'])
def coffee_getter(name):
    
    img_url = url_for('static', filename='upload_photo/coffee2.jpg')
    img_url2 = url_for('static', filename='upload_photo/coffee1.jpg')
    img_url3 = url_for('static', filename='upload_photo/coffee3.jpg')

    return render_template("ordercoffee.html",name=name,img_url = img_url,img_url2 = img_url2,img_url3 = img_url3)
    
if __name__ == '__main__':
    app.run()