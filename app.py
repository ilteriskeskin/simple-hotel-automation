from flask import Flask, render_template, flash, redirect, request, session, logging, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegisterForm, CustomerForm
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os

# Kullanıcı giriş decorator ü
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Bu sayfayı görüntülemek için lütfen giriş yapın.', 'danger')
            return redirect(url_for('login'))
    return decorated_function

app = Flask(__name__)
app.config['SECRET_KEY'] = 'linuxdegilgnulinux'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/ilteriskeskin/Belgeler/Flask/hotel_automation/otel.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(15), unique = True)
    password = db.Column(db.String(25), unique = True)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(15), unique = True)
    email = db.Column(db.String(50), unique = True)
    tel = db.Column(db.Integer, unique = True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/customer_view/')
@login_required
def customer_view():
    customers = Customer.query.all()
    return render_template('customer_view.html', customers = customers)

@app.route('/register/', methods = ['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(email = form.email.data, password = hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Başarılı bir şekilde kayıt oldunuz', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('register.html', form = form)

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate:
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                flash("Başarıyla Giriş Yaptınız", "success")
                
                session['logged_in'] = True
                session['email'] = user.email 

                return redirect(url_for('home'))
            else:
                flash("Email veya Parola Yanlış", "danger")
                return redirect(url_for('login'))

    return render_template('login.html', form = form)

@app.route('/customer_add/', methods = ['GET', 'POST'])
@login_required
def customer_add():
    form = CustomerForm(request.form)
    if request.method == 'POST' and form.validate():
        new_user = Customer(name = form.name.data, email = form.email.data, tel = form.tel.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Başarılı bir şekilde müşteri eklediniz', 'success')
        return redirect(url_for('customer_add'))
    else:
        return render_template('customer_add.html', form = form)

@app.route('/delete/<string:id>')
@login_required
def deleteCustomer(id):
    customer = Customer.query.filter_by(id = id).first()
    db.session.delete(customer)
    db.session.commit()

    return redirect(url_for('customer_view'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)