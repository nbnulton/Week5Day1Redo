from flask import render_template, request, redirect, url_for     # importing flask package from Flask class
import requests
from config import Config
from app import app
from .forms import LoginForm, RegisterForm
from .models import User
from flask_login import login_user, current_user, logout_user, login_required



@app.route('/', methods = ['GET'])             # decorator, @app refers to variable above in constructor, # Flask class above gives us function called route
@login_required
def index():                # named index because we're doing main page index.html
    #return "Hello World"   # Flask class above gives us function called route
                            # '/' is the location, like the main or default page '/' (index.html), home page '/home', login page '/login'
    return render_template('index.html.j2')    # added html template
                           
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():     # when they submit the login
        # do login stuff
        email = request.form.get("email").lower()
        password = request.form.get("password")
                                # Database col = form inputed email
        u = User.query.filter_by(email=email).first()

        if u and u.check_hashed_password(password):
            return redirect(url_for("index"))
        error_string = "Invalid Email/Password combo"
        return  render_template('login.html.j2', error = error_string, form=form)
    return render_template('login.html.j2', form=form)

@app.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data = {
                "first_name":form.first_name.data.title(),
                "last_name":form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data
            }
            # create an empty user
            new_user_object = User()
            # build user with form data
            new_user_object.from_dict(new_user_data)
            # sve user to database
            new_user_object.save()
        except:
            error_string = "There was an unexpected error creating your account. Please try again."
            return render_template('register.html.j2', form=form, error = error_string) #1 when we had an error creating a user
        return redirect(url_for('login')) #2 on a POST request that successfully creates a new user
    return render_template('register.html.j2', form = form) #3 on the GET request

@app.route('/pokemon', methods = ['GET', 'POST'])
@login_required
def pokemon():
    if request.method == 'POST':    # if it's POST, now we need to get info
        pokemon = request.form.get('pokemon_name')   # grab name from form in ergast ('year') info out of form, getting an immutable dictionary so we can't change it, .get works with dictionaries, will return what we need, if nothing will return NONE
        url = f'https://pokeapi.co/api/v2/pokemon/pikachu'
        response = requests.get(url)    #this is like GET, getting the request to url, not dictionary
        if response.ok:     # if it worked
            # the request worked

            if not response.json():
                return "We had an error loading your data"
            data = response.json()
            all_pokemon=[]
            for pokemon in data:
                pokemon_dict={
                    'name':data['forms'][0]['name'],
                    'hp':data['stats']['base-stat'],
                    'attack':data['stats']['base-stat'],
                    'defense':data['stats']['base-stat'],
                    'sprite_url':data['sprites']['front_shiny']
                }
                all_pokemon.append(pokemon_dict)       # HTML = app.py dict
            return render_template('pokemon.html.j2', pokemon=all_pokemon)
        else:
            return "House we had a problem, connection error"
            # The request failed, response != ok, something in url = f'(url)' above didn't work, link broken, server down

    return render_template('pokemon.html.j2')


