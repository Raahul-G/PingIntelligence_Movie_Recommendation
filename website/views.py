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
        movie_obj.set_movie(request.form.get('movieSearch'))

        return redirect(url_for('views.similar'))
    return render_template('home.html')

@views.route('/similar', methods = ['GET', 'POST'])
def similar():
    return render_template('similar.html', movie = movie_obj.get_movie(),
                           recommended = movie_obj.get_recommendations())