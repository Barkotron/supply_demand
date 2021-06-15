#!/usr/bin/env python
# coding: utf-8

# In[1]:


import praw
import networkx as nx
import numpy as np
import itertools
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv


# In[2]:
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
    comments = subreddit.comments(limit=limit)
    

def check_for_keywords(comment,keywords):
    pass

def leave_comment(comment,image_path):
    pass

def check_subreddit(subreddit,keywords,image_path):
    # for each comment:
    # check keywords
    # leave comment
    pass


print(get_flattened_comment_tree(target_sub,n_posts))
