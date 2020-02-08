import os
import secrets
from PIL import Image
from datetime import datetime
import requests
import json
from flask import render_template, url_for, redirect, request, flash #for message
from businessnews.forms import RegistrationForm,UpdateAccountForm, LoginForm, SearchForm
from businessnews.models import User, Post
from businessnews import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

#NEWS API:
url1 = ('https://newsapi.org/v2/top-headlines?'
'country=in&'
# 'q=reliance&'
'category=business&'
'apiKey=78570fe479ef410dbf5c854c5102ef3c')
response1 = requests.get(url1)
d1 = json.loads(response1.text)


def find_category(form):
    if form.sports.data == True:
        return 'sports'
    elif form.entertainment.data == True:
        return 'entertainment'
    elif form.technology.data == True:
        return 'technology'
    elif form.health.data == True:
        return 'heath'
    elif form.science.data == True:
        return 'science'
    else:
        return 'business'

@app.route("/", methods=['GET','POST'])
@app.route("/home", methods=['GET','POST'])
def home():
    form = SearchForm()
    if form.validate_on_submit():
        category = find_category(form)
        # start = form.start_date.data
        # end = form.end_date.data
        url2 = ('https://newsapi.org/v2/top-headlines?'
        'country=in&'
        'q={}&'
        'category={}&'
        'apiKey=78570fe479ef410dbf5c854c5102ef3c'.format(form.keyword.data,category))
        print(url2)
        response2 = requests.get(url2)
        d2 = json.loads(response2.text)
        return render_template('home.html', posts = d2['articles'],form=form)

    return render_template('home.html', posts = d1['articles'],form=form)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # flash(f'Account Created Successfully for {form.username.data}','success')
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created Successfully!','success')
        return redirect(url_for('home')) #name of function for that route
    return render_template('register.html', title='Register',form  =form)

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated :
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next') #[] dont use it will show error if page not exit in dictionary
            return redirect(next_page if next_page else url_for('home')) #name of function for that route
        else:
            flash(f'Unsuccessfull Login','danger')
    return render_template('login.html', title='Login',form  =form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8) #randomise image name as it can collide
    _, f_ext = os.path.splitext(form_picture.filename)  #file_name will be unused
    picture_fn  = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics',picture_fn)

    i = Image.open(form_picture)
    i.thumbnail((125,125))  #125px 125 px scaling of image to make website fast
    i.save(picture_path)

    return picture_fn

@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account updated Successfully','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    return render_template('account.html', title = 'Account', image_file = image_file, form = form)
