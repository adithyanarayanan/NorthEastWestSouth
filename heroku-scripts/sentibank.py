# @author: Adithya Narayanan
# @task:  Cleans tweets and performs sentiment/subjectivity analysis on them

import preprocessor as p
import pandas as pd
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import spacy
from textblob import TextBlob

STOPWORDS = set(stopwords.words('english'))
sia = SentimentIntensityAnalyzer() # Initializing VADER Sentiment Intensity Analyzer

nlp = spacy.load('en_core_web_sm')



"""
Given an input string, this function returns a cleaner string devoid of handles, links, hashtags, emojis
"""
def clean_tweet(str):
    return p.clean(str)


"""
Given a tweet text, this removes stopwords from a column that contains tweets (pre-decided)
Code Reference: https://towardsdatascience.com/text-preprocessing-for-data-scientist-3d2419c8199d
"""
def stopwords(text):
    return " ".join([word for word in str(text).split() if word not in STOPWORDS])


"""
Returns the compound sentiment intensity score of a string using Vader (NLTK)
"""
def vader_sentiment(str):
    return sia.polarity_scores(str)['compound']


"""
Returns the overall polarity score of a string using spacy textblob
"""
def blob_polarity(str):
    wiki = TextBlob(str)
    return wiki.sentiment.polarity


"""
Returns the overall polarity score of a string using spacy textblob
"""
def blob_subjectivity(str):
    return nlp(str)._.sentiment.subjectivity


"""
Rounds polarity values for better calculability
"""
def polarize(polarity):
    if polarity > 0:
        return 1
    if polarity < 0:
        return -1
    if polarity == 0:
        return 0

"""
Returns the polarity of a text tweet if both vader and blob polarities match
"""
def sure_shots(df):
    if df.blob_polarity == df.vader_polarity:
        return df.blob_polarity
    else:
        return 0

"""
Given an input dataframe with a column of tweets (pre-decided), this applies the clean_tweet, stopwords,
and polarity and subjectivity assesor functions to the column to return a dataframe with complete statistics about
the tweets
"""
def get_data_stats(df):
    df['tweet_text_clean'] = df['tweet_text'].apply(clean_tweet)

    df['vader_polarity'] = df['tweet_text_clean'].apply(vader_sentiment)
    df['blob_polarity'] = df['tweet_text_clean'].apply(blob_polarity)

    df.blob_polarity = df.blob_polarity.apply(polarize)
    df.vader_polarity = df.vader_polarity.apply(polarize)

    df['polarity'] = df.apply(sure_shots, axis=1)



    vals = df.polarity.value_counts()
    return vals[1] - vals[-1]
