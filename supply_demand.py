
import nltk
import argparse
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
import praw
import itertools
import os
from dotenv import load_dotenv


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

    

def get_flattened_comment_tree(subreddit, limit):
    
    print(f"Reading from {subreddit}")
    return subreddit.comments(limit=limit)
    

def check_for_collocations(comment,collocs):
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

        lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_list]

        #get most frequent collocations
        bigram_collocation = BigramCollocationFinder.from_words(lemmatized_words)
        n_best = bigram_collocation.nbest(BigramAssocMeasures.raw_freq, 15)

        
        return bool(collocs.intersection(set(n_best)))
    

def check_already_posted(comment):
    
    #replies seem to be empty without this
    comment.refresh()

    #check that we haven't spammed this comment thread already
    submission = comment.submission
    top_level_comments = submission.comments
    replies = comment.replies

    #check replies to THIS comment
    for reply in replies:
        print(reply.author)
        if reply.author == REDDIT_USER:
            print(f"already commented on:\n{comment.body}")
            return True

    #check top level comments of the whole submission
    for reply in top_level_comments:
        print(reply.author)
        if reply.author == REDDIT_USER:
            print(f"already commented on:\n{comment.body}")
            return True
    
    return False

def post_comment(comment,link):
    print(f"commented on:\n{comment.body}")
    comment.reply(f"This may help: {link}")


def check_subreddit(subreddit,keywords,n_posts,link):
    # for each comment:
    # check keywords
    # check that it hasn't already commented here
    # if not: leave comment
    
    comments = get_flattened_comment_tree(subreddit,n_posts)
    for comment in comments:
        if check_for_collocations(comment,keywords):
            if not check_already_posted(comment):
                post_comment(comment,link)


def arguments():
    
    arg_parser  = argparse.ArgumentParser(description="Educational trolling tool for reddit.")

    arg_parser.add_argument(
        "subreddit",
        type=str,
        help="the subreddit to look through"
    )

    arg_parser.add_argument(
        "-l",
        "--link",
        type=str,
        default="https://en.wikipedia.org/wiki/Supply_and_demand",
        help="educational link about supply and demand"
    )

    arg_parser.add_argument(
        "-n",
        "--n_posts",
        default=1000,
        type=int,
        help="the number of posts to check"
    )


    return arg_parser.parse_args()

def main():

    args = arguments()
  
    dwellings = ["house", "condo", "airbnb","home","apartment"]
    pricing = ["cheap", "luxury", "affordable", "expensive","price","pricing","pricey"]

    # to cover sentences like 'affordable housing' as well as 'houses that are affordable'
    collocs = set( list(itertools.product(dwellings, pricing)) + list(itertools.product(pricing,dwellings)) )

    check_subreddit(reddit.subreddit(args.subreddit),collocs,args.n_posts,args.link)

if __name__ == "__main__":
    main()
