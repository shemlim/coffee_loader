# import logging
# path_err = "/home/wsladmin/Flask_EzeePasar/"
# logging.basicConfig(level=logging.ERROR,filename=path_err+"error.log",filemode='w')


from flask import Flask
# from model.turicreate_file import model_predict,model_predict_popularity,connected,recommend
# from model.credit_scoring import load_all,getEzeepasar_API
import pymssql
import numpy as np
import time
# from sklearn.model_selection import train_test_split

import sys
import logging

import pandas as pd
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qkxxgaorsxskie:6993da4ba44e99a4a6fa5f2542e31c630a0f1b1b065b86b8a53ef3991419059e@ec2-54-80-123-146.compute-1.amazonaws.com:5432/das9bp7714f6mq'


logging.basicConfig(stream=sys.stderr)
# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/success/<name>')
def success(name):
    return "Welcome, {}".format(name)
    
if __name__ == '__main__':
    app.run(debug= True)