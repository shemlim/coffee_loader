
from flask_login import LoginManager,login_user, logout_user, login_required,current_user
from flask import Flask, redirect,request,render_template,url_for,session,flash

from create_db import connection,insert_order,select_cat_menu,select_order_list,\
                        check_order_transac_list,update_order_list,update_order_rndstr,select_order_status_list
from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import  Length
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin
from sqlalchemy import create_engine, null
from datetime import timedelta,datetime
from functools import wraps
import random,string
from datetime import date, timedelta
import pandas as pd
import json
from threading import Lock
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit


app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=180)
Bootstrap(app)
async_mode = None
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


## Set connection up ##

class Connection:
    local = 'server'
    
    # local = 'a'
    if local=='server':
        connection_path = "postgresql://vjrkfvpclacsbk:dbb1ed99cc03d72c142336ee06a97fb7d8776314b647b2c728bc3c0fd8b4e624@ec2-34-194-73-236.compute-1.amazonaws.com:5432/dcluovhf5udvoh"
        url ='https://tjcpjcoffee.herokuapp.com/get_json'
    else:
        connection_path = "postgresql://postgres:Shemlim12#@localhost:5432/usersantuy"
        url ='http://127.0.0.1:8080/get_json'

    engine = create_engine(connection_path)
    conn = engine.connect()
    secret_key = 'ezeepasardashboard_2021'

    def set_app_config(self,app):
        return app.config.update(
            SECRET_KEY=self.secret_key,
            SQLALCHEMY_DATABASE_URI=self.connection_path,
            SQLALCHEMY_TRACK_MODIFICATIONS=False
        )
    
    def state_login_manager(self,app):
        login_manager = LoginManager()
        login_manager.login_view = 'login_barista'
        login_manager.login_message = "You need to login first before you go there."
        login_manager.login_message_category = "warning"
        login_manager.init_app(app)
        return login_manager

Connection().set_app_config(app)
login_manager = Connection().state_login_manager(app)
db = SQLAlchemy()
db.init_app(app)
## Set connection up ##

## Decorator ##
def access_template_required(title=[],url='main.index',list_div_id= None):
    def decorator(func):
        @wraps(func)
        def authorize(*args, **kwargs):
            
            if session['barista_job'] not in title:
                flash("Your account doesn't have access to that page.")
                
                if (session['barista_job'] == 'Barista') or (session['barista_job'] == 'Senior Barista'):
                    
                    return redirect(url_for('barista_get_order'))
                elif (session['barista_job'] == 'Waiter'):
                    return redirect(url_for('waiter_order'))
                elif (session['barista_job'] == 'Admin'):
                    return redirect(url_for('admin_order'))
                else:
                    return redirect(url_for("login_barista"))
                        
            return func(*args, **kwargs)
        return authorize
    return decorator
## Decorator ##


@app.route('/')
def success():
    
    return "Please wait for your coffee. Love from TJC PJ."

@app.route('/getcoffee/<name>',methods=['GET'])
@app.route('/getcoffee',methods=['POST'])
def coffee_getter(name=None):
    

    all_menu = select_cat_menu()
    d_cat_menu = dict()
    
    try:
        name = int(name) if name != None else int(request.form['table'])
    except:
        return redirect(url_for("success"))
    if name <= 0:
        return redirect(url_for("success"))

    for x in all_menu:
        file_image = str(x[1]).lower().split(" ")
        file_image = " ".join(file_image) if len(file_image) <3 else " ".join([y[0] for y in file_image])
        price = "{:.2f}".format(x[7])
        image = url_for('static', filename='upload_photo/{}.jpg'.format(file_image))
        d_cat_menu[x[1]] =  dict({'name':x[1],'status':x[2],"image":image,'is_active':x[6],
                                'price':price,'desc':x[4]})
        
    
    if (request.method == 'POST'):
        
        return render_template("index.html",menu_dict=d_cat_menu,list=list,table_order=name,priority=1,
                                name=session['waiter_name'])


    return render_template("index.html",menu_dict=d_cat_menu,list=list,table_order=name,priority=2)


@app.route("/list_order",methods=['POST'])
def recieve_coffee_order():
    if request.method=='POST':
        all_order = request.form['all_input']
        
        table_order = request.form['table_order']
        priority = int(request.form['priority'])
        all_order,order_total = all_order.rsplit(",",1)
        order_total = int(order_total)
        # 1 -> pending, 2-> ongoing, 3-> finished
        order_status = 1

        
        
        try:
            insert_order(all_order,table_order,order_total,order_status,priority)
        except Exception as e:
            print(e)
        
        if priority == 1:
            return redirect(url_for('waiter_order'))
    return redirect(url_for('success'))
## Login for barista ##

class User(UserMixin,db.Model):
    __tablename__ = 'order_barista'
    barista_id = db.Column('barista_id',db.Integer,primary_key = True, nullable=False)
    barista_name = db.Column('barista_name',db.String(100),nullable=False)
    barista_password = db.Column('barista_password',db.String(50),nullable=False)
    barista_job = db.Column('barista_job',db.Integer,nullable=False)
    barista_hold_table = db.Column('barista_hold_table',db.Integer,nullable=True)
    barista_status = db.Column('barista_status',db.Integer,nullable=True)
    barista_order_id = db.Column('barista_order_id',db.Integer,nullable=True)
    barista_date_edit = db.Column('barista_date_edit',db.Date,nullable=True)
     # Fungsi class utk ini
    def get_id(self):
        return (self.barista_id)

    def is_active(self):
        return self.barista_status


@login_manager.user_loader
def load_user(user_id):
    # Return id
    id =  User.query.filter_by(barista_id = user_id).first()
    return id

## Login for barista ##

class LoginForm(FlaskForm):
    password = PasswordField("Password",validators=[Length(7)])

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_barista'))

@app.route('/login_barista',methods = ['GET'])
@app.route('/login_barista', methods=['POST'])
def login_barista():
    if current_user.is_authenticated:

        return redirect(url_for('barista_get_order'))

    form = LoginForm()
    
    if form.validate_on_submit():
        
        user = User.query.filter_by(barista_password=form.password.data).first()
        
        
        if user == None:
            flash('Please check your login details and try again.')
            return redirect(url_for('login_barista'))
        if (user.barista_job == 'Barista') or (user.barista_job == 'Senior Barista') :
            # return str(user)
            try:
                # Reset user barista
                user.barista_hold_table = None
                user.barista_order_id = None
                user.barista_status = None
                db.session.commit()

                # Taruh session
                login_user(user)
                session['barista_id'] = user.barista_id
                session['barista_name'] = user.barista_name
                session['barista_job'] = user.barista_job
                session['barista_hold_table'] = user.barista_hold_table
                session['barista_status'] = user.barista_status
                session['barista_order_id'] = user.barista_order_id
                
            except Exception as e:
                print(e)
            
            return redirect(url_for('barista_get_order'))
        elif user.barista_job == 'Waiter':
            login_user(user)
            ## Lanjutkan ##
            session['waiter_id'] = user.barista_id
            session['waiter_name'] = user.barista_name
            session['barista_job'] = user.barista_job
            
            return redirect(url_for('waiter_order'))
        elif user.barista_job == 'Admin':
            login_user(user)
            session['admin_id'] = user.barista_id
            session['admin_name'] = user.barista_name
            session['barista_job'] = user.barista_job
            
            return redirect(url_for('admin_order'))

    return render_template('login.html',form=form)
## Login for barista ##

def load_order_img(order_tr):
    order_img = dict()
    for x in order_tr[2].split(","):
        temp = x.split("x")[1]
        temp = temp.split(" ")
        if len(temp) > 2:
            order_img[x] = " ".join([y[0] for y in temp]).lower()
        else:
            order_img[x] = " ".join(temp).lower()
            
    return order_img

@app.route("/check_barista_order")
@login_required
@access_template_required(['Barista','Senior Barista'])
def check_order():
    len_order = check_order_transac_list()[0][0]
    return str(len_order)
    
# Function for barista #
@app.route('/barista_order',methods = ['GET'])
@login_required
@access_template_required(['Barista','Senior Barista'])
def barista_get_order():
    user = User.query.filter_by(barista_id = session['barista_id']).first()
    if (user.barista_job == 'Senior Barista'):
        return redirect(url_for('senior_barista'))

    
    if (session['barista_order_id'] != None) & (user.barista_order_id != None):
        
        order_tr = select_order_list(int(session['barista_order_id']))[0]
        if order_tr[6] == 2:
            order_id = order_tr[0]
            order_table = order_tr[1]
            order_total = order_tr[4]
            order_img = load_order_img(order_tr)
            session['after_login'] = 1
            return render_template('barista_index.html',name = session['barista_name'],order_total=order_total
            ,order_tr=order_tr,order_img=order_img)
    
    len_order = check_order_transac_list()[0][0]
    
    if len_order >= 1:
        
        # Order Transaction
        order_tr = select_order_list()[0]
        order_id = order_tr[0]
        order_table = order_tr[1]
        order_total = order_tr[4]

        random_string = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(30))
        update_order_rndstr(random_string,order_id)
        
        # Update order transaction
        try:
            update_order_list(session['barista_name'],order_id,random_string)
            order_tr = select_order_list(order_id=order_id,rand_str=random_string)[0]
            order_id = order_tr[0]
            order_table = order_tr[1]
            order_total = order_tr[4]
            order_img = load_order_img(order_tr)

            # Update order barista
            user.barista_order_id = order_id
            user.barista_hold_table = order_table
            user.barista_status = 1 # Ongoing order
            user.barista_date_edit = datetime.now()
            session['barista_order_id'] = order_id
            db.session.commit()
        except Exception as e:
            flash("Your order has been taken by the others.")
            return render_template('barista_index.html',name = session['barista_name'],order_total=0)
            # print(e)
        return render_template('barista_index.html',name = session['barista_name'],order_total=order_total
        ,order_tr=order_tr,order_img=order_img)
        
    else:
        user.barista_hold_table = None
        user.barista_status = None
        user.barista_date_edit = None
        user.barista_order_id = None

        session['barista_hold_table'] = user.barista_hold_table
        # session['barista_status'] = user.barista_status
        session['barista_order_id'] = user.barista_status
        db.session.commit()
        return render_template('barista_index.html',name = session['barista_name'],order_total=0)


# @app.route('/senior_barista',methods=['GET'])
# @app.route('/senior_barista',methods=['POST'])
# @login_required
# @access_template_required(['Senior Barista'])
# def senior_barista():
    
#     search = request.args.get('search') 
#     if search == None:search=''
#     search = '' if (len(search) == 0) else search
#     session['search'] = search
    
    
#     # print(order_tr)
#     user = User.query.filter_by(barista_id = session['barista_id']).first()
#     if (session['barista_order_id'] != None) & (user.barista_order_id != None):
#         order_tr = select_order_list(int(session['barista_order_id']))[0]
        
#         if order_tr[6] == 2:
#             order_id = order_tr[0]
#             order_table = order_tr[1]
#             order_total = order_tr[4]
#             order_img = load_order_img(order_tr)
#             session['after_login'] = 1
#             return render_template('barista_index.html',name = session['barista_name'],order_total=order_total
#             ,order_tr=order_tr,order_img=order_img)

#     # Later change the head
#     order_tr = select_order_list(head=100) if search == '' else select_order_list(head=100,table_id=search)
    
#     if (request.method == 'POST'):
#         order_id = int(request.form['order_id'])

#         order_tr = select_order_list(order_id=order_id)[0]
#         order_id = order_tr[0]
#         order_table = order_tr[1]
#         order_total = order_tr[4]
        
#         random_string = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(30))
#         update_order_rndstr(random_string,order_id)
        
#         try:
#             # print(random_string)
#             update_order_list(session['barista_name'],order_id,random_string)
#             order_tr = select_order_list(order_id=order_id,rand_str=random_string)[0]
#             order_id = order_tr[0]
#             order_table = order_tr[1]
#             order_total = order_tr[4]
#             order_img = load_order_img(order_tr)
            
#             # Update order barista
#             user.barista_order_id = order_id
#             user.barista_hold_table = order_table
#             user.barista_status = 1 # Ongoing order
#             user.barista_date_edit = datetime.now()
#             session['barista_order_id'] = order_id
            
#             db.session.commit()

#         except Exception as e:
#             print(e)
#             flash("Your order has been taken by the others.")
#             # return redirect(url_for("senior_barista"))
#             return str(e)
        
#         return render_template('barista_index.html',name = session['barista_name'],order_total=order_total
#         ,order_tr=list(order_tr),order_img=order_img)
#         # return order_id
#     session['order_table'] = [x[0] for x in order_tr]
#     return render_template('barista_index_senior.html',name = session['barista_name'],
#                 order_tr=order_tr,zip=zip,search=search)


@app.route("/barista_finish",methods=['POST'])
@access_template_required(['Barista','Senior Barista'])
def barista_finish_order():

    is_del = request.form['order_delete']
    order_id = request.form['order_id']
    # The order will be deleted.
    if is_del == 'delete':
        update_order_list(session['barista_name'],order_id,order_status=5)
        return redirect(url_for('barista_get_order'))

    # The order will be finished and up to delivery.
    user = User.query.filter_by(barista_id = session['barista_id']).first()

    update_order_list(session['barista_name'],order_id,order_status=3)
    
    user.barista_order_id = None
    session['barista_order_id'] = None
    
    db.session.commit()
    return redirect(url_for('barista_get_order'))
# Function for barista #
    


# Function for waiter #
@app.route("/waiter_order",methods=['GET'])
@login_required
@access_template_required(['Waiter'])
def waiter_order():
    
    return render_template('cth.html')

# @app.route('/waiter_coffee_list',methods=['GET'])
# @login_required
# @access_template_required(["Waiter"])
# def waiter_coffee_list():
#     # Later change the head
#     order_tr = select_order_status_list()
    
#     return render_template('coffee_order_list.html',name = session['waiter_name'],
#                 order_tr=order_tr,zip=zip)
# Function for waiter #

# Function for admin #
def allsundays(year,month= []):
    d = date(year, min(month), 1)
    d += timedelta(days = 6 - d.weekday())
    while (d.year == year) & (d.month in month):
        yield d
        d += timedelta(days = 7)


def to_pd(mobile_records,df='order'):
    menu_df = pd.DataFrame(mobile_records)
    if df == 'order':
        menu_df.columns = ['order_id','order_table','order_details','order_priority','order_totals','order_barista','order_status','order_date','order_rand_str']
    else:
        menu_df.columns = ['menu_id','menu_name','menu_status','menu_date','order_description','order_menu_category','menu_available','menu_price']
    return menu_df

def summary_report_func(df,menu_df):
    total_buy = dict()
        
    for x in df['order_details']:
        for y in x.split(","):
            total,coffee = y.split("x")
            if coffee in total_buy.keys():
                total_buy[coffee] += int(total)
            else:
                total_buy[coffee] = int(total)
    
    summary = pd.DataFrame([x for x in total_buy.keys()]).rename(columns={0:'menu_name'})
    summary['menu_count'] = summary['menu_name'].apply(lambda x: total_buy[x])
    summary = pd.merge(summary,menu_df[['menu_name','menu_price']],how='left',left_on='menu_name',right_on='menu_name')
    summary['menu_total'] = summary['menu_count'].astype(int) * summary['menu_price'].astype(float)
    summary

    summary_report = dict()

    summary_report['Total cup'] = summary['menu_count'].astype(int).sum()
    summary_report['Total cost / cup'] = summary['menu_total'].astype(int).sum()
    summary_report['Most ordered coffee'] = ','.join(list(summary[summary['menu_count'] == \
                                                                max(summary['menu_count'])]['menu_name'].values))

    summary_report['Least ordered coffee'] = ','.join(list(summary[summary['menu_count'] == \
                                                                min(summary['menu_count'])]['menu_name'].values))

    return [summary,summary_report]

@app.route("/admin_record/<name>",methods=['GET'])
@login_required
@access_template_required(['Admin'])
def admin_order(name):
    if name == 'monthly':
        now = datetime.now().today()
        min = datetime.strftime(now,"%Y-%m-01")
        max = datetime.strftime(now,"%Y-%m-%d")
        order_tr = select_order_list(min_date=min,max_date=max)
        menu_df = select_cat_menu()
        # print(order_tr,menu_df)
    
        
        df = to_pd(order_tr)
        menu_df = to_pd(menu_df,'a')
        summary,summary_report = summary_report_func(df,menu_df)
        summary.columns = [x.replace("menu_","") for x in summary.columns]

    return render_template('admin_record.html',min=min,max=max,order_tr=order_tr,
                            summary=summary,summary_report=summary_report)
# Function for admin #

# Function Live load #

@app.route('/senior_barista',methods=['GET'])
@login_required
@access_template_required(['Senior Barista'])
def senior_barista():
    
    return render_template("senior_barista_index.html", async_mode=socketio.async_mode)


def background_thread():
    """Example of how to send server generated events to clients."""
    
    while True:
        socketio.sleep(15)
        
        order_tr = select_order_list(head=100,all_status=1)
 
        
        if len(order_tr)> 0:
            
            socketio.emit('my_response',
                    {'data': json.dumps(order_tr, default=str)})


@socketio.event
@login_required
@access_template_required(['Senior Barista'])
def my_event(message):
    order_tr = select_order_list(head=100,all_status=1)
    session['loaded_table'] = [x[0] for x in order_tr]
    emit('my_response',{'data': json.dumps(order_tr, default=str)})


@socketio.on('status_order')
@login_required
@access_template_required(['Senior Barista'])
def handle_message(data):
    
    print("Received message",data['data'],data['action'])
    status_update = 'success'
    order_status = 0
    if data['action'] == 'take':
        order_status = 2
    elif data['action'] == 'delete':
        order_status = 5
    else:
        order_status = 3

    try:
        update_order_list(session['barista_name'],data['data'],order_status=order_status)
    except Exception as e:
        status_update = 'failed'
        print(e)
    
    emit('status_response', {'data': status_update,'id':data['data'],'action':data['action']})


@socketio.event
@login_required
@access_template_required(['Senior Barista'])
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    # emit('my_response', {'data': 'Connected', 'count': 0})


if __name__ == '__main__':
    socketio.run(app,cors_allowed_origins="*")