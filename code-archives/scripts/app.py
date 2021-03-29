# @author: Adithya Narayanan
# @task:  Renders the front end of the dash application which will display the final tweets
# Some code referenced from Dash Open Source Example
# Output Displayed at http://127.0.0.1:8050/


import dash
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
import dash
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']   # Using stylesheet created by Dash Author

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)    # Instantiating the app



# Sample HTML code
# Each of the strings below contain HTML Code to embed a tweet in the app
# They will be passed as parameters to html.IFrame components to render on a web page
str1 = '<blockquote class="twitter-tweet"><p lang="en" dir="ltr">President Biden said on Friday that he planned to declare a major disaster in Texas which would allow for additional federal aid to be routed to residents struggling to access basic necessities after a deadly winter storm. <a href="https://t.co/rPcfIcO0c3">https://t.co/rPcfIcO0c3</a> <a href="https://t.co/qB12ryoEcq">pic.twitter.com/qB12ryoEcq</a></p>&mdash; The New York Times (@nytimes) <a href="https://twitter.com/nytimes/status/1362940072899837952?ref_src=twsrc%5Etfw">February 20, 2021</a></blockquote><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'
str2 = '<blockquote class="twitter-tweet" data-theme="dark"><p lang="en" dir="ltr">Families in Texas are taking desperate steps to stay warm as they face a power grid shutdown during one of the coldest weeks in a generation <a href="https://t.co/u0ZoWCX3Ji">https://t.co/u0ZoWCX3Ji</a></p>&mdash; The Wall Street Journal (@WSJ) <a href="https://twitter.com/WSJ/status/1362178780022857728?ref_src=twsrc%5Etfw">February 17, 2021</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'
str3 = '<blockquote class="twitter-tweet" data-theme="dark"><p lang="en" dir="ltr">UPDATE: Sen. Cruz says his decision to go on a family vacation to Cancún, Mexico as Texans suffered without heat, water and power because of a historic winter storm, was &quot;a mistake&quot; that he now regrets. <a href="https://t.co/21DstBDmY9">https://t.co/21DstBDmY9</a></p>&mdash; NBC News (@NBCNews) <a href="https://twitter.com/NBCNews/status/1362575160067391492?ref_src=twsrc%5Etfw">February 19, 2021</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'
str4 = '<blockquote class="twitter-tweet" data-theme="light"><p lang="en" dir="ltr">Watch: After his superb win against Tsitsipas, Medvedev says pressure on Djokovic in Aus Open final <a href="https://t.co/nmhThooZHx">https://t.co/nmhThooZHx</a> <br><br>Medvedev, now into his second Grand Slam decider on the back of a 20-match winning streak, said the world No 1 has more experience but also more to lose.</p>&mdash; scroll.in (@scroll_in) <a href="https://twitter.com/scroll_in/status/1362826784836829186?ref_src=twsrc%5Etfw">February 19, 2021</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'
str5 = '<blockquote class="twitter-tweet" data-theme="dark"><p lang="en" dir="ltr">Blueprint for a raid: Documents shed light on plan to buy U.S. helicopter gunships for assault on Tripoli <a href="https://t.co/WpIJcZjAQF">https://t.co/WpIJcZjAQF</a></p>&mdash; The Washington Post (@washingtonpost) <a href="https://twitter.com/washingtonpost/status/1362962863040659456?ref_src=twsrc%5Etfw">February 20, 2021</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'


# CSS Styling parameters for Iframes that will render tweets as embedded tweet objects
iframe_style_text = {"width": "19%", 'display': 'inline-block', 'border': 0}
iframe_style_tweet = {"height": "550px", "width": "19%", 'display': 'inline-block', 'border': 0}


# Some data to plot the sample figure - from basic dash example
# Also used to set the style of the HTML Divs that display the stats related to each tweet
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group", title="Sample Figure- to be replaced with "
                                                                             "Topic Model (or similar)")

app.layout = html.Div(children=[
    html.H1(children='NorthEast SW'),   # App title

    html.Div(children='''Top news from Twitter, served on a platter'''),  # App Description

    dcc.Graph(id='example-graph', figure=fig),          # Sample Figure To Be Replaced

    html.H1(children='News Category Headline Here'),

    # Div to display tweet stats
    html.Div(children=[
        html.Div(children = "Subjectivity: x.xx    | |   Polarity = x.xx", style =iframe_style_text),
        html.Div(children = "Subjectivity: x.xx    | |   Polarity = x.xx", style =iframe_style_text),
        html.Div(children = "Subjectivity: x.xx    | |   Polarity = x.xx", style =iframe_style_text),
        html.Div(children = "Subjectivity: x.xx    | |   Polarity = x.xx", style =iframe_style_text),
        html.Div(children = "Subjectivity: x.xx    | |   Polarity = x.xx", style =iframe_style_text)
    ]),


    # Div to display tweets
    html.Div(children = [

    html.Iframe(srcDoc=str1,
                style=iframe_style_tweet),

    html.Iframe(srcDoc=str2,
                style=iframe_style_tweet),

    html.Iframe(srcDoc=str3,
                style=iframe_style_tweet),

    html.Iframe(srcDoc=str4,
                style=iframe_style_tweet),

    html.Iframe(srcDoc=str5,
                style=iframe_style_tweet)

    ]),


    html.H1(children='News Category Headline Here'),


    #Another Div to display tweet stats
    html.Div(children=[
        html.Div(children = "Subjectivity: x.xx    | |   Polarity = x.xx", style =iframe_style_text),
        html.Div(children = "Subjectivity: x.xx    | |   Polarity = x.xx", style =iframe_style_text),
        html.Div(children = "Subjectivity: x.xx    | |   Polarity = x.xx", style =iframe_style_text),
        html.Div(children = "Subjectivity: x.xx    | |   Polarity = x.xx", style =iframe_style_text),
        html.Div(children = "Subjectivity: x.xx    | |   Polarity = x.xx", style =iframe_style_text)
    ]),

    # Another div to display another line of tweets
    html.Div(children=[

        html.Iframe(srcDoc=str1,
                    style=iframe_style_tweet),

        html.Iframe(srcDoc=str2,
                    style=iframe_style_tweet),

        html.Iframe(srcDoc=str3,
                    style=iframe_style_tweet),

        html.Iframe(srcDoc=str4,
                    style=iframe_style_tweet),

        html.Iframe(srcDoc=str5,
                    style=iframe_style_tweet)

    ])

])

if __name__ == '__main__':
    app.run_server(debug=True)