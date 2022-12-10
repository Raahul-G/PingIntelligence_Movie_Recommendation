# Importing libraries
import pandas as pd
import difflib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# loading data file
movie_df = pd.read_csv('website/tmdb_5000_movies.csv', index_col=0)
credits_df = pd.read_csv('website/tmdb_5000_credits.csv')
credits_df.columns = ['id', 'title', 'cast', 'crew']
credits_df = credits_df.drop(columns=['title'])

# Merging two data files
movie_df = movie_df.merge(credits_df, on='id')

# filtering out the specific features
selected_features = ['genres', 'keywords', 'tagline', 'cast', 'crew']

for feature in selected_features:
    movie_df[feature] = movie_df[feature].fillna('')

# specific features into list
combined_features = movie_df['genres'] + '' + movie_df['keywords'] + '' + movie_df['tagline'] + '' + movie_df[
    'cast'] + '' + movie_df['crew']

# Creating vector object
vector = TfidfVectorizer()
feature_vectors = vector.fit_transform(combined_features)

# cosine similarity
similarity = cosine_similarity(feature_vectors)


def movie_recommendation_double(user_title_1, user_title_2, cosine_sim=similarity):
    # getting input from user

    movie_title = movie_df['title'].tolist()
    #if user_title_1 not in movie_title:
    #    return ["The first movie is not in the list"]
    #elif user_title_2 not in movie_title:
    #    return['The second movie is not in the list']

    # finding close match in title
    close_matches_1 = difflib.get_close_matches(user_title_1, movie_title)
    close_matches_2 = difflib.get_close_matches(user_title_2, movie_title)

    close_match_1 = close_matches_1[0]
    close_match_2 = close_matches_2[0]

    # getting the index of the title entered by the user
    idx_of_the_movie_1 = movie_df[movie_df['title'] == close_match_1].index.values[0]
    idx_of_the_movie_2 = movie_df[movie_df['title'] == close_match_2].index.values[0]

    # calculating similarity score both the movies
    similarity_score_1 = list(enumerate(cosine_sim[idx_of_the_movie_1]))
    similarity_score_2 = list(enumerate(cosine_sim[idx_of_the_movie_2]))

    # combining the recommendation list and sorting it in desc order
    similar_movies_list = sorted(similarity_score_1 + similarity_score_2, key=lambda x: x[1], reverse=True)
    movie_recommendation_list = []

    count = 1
    for movies in similar_movies_list:
        idx = movies[0]
        movie_title = movie_df[movie_df.index == idx]['title'].values[0]
        if count <= 12:
            if count > 2:
                movie_recommendation_list.append(movie_title)
            count += 1
    return movie_recommendation_list

if __name__ == "__main__":
