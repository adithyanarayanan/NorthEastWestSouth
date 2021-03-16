# @author: Adithya Narayanan
# @task:  Renders the front end of the dash application which will display the final tweets

import warnings
warnings.simplefilter(action='ignore')

import dash
import dash_core_components as dcc

import plotly.express as px
import pandas as pd
import dash
import dash_html_components as html
import boto3
from botocore.exceptions import NoCredentialsError
import os

import io
import time
start = time.time()



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']   # Using stylesheet created by Dash Author
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server # Instantiating the app
print("Loading App")

template = "simple_white"


# CSS Styling parameters for Iframes that will render tweets as embedded tweet objects
iframe_style_text = {"width": "19%", 'display': 'inline-block', 'border': 0}
iframe_style_tweet = {"height": "550px", "width": "19%", 'display': 'inline-block', 'border': 0}
graph_style = {"width": "45%", 'display': 'inline-block', 'border': 0}


access_key_id = ""
secret_key = ""
region_name= ss""


# Retrieved data to render on app stores as "links.csv" on S3
session = boto3.Session(
                    aws_access_key_id= access_key_id,
                    aws_secret_access_key= secret_key,
                    region_name= region_name)

s3 = session.resource('s3')
news_bucket = s3.Bucket('adithya-aws-bucket')


# Processes the links.csv file from S3 and makes renderable objects
links = news_bucket.Object(key='links.csv')
response = links.get()
links_df = pd.read_csv(io.BytesIO(response['Body'].read()))
links_df.drop(columns=['Unnamed: 0'])

ner_counts = news_bucket.Object(key='ner_counts.csv')
response = ner_counts.get()
counts = pd.read_csv(io.BytesIO(response['Body'].read()))


# Pie Chart depicting trending named entities
fig1 = px.pie(counts, names=counts['Unnamed: 0'], values="freq", title="Trending Named Entities*",
              color_discrete_sequence=px.colors.qualitative.Plotly, opacity=0.5, template=template, labels={'Unnamed: 0': "Entity", 'freq': "Mentions"})



class_counts = news_bucket.Object(key='class_counts.csv')
response = class_counts.get()
c_counts = pd.read_csv(io.BytesIO(response['Body'].read()))



# Bar chart depicting class frequencies
fig2 = px.bar(c_counts, x=c_counts['Unnamed: 0'], y="category", color="category", title="News Category Snapshot*",
              color_continuous_scale=px.colors.sequential.Plotly3, orientation='v', labels={
        'Unnamed: 0' : "News Categories",
        "category" : "Frequency"
    }, opacity=0.85, template=template)



print("Received DataFrames")
print("Time to load in seconds:", time.time() - start)



# App Lqyout Code which renders the tweets and stats.
app.layout = html.Div(children=[
    html.H1(children='NorthEast x WestSouth', style={'color': 'gray'}),   # App title
    html.H3(children='What does the news look like today?', style={'color': 'gray'}),

    html.Div(children=[
    dcc.Graph(id='graph1', figure=fig1, style=graph_style),
    html.Div(style = {"width": "5%", 'display': 'inline-block'}),
    dcc.Graph(id='graph2', figure=fig2, style=graph_style)
    ]),


    html.H2(children='Politics, Governance, and Bureaucracy', style={'color': 'gray'}),

    # Div to display tweet stats
    html.Div(children=[
        html.Div(children="Subjectivity: " + str(links_df.loc[0]['subjectivity']) + " " + "| Polarity: " +
                          str(links_df.loc[0][
                                  'polarities']),
                 style=iframe_style_text),
        html.Div(children="Subjectivity: " + str(links_df.loc[1]['subjectivity']) + " " + "| Polarity: " +
                          str(links_df.loc[1][
                                  'polarities']),
                 style=iframe_style_text),
        html.Div(children="Subjectivity: " + str(links_df.loc[2]['subjectivity']) + " " + "| Polarity: " + str(
            links_df.loc[2][
                'polarities']),
                 style=iframe_style_text),
        html.Div(children="Subjectivity: " + str(links_df.loc[3]['subjectivity']) + " " + "| Polarity: " + str(
            links_df.loc[3][
                'polarities']),
                 style=iframe_style_text),
        html.Div(children="Subjectivity: " + str(links_df.loc[4]['subjectivity']) + " " + "| Polarity: " + str(
            links_df.loc[4][
                'polarities']),
                 style=iframe_style_text)
    ]),


    # Div to display tweets
    html.Div(children = [

    html.Iframe(srcDoc= links_df.loc[0]['html'],
                style=iframe_style_tweet),

    html.Iframe(srcDoc= links_df.loc[1]['html'],
                style=iframe_style_tweet),

    html.Iframe(srcDoc= links_df.loc[2]['html'],
                style=iframe_style_tweet),

    html.Iframe(srcDoc= links_df.loc[3]['html'],
                style=iframe_style_tweet),

    html.Iframe(srcDoc= links_df.loc[4]['html'],
                style=iframe_style_tweet)

    ]),


    html.H2(children='Business, Economics, and the Markets', style={'color': 'gray'}),


    #Another Div to display tweet stats
    html.Div(children=[
        html.Div(children = "Subjectivity: " + str(links_df.loc[5]['subjectivity']) + " " + "| Polarity: " +
                            str(links_df.loc[5][
            'polarities']),
        style =iframe_style_text),
        html.Div(children = "Subjectivity: " + str(links_df.loc[6]['subjectivity']) + " " +"| Polarity: " +
                            str(links_df.loc[6][
            'polarities']),
        style =iframe_style_text),
        html.Div(children="Subjectivity: " + str(links_df.loc[7]['subjectivity']) +" " + "| Polarity: " + str(
            links_df.loc[7][
            'polarities']),
                 style=iframe_style_text),
        html.Div(children="Subjectivity: " + str(links_df.loc[8]['subjectivity']) + " " +"| Polarity: " + str(
            links_df.loc[8][
            'polarities']),
                 style=iframe_style_text),
        html.Div(children="Subjectivity: " + str(links_df.loc[9]['subjectivity']) +" " + "| Polarity: " + str(
            links_df.loc[9][
            'polarities']),
                 style=iframe_style_text)
    ]),

    # Another div to display another line of tweets
    html.Div(children=[

        html.Iframe(srcDoc= links_df.loc[5]['html'],
                    style=iframe_style_tweet),

        html.Iframe(srcDoc= links_df.loc[6]['html'],
                    style=iframe_style_tweet),

        html.Iframe(srcDoc= links_df.loc[7]['html'],
                    style=iframe_style_tweet),

        html.Iframe(srcDoc= links_df.loc[8]['html'],
                    style=iframe_style_tweet),

        html.Iframe(srcDoc= links_df.loc[9]['html'],
                    style=iframe_style_tweet)

    ]),

    html.H2(children='Entertainment, Glitz, and Extravaganza', style={'color': 'gray'}),

    # Div to display tweet stats
    html.Div(children=[
        html.Div(children="Subjectivity: " + str(links_df.loc[10]['subjectivity']) + " " + "| Polarity: " +
                          str(links_df.loc[10][
                                  'polarities']),
                 style=iframe_style_text),
        html.Div(children="Subjectivity: " + str(links_df.loc[11]['subjectivity']) + " " + "| Polarity: " +
                          str(links_df.loc[11][
                                  'polarities']),
                 style=iframe_style_text),
        html.Div(children="Subjectivity: " + str(links_df.loc[12]['subjectivity']) + " " + "| Polarity: " + str(
            links_df.loc[12][
                'polarities']),
                 style=iframe_style_text),
        html.Div(children="Subjectivity: " + str(links_df.loc[13]['subjectivity']) + " " + "| Polarity: " + str(
            links_df.loc[13][
                'polarities']),
                 style=iframe_style_text),
        html.Div(children="Subjectivity: " + str(links_df.loc[14]['subjectivity']) + " " + "| Polarity: " + str(
            links_df.loc[14][
                'polarities']),
                 style=iframe_style_text)
    ]),


    # Div to display tweets
    html.Div(children = [

    html.Iframe(srcDoc= links_df.loc[10]['html'],
                style=iframe_style_tweet),

    html.Iframe(srcDoc= links_df.loc[11]['html'],
                style=iframe_style_tweet),

    html.Iframe(srcDoc= links_df.loc[12]['html'],
                style=iframe_style_tweet),

    html.Iframe(srcDoc= links_df.loc[13]['html'],
                style=iframe_style_tweet),

    html.Iframe(srcDoc= links_df.loc[14]['html'],
                style=iframe_style_tweet)

    ]),

html.H2(children='Pandemics, Welness, and Health', style={'color': 'gray'}),


    #Another Div to display tweet stats
    html.Div(children=[
        html.Div(children = "Subjectivity: " + str(links_df.loc[15]['subjectivity']) + " " + "| Polarity: " +
                            str(links_df.loc[15][
            'polarities']),
        style =iframe_style_text),
        html.Div(children = "Subjectivity: " + str(links_df.loc[16]['subjectivity']) + " " +"| Polarity: " +
                            str(links_df.loc[16][
            'polarities']),
        style =iframe_style_text),
        html.Div(children="Subjectivity: " + str(links_df.loc[17]['subjectivity']) +" " + "| Polarity: " + str(
            links_df.loc[17][
            'polarities']),
                 style=iframe_style_text),
        html.Div(children="Subjectivity: " + str(links_df.loc[18]['subjectivity']) + " " +"| Polarity: " + str(
            links_df.loc[18][
            'polarities']),
                 style=iframe_style_text),
        html.Div(children="Subjectivity: " + str(links_df.loc[19]['subjectivity']) +" " + "| Polarity: " + str(
            links_df.loc[19][
            'polarities']),
                 style=iframe_style_text)
    ]),

    # Another div to display another line of tweets
    html.Div(children=[

        html.Iframe(srcDoc= links_df.loc[15]['html'],
                    style=iframe_style_tweet),

        html.Iframe(srcDoc= links_df.loc[16]['html'],
                    style=iframe_style_tweet),

        html.Iframe(srcDoc= links_df.loc[17]['html'],
                    style=iframe_style_tweet),

        html.Iframe(srcDoc= links_df.loc[18]['html'],
                    style=iframe_style_tweet),

        html.Iframe(srcDoc= links_df.loc[19]['html'],
                    style=iframe_style_tweet)

    ])


])


# Runs the app serveer. If needed, set debug=True to trace call graph

if __name__ == '__main__':
    app.run_server()
