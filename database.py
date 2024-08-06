import sqlite3

def get_connection() :
    return sqlite3.connect("Working_Hours")
def create_table() :
    try :
        new_connection = get_connection()
        cursor = new_connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS STAFF(
                    ID TEXT,
                    PASSWORD TEXT NOT NULL,
                    WORKING_HOURS TEXT,
                    HOURLY_RATE FLOAT NOT NULL,
                    TOTAL_MONTH_PAY FLOAT,
                    TOTAL_TIME_PAY FLOAT,
                    MONTH TEXT,
                    LAST_DAY_WORKED TEXT,
                    ROLE TEXT,
                    CONSTRAINT pk_STAFF PRIMARY KEY(ID)
                    );""")
        new_connection.commit()
        new_connection.close()

        return 1
    except :
        new_connection.close()
        return 0

def insert_new_member(id,password,hourly_rate,today_month) :
    new_connection = get_connection()
    cursor = new_connection.cursor()
    values = (id,password,hourly_rate,0,0,0,today_month,"-1")
    cursor.execute('''INSERT INTO STAFF (ID,PASSWORD,HOURLY_RATE,WORKING_HOURS,TOTAL_MONTH_PAY,TOTAL_TIME_PAY,MONTH,LAST_DAY_WORKED)
    VALUES (?,?,?,?,?,?,?,?)''',values)
    new_connection.commit()
    new_connection.close()


def update_role(id,role) :
    new_connection = get_connection()
    cursor = new_connection.cursor()
    cursor.execute(f"UPDATE STAFF SET ROLE = '{role}' WHERE ID = '{id}'")
    new_connection.commit()
    new_connection.close()

def get_all_id() :
    try :
        new_connection = get_connection()
        cursor = new_connection.cursor()
        cursor.execute("SELECT ID FROM STAFF")
        list_id = cursor.fetchall()
        new_connection.close()
        return list_id
    except :
        return None

def login_authenticate(id,password) :
    new_connection = get_connection()
    cursor = new_connection.cursor()
    cursor.execute(f"SELECT * FROM STAFF WHERE ID = '{id}'")
    list_credentials = cursor.fetchone()
    print(list_credentials)
    if not list_credentials :
        new_connection.close()
        return 0
    elif list_credentials[1] != password :
        new_connection.close()
        return -1
    else :
        new_connection.close()
        return 1

def reset_total_month_pay(id) :
    new_connection = get_connection()
    cursor = new_connection.cursor()
    cursor.execute(f"UPDATE STAFF SET TOTAL_MONTH_PAY = '0' WHERE ID = '{id}'")
    new_connection.commit()
    new_connection.close()

def update_user_data(id,hours,date) :
    new_connection = get_connection()
    cursor = new_connection.cursor()
    cursor.execute(f"SELECT WORKING_HOURS FROM STAFF WHERE ID = '{id}' ")
    working_hours = cursor.fetchone()
    working_hours_to_save = float(working_hours[0]) + float(hours)
    working_hours_to_save = round(working_hours_to_save,2)
    cursor.execute(f"UPDATE STAFF SET WORKING_HOURS = '{working_hours_to_save}' WHERE ID = '{id}'")
    cursor.execute(f"SELECT TOTAL_MONTH_PAY FROM STAFF WHERE ID = '{id}'")
    total_month_pay = cursor.fetchone()
    cursor.execute(f"SELECT HOURLY_RATE FROM STAFF WHERE ID = '{id}'")
    hourly_rate = cursor.fetchone()
    total_month_pay_new = (hours * hourly_rate[0]) + total_month_pay[0]
    cursor.execute(f"UPDATE STAFF SET TOTAL_MONTH_PAY = '{total_month_pay_new}' WHERE ID = '{id}'")
    cursor.execute(f"SELECT TOTAL_TIME_PAY FROM STAFF WHERE ID = '{id}'")
    total_pay = cursor.fetchone()
    total_pay_new = (hours * float(hourly_rate[0])) + total_pay[0]
    cursor.execute(f"UPDATE STAFF SET TOTAL_TIME_PAY = '{total_pay_new}' WHERE ID='{id}'")
    cursor.execute(f"UPDATE STAFF SET LAST_DAY_WORKED = '{date}' WHERE ID = '{id}'")
    new_connection.commit()
    new_connection.close()
def get_user_date(id) :
    new_connection = get_connection()
    cursor = new_connection.cursor()
    cursor.execute(f"SELECT LAST_DAY_WORKED FROM STAFF WHERE ID = '{id}'")
    user_date = cursor.fetchone()
    new_connection.commit()
    if user_date[0] == None :
        new_connection.close()
        return "NONE"
    else :
        new_connection.close()
        print("user date =>",user_date[0])
        return user_date[0]

def get_user_month(id) :
    new_connection = get_connection()
    cursor = new_connection.cursor()
    cursor.execute(f"SELECT MONTH FROM STAFF WHERE ID = '{id}'")
    user_date = cursor.fetchone()
    new_connection.commit()
    if user_date[0] == None:
        new_connection.close()
        return "NONE"
    else:
        new_connection.close()
        return user_date[0]

def get_user_role(id) :
    new_connection = get_connection()
    cursor = new_connection.cursor()
    cursor.execute(f"SELECT ROLE FROM STAFF WHERE ID = '{id}'")
    user_role = cursor.fetchone()
    return user_role[0]

def get_all_users_view() :
    new_connection = get_connection()
    cursor = new_connection.cursor()
    cursor.execute("SELECT ID,WORKING_HOURS,TOTAL_MONTH_PAY,TOTAL_TIME_PAY FROM STAFF")
    users_data = cursor.fetchall()

    users = []
    for user in users_data :
        users.append(user)
    new_connection.commit()
    new_connection.close()
    return users



def get_specific_user_view(id) :
    new_connection = get_connection()
    cursor = new_connection.cursor()
    cursor.execute(f"SELECT WORKING_HOURS,TOTAL_MONTH_PAY,TOTAL_TIME_PAY FROM STAFF WHERE ID = '{id}'")
    users_data = cursor.fetchone()
    new_connection.close()
    return users_data

