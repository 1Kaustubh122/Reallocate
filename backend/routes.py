from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, join_room, send
import os
from backend.forms import RentReg, RentLog, CustLog, CustReg
from backend.models import Rent_User, Customer
from backend import app, db  # Import app and db from the package
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user


# socketio = SocketIO(app)

# Ensure the upload directories exist
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'images'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'videos'), exist_ok=True)


UPLOAD_FOLDER = 'static/uploads/'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_type = request.form['user_type']
        username = request.form['username']
        password = request.form['password']
        
        if user_type == 'renter':
            user = Rent_User(username=username, password=password, role='renter')
        else:
            user = Rent_User(username=username, password=password, role='service_provider')
        
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

# Login route
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Rent_User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            session['user_id'] = user.id
            session['role'] = user.role
            
            if user.role == 'renter':
                return redirect(url_for('renter_dashboard'))
            else:
                return redirect(url_for('service_provider_dashboard'))
        else:
            return 'Invalid credentials!'
    return render_template('login.html')


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/register_customer', methods=['GET', 'POST'])
def register_customer():
    if request.method == 'POST':
        name = request.form.get('name')
        phone_number = request.form.get('phone_number')
        location = request.form.get('location')
        aadhar_number = request.form.get('aadhar_number')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        print(name,phone_number,location,aadhar_number,email,password)


        if Customer.query.filter_by(email_address=email).first():
            flash('Email already registered. Please use a different email.', 'danger')
            return render_template('customer_register.html',name=name, phone_number=phone_number,location=location,aadhar_number=aadhar_number,email=email)
        
        if Customer.query.filter_by(aadhar_number=aadhar_number).first():
            flash('Aadhar already registered. Please use a different Aadhar.', 'danger')
            return render_template('customer_register.html',name=name, phone_number=phone_number,location=location,aadhar_number=aadhar_number,email=email)
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('customer_register.html',name=name, phone_number=phone_number,location=location,aadhar_number=aadhar_number,email=email)


        # Create a new user record
        new_user = Customer(
            name=name,
            phone_number=phone_number,
            location=location,
            aadhar_number=aadhar_number,
            email_address=email,
            password_hash=generate_password_hash(password)  # Encrypt the password
        )

        # Add and commit the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login_customer'))

    return render_template('customer_register.html')


@app.route('/customer_login', methods=['GET', 'POST'])
def login_customer():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(email, password)

        # Find the user by email
        user = Customer.query.filter_by(email_address=email).first()
        
        # Check if user exists and password is correct
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('customer_dashbord'))
        else:
            flash('Login unsuccessful. Please check your email and password', 'danger')

    return render_template('customer_login.html')



@app.route('/renter_login', methods=['GET', 'POST'])
def login_renter():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(email, password)

        # Find the user by email
        user = Rent_User.query.filter_by(email_address=email).first()
        
        # Check if user exists and password is correct
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login successful!', 'success')
            return "LOGIN HOGYA BSDK" # Redirect to home or desired page
        else:
            flash('Login unsuccessful. Please check your email and password', 'danger')

    return render_template('renter_login.html')


@app.route('/renter_register', methods=['GET', 'POST'])
def register_renter():
    if request.method == 'POST':
        name = request.form.get('name')
        phone_number = request.form.get('phone_number')
        location = request.form.get('location')
        aadhar_number = request.form.get('aadhar_number')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        print(name,phone_number,location,aadhar_number,email,password)

        # Check if the email already exists
        if Rent_User.query.filter_by(email_address=email).first():
            flash('Email already registered. Please use a different email.', 'danger')
            return render_template('renter_register.html',name=name, phone_number=phone_number,location=location,aadhar_number=aadhar_number,email=email)
        
        if Rent_User.query.filter_by(aadhar_number=aadhar_number).first():
            flash('Aadhar already registered. Please use a different Aadhar.', 'danger')
            return render_template('renter_register.html',name=name, phone_number=phone_number,location=location,aadhar_number=aadhar_number,email=email)


        # Validate the password confirmation
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('renter_register.html',name=name, phone_number=phone_number,location=location,aadhar_number=aadhar_number,email=email)

        # Create a new user record
        new_user = Rent_User(
            name=name,
            phone_number=phone_number,
            location=location,
            aadhar_number=aadhar_number,
            email_address=email,
            password_hash=generate_password_hash(password)  # Encrypt the password
        )

        # Add and commit the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login_renter'))

    return render_template('renter_register.html')

@app.route('/customer_dashbord')
@login_required
def customer_dashbord():
    return render_template('customer_dashbord.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('index'))



