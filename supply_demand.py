#!/usr/bin/env python
# coding: utf-8

# In[1]:
import nltk
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import re
import praw
import networkx as nx
import numpy as np
import itertools
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv


# In[2]:
#nltk.download()
load_dotenv()
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_SECRET = os.getenv('REDDIT_SECRET')
REDDIT_USER = os.getenv('REDDIT_USER')
REDDIT_PASS = os.getenv('REDDIT_PASS')

reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                     client_secret=REDDIT_SECRET,
                     user_agent="A bot - Reminds people of Supply Vs. Demand",
                     username=REDDIT_USER,
                     password=REDDIT_PASS)


# In[3]:


target_sub_string = 'winnipeg'
target_sub = reddit.subreddit(target_sub_string)
n_posts = 10


# Get `limit` most recent comments from each subreddit
# 
# Comments what were deleted for removed with have `NoneType` so we filter those out before asking for the author name.

# In[4]:


def get_flattened_comment_tree(subreddit, limit):
    
    print(f"Reading from {subreddit}")
    return subreddit.comments(limit=limit)
    

def check_for_keywords(comment,keywords):
    stop_words = set(stopwords.words("english"))

    lemmatizer = nltk.WordNetLemmatizer()

    comment_string = comment.body
    tokens = nltk.word_tokenize(comment_string)

    filtered_list = []

    for word in tokens:
        if word.casefold() not in stop_words:
            filtered_list.append(word)

    lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_list]
    
    sia = SentimentIntensityAnalyzer()
    print(f"COMMENT:\n{comment_string}")
    print(sia.polarity_scores(comment_string))
    
    #print(lemmatized_words)


def leave_comment(comment,image_path):
    pass

def check_subreddit(subreddit,keywords,image_path):
    # for each comment:
    # check keywords
    # leave comment
    
    comments = get_flattened_comment_tree(target_sub,n_posts)
    for comment in comments:
        check_for_keywords(comment,keywords)

keywords = ["condos","condo","home","price","prices"]

check_subreddit(target_sub,keywords,"hello")
