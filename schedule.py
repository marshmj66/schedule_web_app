from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'Marshall'
app.config['MYSQL_PASSWORD'] = 'Allstar77'
app.config['MYSQL_DB'] = 'schedule'

mysql = MySQL(app)
data_save = []

@app.route("/",methods=['GET','POST'])
def home():
    if request.method == 'POST':
        statment = 0
        #details = request.form.get('login_form')
        test_username = request.form.get('un')
        test_password = request.form.get('pwd')

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM login_info")
        info = cur.fetchall()
        for i in info[0]:
            if i == test_username or i == test_password:
                statment += 1
        if statment == 2:
            data_save.append(test_username)
            data_save.append(test_password)
            cur.execute('SELECT * FROM schedule')
            event = cur.fetchall()
            cur.close()
            return render_template('index.html',info=test_username,event=event)
        else:

            return render_template('index.html',info='wrong user information')
    elif request.method == 'GET':
        check_box_data = request.args.get('check')
        print('this', check_box_data)
        print(set(data_save))
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM schedule')
        event = cur.fetchall()
        if check_box_data != None:
            print(check_box_data)
            cur.execute(f'UPDATE schedule SET task_completion = 1 WHERE ID = {int(check_box_data)}')
            mysql.connection.commit()
        if len(data_save) > 1:
            return render_template('index.html',info=data_save[0], event=event,)
        else:
            return render_template('index.html',info=None)

    else:
        return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')