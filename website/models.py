# For database models
from . import nlp_model, mark2

class Movies:

    def __init__(self):
        self.movie1 = None
        self.movie2 = None
        self.recommended = None

    def set_movie1(self, movieName):
        self.movie1 = movieName

    def set_movie2(self, movieName):
        self.movie2 = movieName

    def get_movie1(self):
        return self.movie1

    def get_movie2(self):
        return self.movie2

    def get_recommendations_single(self):
        self.recommended = nlp_model.get_recommendations(self.movie1)
        return self.recommended

    def get_recommendations_double(self):
        self.recommended = mark2.movie_recommendation_double(self.movie1, self.movie2)
        return self.recommended
