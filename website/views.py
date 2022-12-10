from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from . import db
import json
from .models import Movies

views = Blueprint('views', __name__)
movie_obj = Movies()

@views.route('/', methods = ['GET', 'POST'])       # This is the home dirctory of the website
def home():             # This function will run whenever you go to the route mentioned above it
    if request.method == 'POST':

        if 'find' in request.form:
            movie_obj.set_movie1(request.form.get('movieSearch'))
            return redirect(url_for('views.similar_single'))
        else:
            return redirect(url_for('views.double'))

    return render_template('home.html')

@views.route('/double', methods = ['GET', 'POST'])       # This is the home dirctory of the website
def double():             # This function will run whenever you go to the route mentioned above it
    if request.method == 'POST':
        if 'find' in request.form:
            movie_obj.set_movie1(request.form.get('movieSearch1'))
            movie_obj.set_movie2(request.form.get('movieSearch2'))
            print(movie_obj.get_movie1())
            print(movie_obj.get_movie2())
            return redirect(url_for('views.similar_double'))
        else:
            return redirect(url_for('views.home'))

    return render_template('double.html')

@views.route('/similar_single', methods = ['GET', 'POST'])
def similar_single():
    if request.method == 'POST':
        return redirect(url_for('views.home'))
    return render_template('similar_single.html', movie = movie_obj.get_movie1(),
                           recommended = movie_obj.get_recommendations_single())

@views.route('/similar_double', methods = ['GET', 'POST'])
def similar_double():
    if request.method == 'POST':
        return redirect(url_for('views.double'))
    return render_template('similar_double.html', movie1 = movie_obj.get_movie1(),
                           movie2 = movie_obj.get_movie2(),
                           recommended = movie_obj.get_recommendations_double())