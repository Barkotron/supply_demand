#!/usr/bin/env python
# coding: utf-8

# In[1]:
import nltk
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
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


target_sub_string = 'toronto'
target_sub = reddit.subreddit(target_sub_string)
n_posts = 10000


# Get `limit` most recent comments from each subreddit
# 
# Comments what were deleted for removed with have `NoneType` so we filter those out before asking for the author name.

# In[4]:


def get_flattened_comment_tree(subreddit, limit):
    
    print(f"Reading from {subreddit}")
    return subreddit.comments(limit=limit)
    

def check_for_keywords(comment,collocs):
    stop_words = set(stopwords.words("english"))

    lemmatizer = nltk.WordNetLemmatizer()

    comment_string = comment.body

    if comment_string:
        all_tokens = []

        #tokenize by sentence
        sent_tokens = nltk.sent_tokenize(comment_string)

        #tokenize each sentence by word
        for sentence in sent_tokens:
            word_tokens = nltk.word_tokenize(sentence)
            all_tokens = all_tokens + word_tokens


        #remove 'stop words' and punctuation (is, the, that, I...)
        filtered_list = []
        for word in all_tokens:
            if word.casefold() not in stop_words and word.casefold().isalpha():
                filtered_list.append(word.lower())


        #tokens = nltk.pos_tag(filtered_list)
        lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_list]
        #lemma_text = nltk.Text(comment_string)

        
        bigram_collocation = BigramCollocationFinder.from_words(lemmatized_words)
        n_best = bigram_collocation.nbest(BigramAssocMeasures.raw_freq, 15)
        
        sia = SentimentIntensityAnalyzer()


        if set(collocs).intersection(set(n_best)):
        #if True:
            print(f"-------------\nCOMMENT:\n{comment_string}")
            print(f"lemmatized words:\n{lemmatized_words}")
            print(f"collocations:\n{n_best}")
            print(sia.polarity_scores(comment_string))

    


def leave_comment(comment,image_path):
    pass

def test(comment,collocs):
    check_for_keywords(comment,collocs)

def check_subreddit(subreddit,keywords,image_path):
    # for each comment:
    # check keywords
    # leave comment
    
    comments = get_flattened_comment_tree(target_sub,n_posts)
    for comment in comments:
        check_for_keywords(comment,keywords)


test_comment_string = """I'm looking at buying a place but condo prices are so bad.
where do i find a condo for a good price"""

test_comment = reddit.comment(test_comment_string)
test_comment.body = test_comment_string

#print(test_comment.body)

collocs = [("condo","price"),("price","condo"),("house","price"),("price","house"),("home","price"),("price","home"),
("affordable","housing"), ("housing","affordable")]

check_subreddit(target_sub,collocs,"hello")
#test(test_comment,collocs)
