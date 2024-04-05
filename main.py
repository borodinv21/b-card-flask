from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.mail.ru'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///card.db'
db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Student %r>' % self.id




@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        phone = request.form['phone']

        if name != '' and age != '' and email != '' and phone != '':
            student = Student(name=name, age=age, email=email, phone=phone)
            print(email)
            message = Message("HEllo", sender=app.config['MAIL_USERNAME'], recipients=[email])
            message.body = f"Я {name} хочу учиться!"
            mail.send(message)
        else:
            return render_template('index.html', error="static/js/test.js")

        try:
            db.session.add(student)
            db.session.commit()
            return redirect('/')
        except:
            return render_template('index.html', error="static/js/test.js")
    else:
        return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)

