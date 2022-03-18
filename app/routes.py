from app import app, db
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from app.models import User, Property
from app.map import create_map
import time
import requests
import hashlib


@app.route('/')
def home():
    print(current_user.is_anonymous)
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email.lower()).first()
        if user is None or not user.check_password(password):
            flash('invalid e-mail or password', 'danger')
            return redirect(request.referrer)
        flash('login successful!', 'success')    
        login_user(user)
        return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(email=data.get('email')).first()
        if user is not None:
            flash('an account associated with your e-mail is already on file', 'warning')
            return redirect(request.referrer)
        if data.get('password') != data.get('password2'):
            flash('passwords do not match!', 'warning')
            return redirect(request.referrer)
        new_user = User(
            name =data.get('name'),
            email=data.get('email'),
            password=data.get('password')
        )
        db.session.add(new_user)
        db.session.commit()

        flash('registration successful! - you are now logged in', 'success')
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template('register.html')


@app.route('/logout')
def logout():
    logout_user()
    flash('successfully logged out', 'primary')
    return render_template('home.html')
  

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form
        # home = Property.query.filter_by(address=data.get('address')).first()
        # if user is not None:
        #     flash('an account associated with your e-mail is already on file', 'warning')
        #     return redirect(request.referrer)
        # if data.get('password') != data.get('password2'):
        #     flash('passwords do not match!', 'warning')
        #     return redirect(request.referrer)
        new_home = Property(
            address=data.get('address'),
            nickname=data.get('nickname'),
            bedrooms=data.get('bedrooms'),
            bathrooms=data.get('bathrooms'),
            impressions=data.get('impressions'),
            user_id=current_user.id,
        )
        db.session.add(new_home)
        db.session.commit()
        flash('registration successful! - you are now logged in', 'success')
        return redirect(url_for('home'))
    return render_template('add_home.html')


@app.route('/view')
def view():
    homes = Property.query.filter_by(user_id=current_user.id).all()
    collection = [] 
    for h in homes:
            homes_dict = {
            'address': h.address,    
            'nickname': h.nickname,
            'bedrooms': h.bedrooms,
            'bathrooms': h.bathrooms,
            'impressions': h.impressions,
            }
            collection.append(homes_dict)
    context = {
        'homes': collection
    }
    return render_template('view.html', **context)


@app.route('/map_request', methods=['GET', 'POST'])
def map():
    if request.method == 'POST':
        address = request.form.get('address')
        if create_map(address) == False:
            flash('no record for that address - please try again', 'warning')
            return redirect(request.referrer)    
        else:       
            time.sleep( 3 )
            return render_template('final_map.html')
    return render_template('map_request.html')

    