# @author: Adithya Narayanan
# @task:  Computer data for the figures that have to be displayed in the rendered app.


import pandas as pd
import numpy as np
import plotly.express as px
import spacy
from string_grouper import match_strings, match_most_similar, group_similar_strings, StringGrouper
import preprocessor as p

import warnings
warnings.simplefilter(action='ignore')

nlp = spacy.load('en_core_web_sm')



"""
Returns Named Entities from a string using Spacy
"""
def named_entity_tokens(string):
    entities = []
    doc = nlp(string)
    for ent in doc.ents:
        if ent.label_ == "MONEY":
            continue


        entities.append(str(ent))
        return entities


"""
Function that builds NER Corpus from the tweets dataframe
Returns a single long list of named entities
"""
def build_ner_corpus(tweets):
    ner_corpus = []
    tweets['entities'] = tweets.text.apply(named_entity_tokens)
    for entity_list in tweets.entities:
        # print(entity_list)
        if entity_list != None:
            ner_corpus.extend(entity_list)
    return ner_corpus


"""
Creates a bar chart that depicts frequency of class values
"""
def class_plot_counts(df):
    counts = pd.DataFrame(df.category.value_counts())
    # bar = px.bar(counts, x=counts.index, y="category", color="category", title="News Category Dominance")
    return counts


"""
Creates a Named Entity Frequency plot out of all named entities from the tweet texts
"""
def ner_plot_counts(df):
    df.text = df.text.str.lower()
    df.text = df.text.apply(p.clean)

    net_entities_list = build_ner_corpus(df)  # Full long list of entities
    net_entities_list = pd.Series(net_entities_list)
    net_entities_list = net_entities_list.str.replace("'s", "")
    net_entities_list = net_entities_list.str.replace(".", "")
    similarized_entities_list = group_similar_strings(net_entities_list)  # Grouping similar entities together
    counts = pd.DataFrame(similarized_entities_list.value_counts(), columns = ['freq'])
    counts = counts.head(10)

    #ner = px.pie(counts, names=counts.index, values="freq", title="Named Entity Frequency")
    return counts
