import time
import datetime
import spacy
from dotenv import dotenv_values
from app.tweet_reporter import grep_dict
from app.tweepy_tools import config_tweepy_client, get_list_of_pages, tweets_from_pages, get_n_tweets
from app.tweet_analyser import tweet_to_df, tweet_analyser, read_boring_list, score_tweets, top_words, word_counter
from app.sender import make_msgid_list, send_newsletter_from_ram
from app.html_builder import build_email
from app.figure_maker import plot_wordcount, plot_word_correlation, plot_timechart
from spacytextblob.spacytextblob import SpacyTextBlob

#config = dotenv_values(".env")
#all_list = grep_dict(config, 'LIST')
#client=config_tweepy_client(config)
#max_res, limit = get_n_tweets(config)
#list_pages=get_list_of_pages(client, list_id=all_list[0], max_results=max_res, limit=limit)
#list_of_tweets=tweets_from_pages(client, list_pages) 
#twlist=tweet_to_df(list_of_tweets)
#twlist, email, attachment_cid=run_tweet_report(config)
#list_to_words=top_words(word_counter(twlist['nouns']), 20)
#with open('test.html', 'w') as f:
#    f.write(email.render())
