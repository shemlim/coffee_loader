import psycopg2
from datetime import timedelta,datetime


def call_time(local='server'):
    if local == 'server':
        date_now = datetime.now() + timedelta(hours=8)
    else:
        date_now = datetime.now()
    date = date_now.date()
    
    return [date_now,date]

## For order transaction ##
def insert_order(list_order,table_order,order_total,order_status,table_desc,priority=1):
    conn,cur = connection()
    sql = """insert into order_transac(order_table,order_details,order_priority,order_total,order_status,order_date,order_desc) 
            values({},'{}',{},{},{},'{}','{}');
          """.format(table_order,list_order,priority,order_total,order_status,call_time()[0],table_desc)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
## For order transaction ##

## For order menu category ##
def select_cat_menu():
    conn,cur = connection()
    sql = "select * from order_menu order by menu_available desc,menu_id;"
    cur.execute(sql)

    mobile_records = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return mobile_records
## For order menu category ##


def connection(local='server'):
    if local == 'server':
        # For server
        conn = psycopg2.connect(
            host="ec2-34-194-73-236.compute-1.amazonaws.com",
            database="dcluovhf5udvoh",
            user='vjrkfvpclacsbk',
            password='dbb1ed99cc03d72c142336ee06a97fb7d8776314b647b2c728bc3c0fd8b4e624')
    else:
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
    time = call_time()
    min = time[0]
    dt_today = time[1]
    print(dt_today)
    if min.hour <= 17:
        min = datetime.strftime(dt_today,"%Y-%m-%d 06:00:00")
    else:
        min = datetime.strftime(dt_today,"%Y-%m-%d 17:30:00")
    max = datetime.strftime(dt_today,"%Y-%m-%d 23:59:59")
    print('min,max',min,max)
    sql = "select count(*) from order_transac where order_date >= '{}' and order_date <= '{}' and order_status = 1;"\
            .format(min,max)
    cur.execute(sql)

    mobile_records = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return mobile_records

def select_only_id():
    conn,cur = connection()
    sql = ''
    time = call_time()
    min = time[0]
    dt_today = time[1]
    if min.hour <= 17:
        min = datetime.strftime(dt_today,"%Y-%m-%d 06:00:00")
    else:
        min = datetime.strftime(dt_today,"%Y-%m-%d 17:30:00")
    max = datetime.strftime(dt_today,"%Y-%m-%d 23:59:59")

    sql = """select order_id from order_transac where order_date >= '{}' and order_date <= '{}'
                    order by order_status,order_priority,order_id;"""\
                    .format(min,max)
    cur.execute(sql)
    mobile_records = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return mobile_records



def select_order_list(order_id=None,rand_str=None,head=1,min_date=None,max_date=None,table_id=None,list_of_excluded=[],all_status=0):
    conn,cur = connection()
    sql = ''
    time = call_time()
    min = '';max=''
    if (min_date == None) and (max_date == None):
        if order_id != None:
        
            sql = """select * from order_transac where order_id = {}"""\
                .format(order_id) if rand_str == None else \
                    """select * from order_transac where order_id = {} and order_rand_str='{}' """\
                .format(order_id,rand_str)

        else:
            min = time[0]
            dt_today = time[1]
            if min.hour <= 17:
                min = datetime.strftime(dt_today,"%Y-%m-%d 06:00:00")
            else:
                min = datetime.strftime(dt_today,"%Y-%m-%d 17:30:00")
            max = datetime.strftime(dt_today,"%Y-%m-%d 23:59:59")

            if table_id != None:
                sql = """select * from order_transac where order_date >= '{}' and order_date <= '{}' and order_status = 1
                        and order_rand_str is NULL and order_table = '{}'
                        order by order_priority,order_id
                        limit {};"""\
                        .format(min,max,table_id,head)

            elif len(list_of_excluded)!=0:
                sql = """select * from order_transac where order_date >= '{}' and order_date <= '{}' and order_status = 1
                        and order_rand_str is NULL and order_id not in %s
                        order by order_priority,order_id
                        limit {};"""\
                        .format(min,max,head)
                cur.execute(sql,(list_of_excluded,))

                mobile_records = cur.fetchall()
                conn.commit()
                cur.close()
                conn.close()
                return mobile_records
            
            elif all_status == 1:
                sql = """select * from order_transac where order_date >= '{}' and order_date <= '{}'
                        order by order_status,order_priority,order_id
                        limit {};"""\
                        .format(min,max,head)

            else:
                sql = """select * from order_transac where order_date >= '{}' and order_date <= '{}' and order_status = 1
                        and order_rand_str is NULL
                        order by order_priority,order_id
                        limit {};"""\
                        .format(min,max,head)
    else:
        min = min_date
        max = max_date

        sql = "select * from order_transac where order_date >= '{}' and order_date <= '{}' and order_status = 3;"\
            .format(min,max)

    
    cur.execute(sql)

    mobile_records = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return mobile_records


def select_order_status_list():
    conn,cur = connection()
    sql = ''
    time = call_time()
    min = time[0]
    dt_today = time[1]
    if min.hour <= 17:
        min = datetime.strftime(dt_today,"%Y-%m-%d 06:00:00")
    else:
        min = datetime.strftime(dt_today,"%Y-%m-%d 17:30:00")
    max = datetime.strftime(dt_today,"%Y-%m-%d 23:59:59")
    print('min,max',min,max)
    
    sql = """select * from order_transac where order_date >= '{}' and order_date <= '{}'
            order by order_status desc, order_priority asc,order_id asc;"""\
            .format(min,max)
    cur.execute(sql)

    mobile_records = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return mobile_records

# On going, status = 2#
def update_order_list(order_barista,order_id,order_rand_str=None,order_status=2):
    conn,cur = connection()
    sql = """
            update order_transac
            set order_barista = '{}',order_status = {}
            where order_id = {} and order_status = 1 and order_rand_str = '{}';
            
            """.format(order_barista,order_status,order_id,order_rand_str) if order_rand_str != None else \
            """
            update order_transac
            set order_barista = '{}',order_status = {}
            where order_id = {} ;
            
            """.format(order_barista,order_status,order_id)
    print(sql)
    cur.execute(sql)

    conn.commit()
    cur.close()
    conn.close()

def update_order_rndstr(order_rand_str,order_id,order_status=2):
    conn,cur = connection()
    
    sql = """
            
            update order_transac
            set order_rand_str = '{}'
            where order_id = {} and order_status = 1 and order_barista is NULL;
            
            """.format(order_rand_str,order_id)
    cur.execute(sql)

    conn.commit()
    cur.close()
    conn.close()
## For order transaction ##