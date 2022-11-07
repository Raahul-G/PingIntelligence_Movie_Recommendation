# For database models
from . import nlp_model

class Movies:

    def __init__(self):
        self.movie = None
        self.recommended = None

    def set_movie(self, movieName):
        self.movie = movieName

    def get_movie(self):
        return self.movie

    def get_recommendations(self):
        self.recommended = nlp_model.recommendations(self.movie)
        return self.recommended
