#! flask/bin/python

from flask import Flask, render_template, request
import pymysql

# set up flask server details
app = Flask(__name__,static_url_path = "/static" , static_folder = "./static/")

# set up MySQL connection details
host = 'localhost'
port = 3306
user = 'My_SQL_USER'
passwd = 'MySQL_PASSWD'
db = 'capstone'


# set up Searching users info HTML page route
@app.route('/users')
def index():
    return render_template('/users.html')

@app.route('/info', methods = ['POST'])
def info():
    userName = request.form.get('name')
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset='utf8')
    cursor = conn.cursor()
    if userName != 'all':
        sql = '''SELECT * FROM users where name = "{}"'''.format(userName)
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
    else:
        sql = '''SELECT * FROM users'''
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        conn.close()

    print(data)
    return render_template('/users.html',
                            data=data)


# Set up Searching workout record HTML page route
@app.route('/workout')
def workout():
    return render_template('/workout.html')

@app.route('/record', methods = ['POST'])
def record():
    userno = request.form.get('userno')
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset='utf8')
    cursor = conn.cursor()
    # If client doesn't specify userno
    if userno != 'all':
        sql = '''SELECT name, muscle, sum(duration) FROM user_workout_record
         WHERE userno = "{}" GROUP BY name, muscle;'''.format(userno)
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
    # If client specify userno
    else:
        sql = '''SELECT name, muscle, sum(duration) FROM user_workout_record
         GROUP BY name, muscle;'''.format(userno)
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        conn.close()

    print(data)
    return render_template('/workout.html',
                            data=data)



# set up Searching workout record by user name HTML page
# Utilize JOIN SQL query
@app.route('/workoutbyname')
def workoutByName():
    return render_template('/user_work.html')

@app.route('/recordbyname', methods = ['POST'])
def recordByName():
    name = request.form.get('name')
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset='utf8')
    cursor = conn.cursor()
    # If client doesn't specify user name
    if name != 'all':
        sql = '''SELECT u.name, r.muscle, sum(r.duration)
         FROM users u JOIN user_workout_record r ON u.userno = r.userno
          WHERE u.name = "{}"
           GROUP BY u.name, r.muscle;'''.format(name)
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
    # If client specify user name
    else:
        sql = '''SELECT u.name, r.muscle, sum(r.duration)
                 FROM users u JOIN user_workout_record r ON u.userno = r.userno
                GROUP BY u.name, r.muscle;'''.format(name)
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        conn.close()

    print(data)
    return render_template('/user_work.html',
                            data=data)

# API for READing all user info
@app.route('/api/users/all', methods = ['GET'])
def getAllUesrs():
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset='utf8')
    cursor = conn.cursor()
    sql = '''SELECT * FROM users'''
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return (str(data))

# API for READing one user info by userno
@app.route('/api/users/<user_no>', methods = ['GET'])
def getOneUesrs(user_no):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset='utf8')
    cursor = conn.cursor()
    sql = '''SELECT * FROM users WHERE userno = "{}"'''.format(user_no)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return (str(data))



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)