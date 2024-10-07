from flask import render_template, request, redirect, url_for, flash, send_file, make_response, jsonify, Blueprint
from flask_login import login_user, login_required, logout_user, current_user, fresh_login_required
from werkzeug.security import generate_password_hash, check_password_hash
from backend import app, db, socketio
from backend.models import Customer, Rent_User
import PIL.Image as Image
import io


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

        if (not(aadhar_number.isdigit)) or (len(aadhar_number) != 12):
            flash('Invalid aadhar.', 'danger')
            return render_template('customer_register.html', name=name, phone_number=phone_number, location=location, aadhar_number=aadhar_number, email=email)
        
        if (not (phone_number.isdigit()) or not (len(phone_number) == 10 )):
            flash('Invalid Contact Number.', 'danger')
            return render_template('customer_register.html', name=name, phone_number=phone_number, location=location, aadhar_number=aadhar_number, email=email)
        

        if Customer.query.filter_by(email_address=email).first():
            flash('Email already registered. Please use a different email.', 'danger')
            return render_template('customer_register.html', name=name, phone_number=phone_number, location=location, aadhar_number=aadhar_number, email=email)
        
        if Customer.query.filter_by(aadhar_number=aadhar_number).first():
            flash('Aadhar already registered. Please use a different Aadhar.', 'danger')
            return render_template('customer_register.html', name=name, phone_number=phone_number, location=location, aadhar_number=aadhar_number, email=email)
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('customer_register.html', name=name, phone_number=phone_number, location=location, aadhar_number=aadhar_number, email=email)
        
        try:
            new_user = Customer(
                name=name,
                phone_number=phone_number,
                location=location,
                aadhar_number=aadhar_number,
                email_address=email,
                password_hash=generate_password_hash(password)
            )

            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login_customer'))
        except:
            flash('Invalid details found', 'danger')
            return render_template('customer_register.html', name=name, phone_number=phone_number, location=location, aadhar_number=aadhar_number, email=email)


    return render_template('customer_register.html')


@app.route('/customer_login', methods=['GET', 'POST'])
def login_customer():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Customer.query.filter_by(email_address=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=True)
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

        user = Rent_User.query.filter_by(email_address=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=True)
            flash('Login successful!', 'success')
            return redirect(url_for('renter_dashboard'))
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

        if Rent_User.query.filter_by(email_address=email).first():
            flash('Email already registered. Please use a different email.', 'danger')
            return render_template('renter_register.html', name=name, phone_number=phone_number, location=location, aadhar_number=aadhar_number, email=email)
        
        if Rent_User.query.filter_by(aadhar_number=aadhar_number).first():
            flash('Aadhar already registered. Please use a different Aadhar.', 'danger')
            return render_template('renter_register.html', name=name, phone_number=phone_number, location=location, aadhar_number=aadhar_number, email=email)

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('renter_register.html', name=name, phone_number=phone_number, location=location, aadhar_number=aadhar_number, email=email)

        new_user = Rent_User(
            name=name,
            phone_number=phone_number,
            location=location,
            aadhar_number=aadhar_number,
            email_address=email,
            password_hash=generate_password_hash(password)
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login_renter'))

    return render_template('renter_register.html')

@app.route('/renter_dashboard', methods=['GET', 'POST'])
def renter_dashboard():
    
    if request.method == 'POST':
        product_name = request.form['product']
        product_images = request.files.getlist('Pimage')
        product_video = request.files['Pvideo']
        purchase_date = request.form['PDOP']
        product_description = request.form['Pdescription']
        price = request.form['Price']

 
        image_binaries = [image.read() for image in product_images]
        img_stream = io.BytesIO(image_binaries[0])

        

        video_binary = product_video.read()

        new_product = Rent_User(
            name=product_name,
            Pdescription=product_description,
            PDOP=purchase_date,
            Price=price,
            Pimage=img_stream.getvalue(),
            Pvideo=video_binary
            # user_id=current_user.id
        )

        # print(current_user.id)

        db.session.add(new_product)
        db.session.commit()
        print(product_name, product_description, purchase_date, price, new_product)

        flash('Product details submitted successfully!', 'success')
        return redirect(url_for('renter_dashboard'))

    return render_template('renter_dashboard.html', user=current_user)

@app.route('/register_service', methods=['GET', 'POST'])
def register_service():
    if request.method == 'POST':
        name = request.form.get('name')
        phone_number = request.form.get('phone_number').strip()
        location = request.form.get('location')
        service = request.form.get('service')
        Sdescription = request.form.get('Sdescription')
        experience = request.files.get('experience')
        aadhar_number = request.form.get('aadhar_number')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        profile_pic = request.files.get('profile_pic')

        if profile_pic and profile_pic.filename != '':
            Pimage = profile_pic.read()
        else:
            Pimage = None

        if Rent_User.query.filter_by(aadhar_number=aadhar_number).first():
            flash('Aadhar already registered. Please use a different Aadhar.', 'danger')
            return render_template('service_register.html', name=name, phone_number=phone_number, location=location, service=service, experience=experience, aadhar_number=aadhar_number)
        
        if Rent_User.query.filter_by(phone_number=phone_number).first():
            flash('Aadhar already registered. Please use a Phone Number.', 'danger')
            return render_template('service_register.html', name=name, phone_number=phone_number, location=location, service=service, experience=experience, aadhar_number=aadhar_number)

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('service_register.html', name=name, phone_number=phone_number, location=location, service=service, experience=experience, aadhar_number=aadhar_number)
        
        new_user = Rent_User(
            name=name,
            phone_number=phone_number,
            location=location,
            service=service,  
            Sdescription=Sdescription,
            experience=experience,
            aadhar_number=aadhar_number,
            password_hash=generate_password_hash(password),
            Pimage=Pimage
        )


        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login_service'))
   

    return render_template('service_register.html')

@app.route('/service_login', methods=['GET', 'POST'])
def login_service():
    if request.method == 'POST':
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')
        

        user = Rent_User.query.filter_by(phone_number=phone_number).first()
        print(user.service)
      
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=True)
            flash('Login successful!', 'success')
            print("Login SUCCESS")
            return render_template('service_dashbord.html', user=current_user)
        else:
            print("Login FAILED")

            flash('Login unsuccessful. Please check your Phone Number and password', 'danger')

    return render_template('service_login.html')

# @app.route('/service_dashboard')
# # @login_required
# def service_dashboard():
#     print(current_user)
#     return render_template('service_dashbord.html', user=current_user)

@app.route('/customer_dashbord')
@login_required
def customer_dashbord():
    if not isinstance(current_user, Customer):
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))
    return render_template('customer_dashbord.html')


@app.route('/service')
@login_required
def view_service():
    service = request.args.get('service')
    print(service)
    service_providers = Rent_User.query.filter_by(service=service).all()
    print(service_providers)


    provider_details = []
    for provider in service_providers:
        provider_info = {
            'id': provider.id,  # Assuming 'id' is a column in your Rent_User model
            'name': provider.name,  # Adjust this to your actual provider name field
            'service': provider.service,  # The service offered
            'location': provider.location,  # Assuming you have a location field
            'experience': provider.experience,  # Assuming you have an experience field
            # 'rate': provider.rate,  # Uncomment if you have a rate field
            'rating': provider.Srating,  # Assuming you have a rating field
            'description': provider.Sdescription  # The service description
        }
        provider_details.append(provider_info)

    # Pass the provider details directly to the template
    return render_template('service_list.html', providers=provider_details)





@app.route('/image/<int:product_id>')
def get_image(product_id):
    product = Rent_User.query.get(product_id)
    if product and product.Pimage:
        return send_file(io.BytesIO(product.Pimage), mimetype='image/jpeg')  # Adjust mimetype if necessary
    return "Image not found", 404


@app.route('/product')
@login_required
def view_product():
    product_name = request.args.get('product')
    print(product_name)
    products = Rent_User.query.filter_by(name=product_name).all()
    print(len(products))

    return render_template('rental_list.html', products=products)

@app.route('/rent')
@login_required
def rent():
   
    product_ = request.args.get('product_id')
    product = Rent_User.query.get(product_)

    print(product.name)

    # product = Rent_User.query.get(product_id)

    return render_template('Rent_now.html', product=product)


@app.route('/product/<int:product_id>')
@login_required
def product_details(product_id):
    # Fetch product details from the database
    product = Rent_User.query.get(product_id)  # Assuming Rent_User holds the product information
    if not product:
        flash('Product not found', 'danger')
        return redirect(url_for('rent'))  # Redirect to rent page if product not found
    
    return render_template('product_details.html', product=product)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('index'))



@app.route('/book_services')
def Book_Service():
    return render_template('Book_service.html')

@app.route('/view_services')
def View_Profile():
    return render_template('view_service_profile.html')

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    response = make_response(redirect(url_for("login_page")))  # Create response to set headers
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    return response



