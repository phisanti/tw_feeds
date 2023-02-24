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

def get_next_run_time():
    now = datetime.datetime.now()
    today = datetime.datetime.today()
    next_run_time = datetime.datetime.combine(today, datetime.time(hour=8, minute=0))
    if now >= next_run_time:
        next_run_time += datetime.timedelta(days=1)
    return next_run_time

def trigger_tweet_report(config):
    """ Trigger the tweet analyser once a day.
    :param config: Dictionary with the all settings.
    """
    # get the current date and time
    while eval(config['RUN']):
        
        # Run tweet analyser
        run_tweet_report(config)
        config = dotenv_values(".env")
        # wait for 24 hours before scheduling again
        now = datetime.datetime.now()
        next_run_t=get_next_run_time()
        waiting_time = next_run_t - now
        waiting_hours = waiting_time.total_seconds() / 3600
        print('tweet report done, waiting for next run {} hour(s)'.format(waiting_hours))
        time.sleep(waiting_time.total_seconds())

    return True

def run_tweet_report(config, nlp=None, boring_list=None):

    """ Master function for the tweet analyser.
    :param config: Dictionary with the all settings.
    :param nlp: a loaded SpaCy NLP model
    :param boring_list: a list of boring words to remove from tweets.
    """

    if boring_list is None:
        boring_list=read_boring_list()
    
    if nlp is None:
        disable_feat = [
                    'textcat',
                    'textcat_multilabel',
                    'trainable_lemmatizer'
                    ]
        nlp = spacy.load("en_core_web_sm",  exclude = disable_feat
        )
        nlp.add_pipe('spacytextblob')

    # Get tweets
    client=config_tweepy_client(config)
    max_res, limit = get_n_tweets(config)
    list_pages=get_list_of_pages(client, list_id=config['LIST_ID'], max_results=max_res, limit=limit)
    list_of_tweets=tweets_from_pages(client, list_pages) 
    twlist=tweet_to_df(list_of_tweets)

    # Extract nouns
    twlist['nouns'], twlist['tokens'], twlist['sentiment'], twlist['polarity'] = tweet_analyser(twlist, nlp, boring_list=boring_list)
    twlist['score'] = score_tweets(twlist, column='tokens')

    # Plot figures
    plot_wordcount(twlist, column='nouns', cutoff=30)
    plot_timechart(twlist)
    list_to_words=top_words(word_counter(twlist['tokens']), 20)
    plot_word_correlation(twlist, 'tokens', list_to_words)
    
    # Build email
    attachment_cid=make_msgid_list(4)
    email=build_email(attachment_cid, twlist, n_relevant_tweets=20, n_top_tweets=20)

    # Send email
    send_newsletter_from_ram(config, email_html=email, attachment_cid=attachment_cid)

    return twlist, email, attachment_cid

config = dotenv_values(".env")
twlist, email, attachment_cid=run_tweet_report(config)
#list_to_words=top_words(word_counter(twlist['nouns']), 20)
#with open('test.html', 'w') as f:
#    f.write(email.render())
