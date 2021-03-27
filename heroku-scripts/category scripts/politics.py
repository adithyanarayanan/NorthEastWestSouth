# @author: Adithya Narayanan
# @task:  Master File which controls all replies extracted from shortlisted politics tweets. Find statistics on this auxiliary data
# and uploads a csv files to S3

import politics_replies
import pandas as pd
import sentibank

import boto3
from botocore.exceptions import NoCredentialsError
import os


print("Politics: Retrieving File from S3")

access_key_id = ""
secret_key = ""
region_name=''

session = boto3.Session(
                    aws_access_key_id= access_key_id,
                    aws_secret_access_key= secret_key,
                    region_name= region_name)

s3 = session.resource('s3')
news_bucket = s3.Bucket('adithya-aws-bucket')

news_file = news_bucket.Object(key='politics.csv')
response = news_file.get()

lines = response['Body'].read()
with open('politics.csv', 'wb') as file:
    file.write(lines)


df = pd.read_csv("politics.csv")
df = df.drop(columns=['Unnamed: 0'])


for index, row in df.iterrows():
    # print(row)
    if row['polarity'] == 'X':
        df.loc[index, 'retrieved'] = True
        # print("skipping")
        continue

    if row['retrieved'] == False:
        conv_ids = [row['conversation_id']]
        replies = politics_replies.reply_thread_maker(conv_ids)
        polarity = sentibank.get_data_stats(replies)
        df.loc[index, 'polarity'] = round(polarity, 2)
        df.loc[index, 'retrieved'] = True
        break


"""
Uploads the necessary files to AWS S3 for app.py to read from
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
Creates the final file and uploads it to AWS S3, removes local copy to handle write conflicts
"""
df.to_csv("politics.csv")
upload_to_s3("politics.csv", "adithya-aws-bucket", "politics.csv")
os.remove("politics.csv")
