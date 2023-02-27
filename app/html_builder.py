import dominate
import pandas as pd
from dominate.tags import *

def read_css_file(filename):

    """Read a css file and return a string
    :param filename: a css file name
    """

    with open(filename, 'r') as file:
        css_string = file.read()
    return css_string

def dict_to_obj(dict) -> object:

    """Convert a dictionary to an object
    :param dict: a dictionary
    """

    class Obj(object):
        def __init__(self, d):
            self.__dict__ = d

    return Obj(dict)

def sort_df(df, col, n) -> pd.DataFrame:

    """ sort a dataframe by a column and return the top n rows
    :param df: a pandas dataframe
    :param col: a column name to sort by
    :param n: number of rows to return
    """

    df = df.sort_values(by=col, ascending=False)
    df = df.head(n)
    return df

def split_tweet(tweet_text, current_td) -> str:

    """" Split tweet text into fragments
    :param tweet_text: a tweet text string
    :param current_td: a dominate td object"""

    if "\n" in tweet_text:
        tw_fragments=tweet_text.split('\n')
        with current_td:
            for twf in tw_fragments:
                current_td.add(p(
                    twf
                    , style= "font-family:Helvetica"))
    else:
        current_td.add(p(
            tweet_text
            , style= "font-family:Helvetica"))

    return current_td

def text_to_emoji(text) -> str:

    """"
    Convert text to emoji
    :param text: a text string
    """
    
    if text == 'retweet_count':
        emoji = '🔁'
    if text == 'reply_count':
        emoji = '💬'
    if text == 'like_count':
        emoji = '💓'
    if text == 'quote_count':
        emoji = '📜'
    if text == 'impression_count':
        emoji = '👁️'

    return emoji

def check_iter_odd(n) -> bool:
    
    """"
    Check if a number is odd
    :param n: an integer
    """

    if n % 2 == 0:
        return False
    else:
        return True

def reshape_test(tw0, mytable, iter, counter=0) -> dominate.document:

    """"
    Reshape tweet data into a table
    :param tw0: a tweet object
    :param mytable: a dominate table object
    :param counter: a counter to identify whether the tweet is original or a quote
    """
    if check_iter_odd(iter):
        row = 'odd'
    else:
        row = 'even'

    avatar_style="""padding: 12px;
                    border-radius: 50%;
                    max-width: 48px;
                    max-height: 48px;"""
    avatar_cell_style= """@media only screen and (max-width: 700px) {
                          padding-left: 12px; 
                          padding-right: 70px !important; 
                          color: #4A5056}"""
    tweet_table_style="""border-collapse: collapse; 
                         border: 1px solid #ddd;"""
    quote_tw_style="""
                    margin-left: auto;
                    margin-right: auto;
                    background-color: #ffffff; 
                    filter: alpha(opacity=40); 
                    opacity: 0.95;
                    min-width: 650px;
                    border:1px grey solid;
                    border-radius:50%;

                    """

    if counter == 0:
        quote_tw=''
    else:
        quote_tw='_qt'
    with mytable as tweet_table:

        #tweet_table.set_attribute('class', 'tweet_box_{}'.format(row))
        tweet_table.set_attribute('style', tweet_table_style)
        with tr(cls='tweet_row_{}'.format(row)):
            td(img(src=tw0.profile_url, cls = 'avatar', style = avatar_style), 
                    cls = 'prof_cell', rowspan="2",width="48", height="48", style=avatar_cell_style)
            td(tw0.user, cls='username_cell{}'.format(quote_tw))
        with tr(cls='tweet_row_{}'.format(row)):
            td().add(
                a('@{}'.format(tw0.username), 
                href='https://twitter.com/{}'.format(tw0.username), 
                cls='username_cell{}'.format(quote_tw),
                style = "color: #360bcf")
            )
        with tr(cls='tweet_row_{}'.format(row)):
            if counter == 1:
                td()
                
            split_tweet(tw0.text, td(cls = 'tweet_cell', colspan="2"))
        if tw0.media_url != None:
            if len(tw0.media_url) >= 1:
                for media in tw0.media_url:
                    if media != None:
                        with tr(cls='tweet_row_{}'.format(row)):

                            if 'png' in media or 'jpg' in media or 'jpeg' in media:
                                td()
                                td(img(src=media, style="max-width: 647px;"))
                            if 'mp4' in media:
                                media=media.replace('?tag=14','')
                                media=media.replace('?tag=12','')
                                td()
                                td(video(width="320", height="240", src=media, type="video/mp4"))
        with tr(cls='tweet_row_{}'.format(row)):
            td()
            with td():
                metrics= {'retweet_count': tw0.retweet_count, 
                    'reply_count': tw0.reply_count, 
                    'like_count' : tw0.like_count, 
                    'quote_count' : tw0.quote_count, 
                    'impression_count' : tw0.impression_count
                }
                for key, value in metrics.items():
                    emoji = text_to_emoji(key)

                    span(' {}: '.format(emoji))
                    span(value)

        if tw0.tw_quote == 'yes' and counter == 0:
            quote = dict_to_obj(tw0.quote)
            with tr(cls='tweet_row_{}'.format(row)):
                with td(colspan="2"):
                    with table(cls='quote', style=quote_tw_style) as qtable:
                        with tbody():
                            reshape_test(quote, qtable, iter, counter=1)
            
    return tweet_table

def join_tweets(body, mytable, list_of_tweets) -> dominate.document:

    """
    This function takes a list of tweets and joins them into a single table
    :param body: the body of the email
    :param mytable: the table to be populated
    :param list_of_tweets: the list of tweets to be joined
    """

    counter = 0
    for row in list_of_tweets.itertuples():
        counter += 1
        with body:
            with mytable:
                reshape_test(row, mytable, iter=counter, counter=counter)
                            
    return body

def create_headings(body, list_of_tweets, attachment_cid, inline_title_style) -> dominate.document:

    """create the headings for the email
    :param body: the body of the email
    :param list_of_tweets: the list of tweets to be joined
    :param attachment_cid: the cid of the image to be attached
    :param inline_title_style: the style of the title
    """

    with body:
        with table(cls='main_table', id='main_table') as maintable:
            with tr(cls='section_title'):
                td(style='border-bottom: 5px solid grey')
                td("Sentiment", cls="section_title", style=inline_title_style)
                sent=list_of_tweets.sentiment.mean()
                sent=round(sent, 2)
                polarity=list_of_tweets.polarity.mean()
                polarity=round(polarity, 2)
            with tr():
                td()
                td('Sentiment: {}'.format(str(sent)), 
                style="font-size: 60px;font-weight: bold;font-family:Helvetica;color: #E36B5B")
            with tr():
                td()
                td(img(src='cid:' + attachment_cid[1][1:-1], 
                style="max-width: 100%a;"))

            with tr():
                td()
                td('Polarity: {}'.format(str(polarity)), 
                style="font-size: 60px;font-weight: bold;font-family:Helvetica;color: #88ADE3")
            with tr():
                td()
                td(img(src='cid:' + attachment_cid[2][1:-1], 
                style="max-width: 100%;"))

            with tr(cls='section_title'):
                td(style='border-bottom: 5px solid grey')
                td("Topic \nAnalysis", cls="section_title", 
                style=inline_title_style)
            
            with tr():
                td()
                td(img(src='cid:' + attachment_cid[0][1:-1], 
                style="max-width: 100%;"))

            with tr(cls='section_title'):
                td(style='border-bottom: 5px solid grey')
                td("Word \nCorrelation", cls="section_title", 
                style=inline_title_style)

            with tr():
                td()
                td(img(src='cid:' + attachment_cid[3][1:-1], 
                style="max-width: 100%;"))

            with tr(cls='section_title'):
                td(style='border-bottom: 5px solid grey')
                td("Topic \ntweets", cls="section_title", 
                style=inline_title_style)


    return body

def build_email(attachment_cid, list_of_tweets, n_top_tweets=10, n_relevant_tweets=10, save_email=False) -> dominate.document:

    """build the email
    Takes the list of tweets and builds the email newsletter.
    :param attachment_cid: the cid of the image to be attached
    :param list_of_tweets: the list of tweets to be joined
    :param n_top_tweets: the number of top tweets to be included
    :param n_relevant_tweets: the number of relevant tweets to be included
    :param save_email: whether to save the email
    """
    doc_style = read_css_file('datafiles/newsletter_style.css')
    doc = dominate.document(title='Tweeter Report')
    inline_title_style="""margin: 100px 25px 50px 25px;
                          padding-left: 24px;
                          padding-right: 24px;
                          font-size: 130px;
                          font-family:Helvetica;
                          font-weight: bold;
                          border-bottom: 5px solid grey;"""

    with doc.head:
        meta(name='viewport', content='width=device-width, initial-scale=1.0')
        meta(http_equiv='Content-Type', content='text/html; charset=utf-8')
        meta(http_equiv='X-UA-Compatible', content='IE=edge')
        style(doc_style)

    with doc.body as doc_body:
        create_headings(doc_body, list_of_tweets, attachment_cid, inline_title_style)
    
    join_tweets(doc.body, doc.body.getElementById('main_table'),  
                        sort_df(list_of_tweets, 'score', n_relevant_tweets))
    with doc.body.getElementById('main_table'):
        with tr(cls='section_title'):
            td(style='border-bottom: 5px solid grey')
            td("Best tweets", cls="section_title", style=inline_title_style)
    join_tweets(doc.body, doc.getElementById('main_table'),  
                        sort_df(list_of_tweets, 'like_count', n_top_tweets))

    if save_email:
        with open('app/datafiles/test.html', 'w') as f:
            f.write(doc.render())

    return doc
