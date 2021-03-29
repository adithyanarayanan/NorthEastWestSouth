# @author: Adithya Narayanan
# @task:  Retrieves five individual files (for each of the categories from S3) +
# Makes a csf file with just the final statistics and embeddable html code to be dislpayed from these files (which recieve it from category_replies.py files)
# Final stats to be displayed: Subjectivity and Polarity.


import pandas as pd
import boto3
import os
import warnings
warnings.simplefilter(action='ignore')
from botocore.exceptions import NoCredentialsError



"""
Makes individual parseable files for each of the categories of news we display.
There is a way to do this without recreating the files locally, but it doesn't add much value at this moment
in terms of efficiency.
"""
def make_files():
    print("Retrieving File from S3")

    access_key_id = ""
    secret_key = ""
    region_name=""

    session = boto3.Session(
                        aws_access_key_id= access_key_id,
                        aws_secret_access_key= secret_key,
                        region_name= region_name)

    s3 = session.resource('s3')
    news_bucket = s3.Bucket('adithya-aws-bucket')

    ################################################################################
    politics_file = news_bucket.Object(key='politics.csv')
    response = politics_file.get()

    lines = response['Body'].read()
    with open('politics.csv', 'wb') as file:
        file.write(lines)

    politics = pd.read_csv("politics.csv")
    os.remove("politics.csv")
    ################################################################################
    entertainment = news_bucket.Object(key='entertainment.csv')
    response = entertainment.get()

    lines = response['Body'].read()
    with open('entertainment.csv', 'wb') as file:
        file.write(lines)

    entertainment = pd.read_csv("entertainment.csv")
    os.remove("entertainment.csv")
    #################################################################################

    business = news_bucket.Object(key='business.csv')
    response = business.get()

    lines = response['Body'].read()
    with open('business.csv', 'wb') as file:
        file.write(lines)

    business = pd.read_csv("business.csv")
    os.remove("business.csv")
    #################################################################################

    health = news_bucket.Object(key='health.csv')
    response = health.get()

    lines = response['Body'].read()
    with open('health.csv', 'wb') as file:
        file.write(lines)

    health = pd.read_csv("health.csv")
    os.remove("health.csv")
    #################################################################################

    sports = news_bucket.Object(key='sports.csv')
    response = sports.get()

    lines = response['Body'].read()
    with open('sports.csv', 'wb') as file:
        file.write(lines)

    sports = pd.read_csv("sports.csv")
    os.remove("sports.csv")
    #################################################################################
    news_large = news_bucket.Object(key='news_large.csv')
    response = news_large.get()

    lines = response['Body'].read()
    with open('news_large.csv', 'wb') as file:
        file.write(lines)

    news_large = pd.read_csv("news_large.csv")
    os.remove("news_large.csv")
    #################################################################################


    return politics, health, entertainment, sports, entertainment, business


"""
Uploads files to S3- used several times through the project
"""

def upload_to_s3(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id="",
                      aws_secret_access_key= "")

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
Retrieves the files for each individual category.
"""
politics, health, entertainment, sports, entertainment, business = make_files()

htmls = []
polarities = []
subjectivity = []

for index, row in politics.iterrows():
    htmls.append(row['html'])
    polarities.append(row['polarity'])
    subjectivity.append(row['subjectivity'])


for index, row in business.iterrows():
    htmls.append(row['html'])
    polarities.append(row['polarity'])
    subjectivity.append(row['subjectivity'])


for index, row in entertainment.iterrows():
    htmls.append(row['html'])
    polarities.append(row['polarity'])
    subjectivity.append(row['subjectivity'])

for index, row in health.iterrows():
    htmls.append(row['html'])
    polarities.append(row['polarity'])
    subjectivity.append(row['subjectivity'])

for index, row in sports.iterrows():
    htmls.append(row['html'])
    polarities.append(row['polarity'])
    subjectivity.append(row['subjectivity'])




links = pd.DataFrame()
links['html'] = htmls
links['polarities'] = polarities
links['subjectivity'] = subjectivity

links.to_csv("links.csv")
upload_to_s3("links.csv", "adithya-aws-bucket", "links.csv")
os.remove("links.csv")
