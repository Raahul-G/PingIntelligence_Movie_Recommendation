# importing libraries
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Importing data file
movie_df = pd.read_csv('website/tmdb_5000_movies.csv')
credits_df = pd.read_csv('website/tmdb_5000_credits.csv')
credits_df.columns = ['id', 'title', 'cast', 'crew']
credits_df = credits_df.drop(columns=['title'])

# Merging into a main dataframe
movie_df = movie_df.merge(credits_df, on='id')

# Defining Tfidf vectorized object, to remove all english stopwords
tfidf = TfidfVectorizer(stop_words='english')

movie_df['overview'] = movie_df['overview'].fillna('')

tfidf_matrix = tfidf.fit_transform(movie_df['overview'])

# Compute the cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

indices = pd.Series(movie_df.index, index=movie_df['title']).drop_duplicates()


# Function that takes in movie title as input and outputs most similar movies
def get_recommendations(title, cosine_similarity=cosine_sim):
    # Get the index of the movie that matches the title
    if title in indices:
        idx = indices[title]
    else:
        return ['Sorry, We did not find this movie in the database']
    # Get the pairwise similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_similarity[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return movie_df['title'].iloc[movie_indices]


if __name__ == '__main__':
    get_recommendations("Batman Begins")
