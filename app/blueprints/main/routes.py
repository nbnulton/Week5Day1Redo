from flask import render_template, request  # importing flask package from Flask class
import requests
from flask_login import login_required
from .import bp as main

@main.route('/', methods = ['GET'])             # decorator, @app refers to variable above in constructor, # Flask class above gives us function called route
@login_required
def index():                # named index because we're doing main page index.html
    #return "Hello World"   # Flask class above gives us function called route
                            # '/' is the location, like the main or default page '/' (index.html), home page '/home', login page '/login'
    return render_template('index.html.j2')    # added html template

@main.route('/pokemon', methods = ['GET', 'POST'])
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


