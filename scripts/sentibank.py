# @author: Adithya Narayanan
# @task:  Cleans tweets and performs sentiment/subjectivity  analysis on them from
# Sample Output: 'sample_outputs/senti-data.csv'

import preprocessor as p
import pandas as pd
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

STOPWORDS = set(stopwords.words('english'))
sia = SentimentIntensityAnalyzer() # Initializing VADER Sentiment Intensity Analyzer

nlp = spacy.load('en_core_web_sm')
blob = SpacyTextBlob()
nlp.add_pipe(blob)


sample = pd.read_csv("replies.csv")
str1 = "@Adithya is testing if this string is a good enough input string :) :P :D " \
       "https://pypi.org/project/tweet-preprocessor/"  # sample testing input string

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
    return nlp(str)._.sentiment.polarity


"""
Returns the overall polarity score of a string using spacy textblob
"""
def blob_subjectivity(str):
    return nlp(str)._.sentiment.subjectivity



"""
Given an input dataframe with a column of tweets (pre-decided), this applies the clean_tweet, stopwords, 
and polarity and subjectivity assesor functions to the column to return a dataframe with complete statistics about 
the tweets
"""
def get_data_stats(df):
    # df['tweet_text_clean'] = df['tweet_text'].apply(stopwords)
    df['tweet_text_clean'] = df['tweet_text'].apply(clean_tweet)
    df['subjectivity'] = df['tweet_text_clean'].apply(blob_subjectivity)
    df['vader_polarity'] = df['tweet_text_clean'].apply(vader_sentiment)
    df['blob_polarity'] = df['tweet_text_clean'].apply(blob_polarity)
    df.to_csv('senti_data.csv')
    return df



# MAIN METHOD TEMP SUBSTITUTE
get_data_stats(pd.read_csv('replies.csv'))

