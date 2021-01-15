# @author: Adithya Narayanan
# @task:  Retrieves tweets from news orgs. handles from a list of screen names
# Code used heavily from TwitterAPI Examples: https://github.com/geduldig/TwitterAPI
# see sample_output/news.csv for sample output

import pandas as pd
import time
import tweepy
from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRequestError, TwitterConnectionError


consumer_key= "MFg6zCjk0ieHKB9q5oxKkOT2D"
consumer_secret= "hTIdnRbNs1J6biailaVIogTvhIS8OYm4eLv4PHSOGrSX2RUbeo"
access_token_key= "2515973623-3XU4n5BkGyyoCAIyicvj08trw5jb82nDCEUmr8E"
access_token_secret= "2hFyxjowGDZwiF3XzAVaOzSnylfAU5MnTj9PF8jGxBtyT"

# TWeepy Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)

names = ["nytimes", "Reuters"]  # placeholder names


""" Retrieves the most recent 200 tweets from a  set of given screen names
    Returns a data frame of the tweets with [id, screen_name, text, timestamp]
"""
def get_new_tweets(names):
    print("Retrieving tweets")
    corpus = []                                                                                        # an array that will store all the tweets we need from the screen_name
    for name in names:
        tweets = api.user_timeline(name, include_rts=False, count=200, tweet_mode="extended")          # retrieves up to 200 tweets from the given screen name
        time.sleep(4)
        corpus.extend(tweets)                                                                          # add current retrieval of tweets to our corpus

    data = [[tweet.id_str, tweet.user.screen_name, tweet.full_text, tweet.created_at] for tweet in corpus]
    news = pd.DataFrame(data, columns=['tweet_id', 'screen_name', 'text', 'timestamp'])                # creates a dataframe with the retrieved tweets

    return news





""" Adds conversation_ids to the tweets retrieved from get_new_tweets
    Returns a data frame of the tweets with [id, screen_name, text, timestamp, conversation_id]
"""
def add_data(news):
    print("Retrieving additional data")
    ids = news.tweet_id
    conv_ids = []
    for id in ids:

        TWEET_ID = id
        TWEET_FIELDS = 'conversation_id'

        try:
            twapi = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret, api_version='2')
            r = twapi.request(f'tweets/:{TWEET_ID}', {'tweet.fields': TWEET_FIELDS})

            for item in r:
                conv_ids.append(item['conversation_id'])


        except TwitterRequestError as e:
            print(e.status_code)
            for msg in iter(e):
                print(msg)

        except TwitterConnectionError as e:
            print(e)

        except Exception as e:
            print(e)

    news['conversation_id'] = conv_ids
    return news

### Testing Method Definitions
news = get_new_tweets(names)
news = add_data(news)

print("Final DataFrame")
print(news.head())

# UNCOMMENT TO WRITE TO DESIRED FILE NAME
# news.to_csv("news.csv")
