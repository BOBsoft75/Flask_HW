from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from forms import RegisterForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)
# db = SQLAlchemy(app)


category = [
    {"title": 'Home page', "func_name": 'index'},
]


@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html', category=category)
# def index():
#     return 'Hi!'


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('Ok')


# @app.cli.command("add-john")
# def add_user():
#     user = User(username='john', usersurname='johnson', password='12345',
#                 email='john@example.com')
#     db.session.add(user)
#     db.session.commit()
#     print('John added to DB!')


@app.route('/log/', methods=['GET', 'POST'])
def log():
    if request.method == 'POST':
        session['username'] = request.form.get('username')
        session['usersurname'] = request.form.get('usersurname')
        session['email'] = request.form.get('email')
        session['password'] = request.form.get('password')
        user = User(username={session['username']}, usersurname={session['usersurname']},
                    email={session['email']}, password={session['password']})
    db.session.add(user)
    db.session.commit()
    print('User added to DB!')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
