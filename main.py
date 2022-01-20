from flask import Flask, render_template, request, redirect, session
import cx_Oracle
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

con = cx_Oracle.connect('system/sumit1311@127.0.0.1/XE')
cursor = con.cursor()


@app.route('/')
def login():
    return render_template('login.html')


# routes used to redirect multiple pages
@app.route('/register')
def about():
    return render_template("register.html")


@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template("home.html")
    else:
        return redirect('/')


@app.route('/login_validation', methods=['Post'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')
    cursor.execute("select * from users where email like '{}' and password like '{}'".format(email, password))
    user = cursor.fetchall()
    if len(user) > 0:
        session['user_id'] = user[0][0]
        return redirect('/home')
    else:
        return redirect('/')


@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('uname')
    email = request.form.get('email')
    password = request.form.get('password')
    # cursor.execute("insert into users values(:name,:email,:password)", (name, email, password))
    rows = [(name, email, password)]
    cursor.executemany("insert into users (name,email,password) values(:name,:email,:password)", rows)
    con.commit()
    cursor.execute("select * from users where email like '{}'".format(email))
    myuser = cursor.fetchall()
    session['user_id'] = myuser[0][0]
    return redirect('/home')


@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
