# @author: Adithya Narayanan
# @task:  Master Script that retrieves and processes tweets from news handles
# Retrieves, shortlists, classifies and finds embeddable links for the tweets that will be displayed


import time
start = time.time()
import os


import boto3
from botocore.exceptions import NoCredentialsError
import app_figures

import warnings
warnings.simplefilter(action='ignore')

import random
import spacy
nlp = spacy.load('en_core_web_sm')

from textblob import TextBlob


import time
import requests
import tweepy
from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRequestError, TwitterConnectionError
import pandas as pd
import pickle
import preprocessor as p



# Replace with own keys when using
consumer_key= ""
consumer_secret= ""
access_token_key= ""
access_token_secret= ""
bearer_token = ""



# TWeepy Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)

names = ["nytimes", "Reuters", "cnn", "BBCWorld", "AP", "Washingtonpost", "ChicagoTribune"]  # modify as per need




""" Retrieves the most recent 200 tweets from a  set of given screen names
    Returns a data frame of the tweets with [id, screen_name, text, timestamp]
"""
def get_new_tweets(names):
    print("Retrieving tweets")
    corpus = []                                                                                        # an array that will store all the tweets we need from the screen_name
    for name in names:
        tweets = api.user_timeline(name, include_rts=False, count=200, tweet_mode="extended")          # retrieves
        # up to 200 tweets from the given screen name
        # time.sleep(4)
        corpus.extend(tweets)                                                                          # add current retrieval of tweets to our corpus

    data = [[tweet.id_str, tweet.user.screen_name, tweet.full_text, tweet.favorite_count, tweet.retweet_count] for
            tweet in
            corpus]
    news = pd.DataFrame(data, columns=['tweet_id', 'screen_name', 'text', 'favorites', 'retweets'])    # df of tweets
    # news.drop_duplicates(subset=['text'])
    return news





""" Adds conversation_ids to the tweets retrieved from get_new_tweets
    Returns a data frame of the tweets with [id, screen_name, text, timestamp, conversation_id]
"""
def add_data(news):
    # print("Time Lapsed (s)", time.time() - start)
    # print("Retrieving additional data")
    ids = news.tweet_id
    conv_ids = []
    replies = []
    for id in ids:


        TWEET_ID = id
        TWEET_FIELDS = 'conversation_id,public_metrics'

        try:
            twapi = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret, api_version='2')
            r = twapi.request(f'tweets/:{TWEET_ID}', {'tweet.fields': TWEET_FIELDS})

            for item in r:
                conv_ids.append(item['conversation_id'])
                replies.append(item['public_metrics']['reply_count'])


        except TwitterRequestError as e:
            print(e.status_code)
            for msg in iter(e):
                print(msg)


        except TwitterConnectionError as e:
            print(e)

        except Exception as e:
            print(e)
    news['replies'] = replies
    news['conversation_id'] = conv_ids
    return news



"""
Retrieves embeddable HTML code for every tweet
The HTML code will be rendered in the Dash App rendered by app.py
Randomly allocates dark/light choice of embed theme
"""
def get_oembed_link(string):
    theme = ['light', 'dark']
    json_embed = requests.get('https://publish.twitter.com/oembed?url=' + string + "&theme="+random.choice(theme))
    return json_embed.json()['html']




"""
Applies get_oembed_link to every element of the data_frame news
"""
def get_embeds(news):
    print("Retrieving Embeddable HTML for Tweets")
    news['url'] = "https://twitter.com/" + news.screen_name + '/status/' + news.tweet_id
    news['html'] = news.url.apply(get_oembed_link)
    return news



"""
Convert model predictions from numerical value to a text label
"""
def return_label(key):
    labels = {0: "health", 1: "business", 2: "politics", 3: "sports", 4: "entertainment"}  # Use with large_data.csv
    return labels[key]



"""
Cleans the text of news tweets
"""
def clean_tweets(news):
    news.text = news.text.str.lower()
    news.text = news.text.apply(p.clean)
    return news

"""
Checks if the ensemble of models predict the same category of news for a tweets
"""
def sure_shots(news):
    if news.y_svc == news.y_mnb == news.y_log:
        return 1
    else:
        return 0



"""
Returns the overall polarity score of a string using spacy textblob
"""
def blob_subjectivity(str):
    wiki = TextBlob(str)
    return wiki.sentiment.subjectivity



"""
Predicts the category that each news tweet belongs to
"""

def categorize_tweets(news):
    logit = pickle.load(open('models/logit_model.pkl', 'rb'))
    mnb = pickle.load(open('models/mnb_model.pkl', 'rb'))
    svc = pickle.load(open('models/svc_model.pkl', 'rb'))

    # news = clean_tweets(news)
    news.drop_duplicates(subset=['text'], inplace=True)

    y_svc = svc.predict(news.text)
    y_mnb = mnb.predict(news.text)
    y_log = logit.predict(news.text)

    y_svc = list(map(return_label, y_svc))
    y_mnb = list(map(return_label, y_mnb))
    y_log = list(map(return_label, y_log))

    news['y_svc'] = y_svc  # SVC Predictions
    news['y_mnb'] = y_mnb  # MNB Predictions
    news['y_log'] = y_log  # LOG Predictions

    news['y'] = news.apply(sure_shots, axis=1)  # Final Predictions (if all three above match)

    news = news[news.y == 1] # Mismatched predictions discarded
    news['category'] = news.y_svc
    news['subjectivity'] = news.text.apply(blob_subjectivity)

    news['engagement'] = news.favorites + news.retweets
    news.drop(['favorites', 'retweets'], axis=1, inplace=True)

    news.drop(['y_svc', 'y_mnb' ,'y_log'], axis=1, inplace=True)

    return news


"""
In a given dataframe, returns the best five tweets by engagement
"""
def best_five(df):
    final = df.sort_values(by='engagement', ascending=False).head()
    return final


"""
Retrieves the best five news tweets for every category
"""
def get_best_news(news):
    politics = best_five(news[news.category == 'politics'])
    sports = best_five(news[news.category == 'sports'])
    entertainment = best_five(news[news.category == 'entertainment'])
    health = best_five(news[news.category == 'health'])
    business = best_five(news[news.category == 'business'])

    news = pd.concat([politics, sports, entertainment, health, business], ignore_index=True)
    return news


"""
Modifies the structure of news dataframe to help retrieve_replies efficiently
"""
def embellish(news):
    news['retrieved'] = False
    news['polarity'] = "*"
    news.loc[news.replies >= 800 , 'polarity'] = "X"
    return news


"""
Uploads the necessary files to AWS S3 for app.py to read from
"""
def upload_to_s3(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id="AKIAJ37JNUI5G2R62E4Q",
                      aws_secret_access_key= "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")

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful", local_file)
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False





"""
Function that chains the other functions from above in order of usage
Takes a list of twitter screen names of news handles, returns a dataframe with most recent tweets and their predicted
categories
"""

def tweets(names):
    news = get_new_tweets(names)

    print("Categorizing Tweets")
    news = categorize_tweets(news)

    # Retrieving graphable data
    class_plot_counts = app_figures.class_plot_counts(news)
    ner_counts = app_figures.ner_plot_counts(news)

    class_plot_counts.to_csv("class_counts.csv")
    ner_counts.to_csv("ner_counts.csv")

    print("Uploading graphable data to S3")

    upload_to_s3("class_counts.csv", "adithya-aws-bucket", "class_counts.csv")
    upload_to_s3("ner_counts.csv", "adithya-aws-bucket", "ner_counts.csv")

    os.remove("ner_counts.csv")
    os.remove("class_counts.csv")

    print("Getting Best News")

    news = get_best_news(news)
    print("Finding Conversation Threads")
    news = add_data(news)
    print("Finding tweet embed links")
    news = get_embeds(news)
    news = embellish(news)

    politics = news[news.category == 'politics']
    sports = news[news.category == 'sports']
    entertainment = news[news.category == 'entertainment']
    health = news[news.category == 'health']
    business = news[news.category == 'business']

    print("Uploading category files to AWS S3 bucket adithya-aws-bucket")

    politics.to_csv("politics.csv")
    upload_to_s3("politics.csv", "adithya-aws-bucket", "politics.csv")
    os.remove("politics.csv")


    sports.to_csv("sports.csv")
    upload_to_s3("sports.csv", "adithya-aws-bucket", "sports.csv")
    os.remove("sports.csv")

    entertainment.to_csv("entertainment.csv")
    upload_to_s3("entertainment.csv", "adithya-aws-bucket", "entertainment.csv")
    os.remove("entertainment.csv")


    health.to_csv("health.csv")
    upload_to_s3("health.csv", "adithya-aws-bucket", "health.csv")
    os.remove("health.csv")

    business.to_csv("business.csv")
    upload_to_s3("business.csv", "adithya-aws-bucket", "business.csv")
    os.remove("business.csv")


    return news


def main():
    news = tweets(names)
    news.to_csv("news.csv")
    upload_to_s3("news.csv", "adithya-aws-bucket", "news.csv")
    os.remove("news.csv")
    print("Latest files uploaded to AWS S3 at", time.time())
    print('Execution time in seconds: ', time.time() - start)
    print("Ciao")


if __name__ == '__main__':
    main()
