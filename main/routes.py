from main import app, db, bcrypt
from flask import redirect, render_template, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from main.forms import LoginForm, RegistrationForm
from main.models import User
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('dashboard'))
    form = LoginForm(request.form)
    if form.validate_on_submit() and request.method == 'POST':
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                form.password.data) and user.role == form.role.data:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                if form.role.data == 'customer':
                    return redirect(url_for('customer_dashboard'))
                else:
                    return redirect(url_for('seller_dashboard'))
        else:
            flash('Please check your credentials', 'danger')
    return render_template('login.html', form=form, title='Login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = \
            bcrypt.generate_password_hash(form.password.data).decode('utf-8'
                )
        user = User(username=form.username.data, email=form.email.data,
                    password=hashed_pwd, role = form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! Please Login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard/customer')
@login_required
def customer_dashboard():
    return render_template('customer_dashboard.html')

@app.route('/dashboard/seller')
@login_required
def seller_dashboard():
    return render_template('seller_dashboard.html')