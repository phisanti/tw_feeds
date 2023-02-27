import time
import datetime
import spacy
from dotenv import dotenv_values
from app.tweepy_tools import config_tweepy_client, get_list_of_pages, tweets_from_pages, get_n_tweets
from app.tweet_analyser import tweet_to_df, tweet_analyser, read_boring_list, score_tweets, top_words, word_counter
from app.sender import make_msgid_list, send_newsletter_from_ram
from app.html_builder import build_email
from app.figure_maker import plot_wordcount, plot_word_correlation, plot_timechart
from spacytextblob.spacytextblob import SpacyTextBlob

#config = dotenv_values(".env")
#twlist, email, attachment_cid=run_tweet_report(config)
#list_to_words=top_words(word_counter(twlist['nouns']), 20)
#with open('test.html', 'w') as f:
#    f.write(email.render())
