import pandas as pd
import numpy as np
from rake_nltk import Rake
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

df = pd.read_csv('https://query.data.world/s/uikepcpffyo2nhig52xxeevdialfl7')

# Narrowing data table to columns with natural language data
df = df[['Title','Genre','Director','Actors','Plot']]

# Tokenizing the words in the Genre category by splitting with commas
df['Genre'] = df['Genre'].map(lambda x: x.lower().split(','))

# Keeping only the names of the first 3 actors and combining their names into one word
df['Actors'] = df['Actors'].map(lambda x: x.split(',')[:3])
for ind, row in df.iterrows():
    row['Actors'] = [x.lower().replace(' ','') for x in row['Actors']]

# Combining the director name into one word
df['Director'] = df['Director'].map(lambda x: x.split(' '))
for ind, row in df.iterrows():
    row['Director'] = ''.join(row['Director']).lower()

# initializing the new column
df['Key_words'] = ""

for ind, row in df.iterrows():
    plot = row['Plot']

    # Initializing Rake
    r = Rake()

    # extracting words from the plot
    r.extract_keywords_from_text(plot)

    # making a dictionary of word count
    key_words_dict_scores = r.get_word_degrees()

    # setting new column equal to the word count dictionary
    row['Key_words'] = list(key_words_dict_scores.keys())

# dropping the Plot column
df = df.drop(columns=['Plot'])

df.set_index('Title', inplace = True)

df['bag_of_words'] = ''
columns = df.columns
for index, row in df.iterrows():
    words = ''
    for col in columns:
        if col != 'Director':
            words = words + ' '.join(row[col]) + ' '
        else:
            words = words + row[col] + ' '
    row['bag_of_words'] = words

df.drop(columns=[col for col in df.columns if col != 'bag_of_words'], inplace=True)

# instantiating and generating the count matrix
count = CountVectorizer()
count_matrix = count.fit_transform(df['bag_of_words'])

# creating a Series for the movie titles so they are associated to an ordered numerical
# list I will use later to match the indexes
indices = pd.Series(df.index)
c=count_matrix.todense()

# generating the cosine similarity matrix
cosine_sim = cosine_similarity(count_matrix, count_matrix)


# function that takes in movie title as input and returns the top 10 recommended movies
def recommendations(title, cosine_sim=cosine_sim):
    recommended_movies = []

    # gettin the index of the movie that matches the title
    idx = indices[indices == title].index[0]

    # creating a Series with the similarity scores in descending order
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending=False)

    # getting the indexes of the 10 most similar movies
    top_10_indexes = list(score_series.iloc[1:11].index)
    #print(top_10_indexes)

    # populating the list with the titles of the best 10 matching movies
    for i in top_10_indexes:
        recommended_movies.append(list(df.index)[i])

    return recommended_movies

