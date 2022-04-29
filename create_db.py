import psycopg2
from datetime import timedelta,datetime

class db_date:
    def __init__(self):
        self.date_now = datetime.now() + timedelta(hours=8)
        self.date = self.date_now.date()
        self.hour = self.date_now.hour

## For order transaction ##
def insert_order(list_order,table_order,order_total,order_status,priority=1):
    conn,cur = connection()
    sql = """insert into order_transac(order_table,order_details,order_priority,order_total,order_status,order_date) 
            values({},'{}',{},{},{},'{}');
          """.format(table_order,list_order,priority,order_total,order_status,db_date().date_now)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
## For order transaction ##

## For order menu category ##
def select_cat_menu():
    conn,cur = connection()
    sql = "select * from order_menu;"
    cur.execute(sql)

    mobile_records = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return mobile_records
## For order menu category ##


def connection():
    # For server
    # conn = psycopg2.connect(
    #     host="ec2-34-194-73-236.compute-1.amazonaws.com",
    #     database="dcluovhf5udvoh",
    #     user='vjrkfvpclacsbk',
    #     password='dbb1ed99cc03d72c142336ee06a97fb7d8776314b647b2c728bc3c0fd8b4e624')

    # For Local
    conn = psycopg2.connect(
        host="localhost",
        database="usersantuy",
        user='postgres',
        password='Shemlim12#')

    cur = conn.cursor()

    return [conn,cur]


## For order transaction ##
def check_order_transac_list():
    conn,cur = connection()
    
    min = db_date().date_now
    dt_today = db_date().date
    print(dt_today)
    if min.hour <= 17:
        min = datetime.strftime(dt_today,"%Y-%m-%d 06:00:00")
    else:
        min = datetime.strftime(dt_today,"%Y-%m-%d 17:30:00")
    max = datetime.strftime(dt_today,"%Y-%m-%d 23:59:59")
    
    sql = "select count(*) from order_transac where order_date >= '{}' and order_date <= '{}' and order_status = 1;"\
            .format(min,max)
    cur.execute(sql)

    mobile_records = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return mobile_records

def select_order_list(order_id=None,head=1):
    conn,cur = connection()
    sql = ''
    min = db_date().date_now
    dt_today = db_date().date
    if min.hour <= 17:
        min = datetime.strftime(dt_today,"%Y-%m-%d 06:00:00")
    else:
        min = datetime.strftime(dt_today,"%Y-%m-%d 17:30:00")
    max = datetime.strftime(dt_today,"%Y-%m-%d 23:59:59")
    if order_id != None:
        sql = """select * from order_transac where order_id = {}"""\
            .format(order_id)
    else:
        sql = """select * from order_transac where order_date >= '{}' and order_date <= '{}' and order_status = 1
                order by order_priority,order_id
                limit {};"""\
                .format(min,max,head)
    cur.execute(sql)

    mobile_records = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return mobile_records


# On going, status = 2#
def update_order_list(order_barista,order_id,order_status=2):
    conn,cur = connection()
    sql = """update order_transac
            set order_barista = '{}',order_status = {}
            where order_id = {} """.format(order_barista,order_status,order_id)
    cur.execute(sql)

    conn.commit()
    cur.close()
    conn.close()
## For order transaction ##