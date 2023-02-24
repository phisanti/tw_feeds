import re
import string
import pandas as pd
import numpy as np
import emoji
from collections import Counter
import contractions

def tweet_to_df(tweet_list) -> pd.DataFrame:
    
    """ Get the text from a tweet list and generates a list text.
    :param tweet_list: A list of tweets from list_tweets.
    """
    tweets = []
    
    for twi in tweet_list:
        twi.update(twi['metrics'])
        twi.pop('metrics')
        tweets.append(twi)

        if twi['tw_quote'] == 'yes':
            qt = twi['quote']
            qt.update(qt['metrics'])
            qt.pop('metrics')
            tweets.append(qt)

    df=pd.DataFrame(tweets)
    df['clean_tweet']=df['text'].apply(lambda x: clean_tweet(x))

    return df

def remove_emoji(text):

    """
    Removes emoji's from tweets
    Accepts:
        Text (tweets)
    Returns:
        Text (emoji free tweets)
    """
    emoji_list = [c for c in text if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.split() if not any(i in str for i in emoji_list)])
    return clean_text

def clean_tweet(tweet) -> str:
    
    """ Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    :param tweet: a tweet text string.
    """
    expanded_tweet = []   
    for word in tweet.split():
        # using contractions.fix to expand the shortened words
       expanded_tweet.append(contractions.fix(word))  
    tweet = ' '.join(expanded_tweet)
    tweet=emoji.replace_emoji(tweet,'')    
    tweet = re.sub("&amp;", "and", tweet) # https://www.youtube.com/watch?v=O2onA4r5UaY
    tweet = re.sub("http\\S+", "", tweet) # https://www.youtube.com/watch?v=O2onA4r5UaY
    tweet = re.sub('[^a-zA-Z 0-9]', '', tweet)
    tweet = re.sub('[%s]' % re.escape(string.punctuation), '', tweet) # Remove punctuation
    tweet = re.sub('\\w*\\d\\w*', '', tweet) # Remove words containing numbers
    tweet = re.sub('@*', '', tweet)
    tweet = re.sub('RT*', '', tweet)
    tweet = re.sub('  ', ' ', tweet)
    
    return tweet

def read_boring_list() -> list:

    """ Read list of boring words to remove from a tweet.
    """

    with open('app/datafiles/boring_words.txt', 'r') as f:
        boring_list = f.read().splitlines()

    return boring_list

def word_counter(token_col, return_freq=True) -> Counter:

    """ Count words in a list of tokens.
    :param token_col: a pandas col of tokens.
    """

    flat_list = [item for sublist in token_col.to_list() for item in sublist]
    wcount=Counter(flat_list)
    if return_freq:
        output=word_freq(wcount)
    else:
        output=wcount

    return output

def word_freq(word_count):
    
    """ Calculate word frequencies.
    :param word_count: a dictionary of word counts.
    """
    total=sum(word_count.values())
    return {k: v/total for k, v in word_count.items()}

def score_tweets(twlist, column):

    """ Score tweets based on word frequencies.
    :param twlist: a pandas dataframe containing the column tweets. This column must be a string.
    :param wordfreq: a dictionary of word frequencies to assing tweet scores.
    """
    wordcount=word_counter(twlist[column])
    wordfreq=word_freq(wordcount)
    score=[]
    for row in twlist.itertuples():
        score.append(sum([wordfreq.get(word, 0) for word in row.nouns]))
    return score

def tweet_analyser(twlist, nlp, boring_list, lang = 'en') -> list:

    """ Extract nouns and proper nouns from tweets.
    :param tweet_col: a pandas col of tweets or strings.
    :param nlp: a loaded SpaCy NLP model
    :param boring_list: a list of boring words to remove from tweets.
    :param lang: a string with the language of the tweets.
    :return: a list of lists of key words, nouns, sentiment and subjectivity.
    """

    tokens = []
    nouns = []
    sent=[]
    subj=[]
    for row in twlist.itertuples():

        twi_nouns=[]
        twi_token=[]
        
        
        if row.lang != lang:
            nouns.append([])
            tokens.append([])
            sent.append(None)
            subj.append(None)
        else:
        
            doc=nlp(row.clean_tweet)
            sent.append(doc._.polarity)
            subj.append(doc._.subjectivity)

            for token in doc:

                if token.lemma_.lower() in boring_list:
                    continue

                else:
                    if token.pos_ == 'NOUN' or token.pos_ == 'PROPN':
                        twi_nouns.append(token.lemma_)
                        
                    if token.pos_ == 'NOUN' or token.pos_ == 'PROPN' or token.pos_ == 'VERB' or token.pos_ == 'ADJ':
                        twi_token.append(token.lemma_)
            
            nouns.append(twi_nouns)
            tokens.append(twi_token)
    
    return nouns, tokens, sent, subj

def filter_df_by_tokens(target_words, df, column='tokens'):
    """Filter a DataFrame by a list of tokens
    :param target_words: a list of tokens
    :param df: a pandas DataFrame"""

    # Boolean mask 
    mask = df[column].apply(lambda tokens: any(word in tokens for word in target_words))
    
    # Filter the DataFrame using the mask
    filtered_df = df[mask]
    return filtered_df

def word_corr(df, target_words=None, column='nouns') -> pd.DataFrame:

    """"Compute the correlation matrix for a list of words in a DataFrame column
    :param df: a pandas DataFrame
    :param column: the name of the column containing the list of words"""
    if target_words == None:
        df=df
    else:
        df=filter_df_by_tokens(target_words, df, column)
    
    # Create a list of all unique words
    all_words = np.unique(np.concatenate(df[column].to_list()))
    word_counts = np.zeros((len(df), len(all_words)))

    for i, word in enumerate(all_words):
        word_counts[:, i] = df[column].apply(lambda x: x.count(word)).values

    # Compute the correlation matrix using NumPy operations
    correlation_matrix = np.corrcoef(word_counts, rowvar=False)
    corr_df = pd.DataFrame(correlation_matrix, columns=all_words, index=all_words)

    return corr_df

def top_words(word_list, n):

    """"Select the top n most frequent words from a word count dictionary produced by word_count
    :param word_list: a dictionary of word counts
    :param n: the number of words to select
    :return: a list of the top n words"""
        
    word_list = sorted(word_list.items(), key=lambda x: x[1], reverse=True)
    word_list = [word[0] for word in word_list[:n]]
        
    return word_list


def filter_correlation_matrix(corr_df, word_list):

    """" Filter a correlation matrix to only include words in a list
    :param corr_df: a pandas DataFrame containing the correlation matrix
    :param word_list: a list of words to include in the submatrix
        (output of word_corr)
    """

    mask = np.isin(corr_df.columns, word_list)    
    submatrix = corr_df.loc[mask, mask]
    
    return submatrix
