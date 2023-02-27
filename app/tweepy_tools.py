import tweepy

def get_tweet(client, twid) -> tweepy.client.Response:

    """ Get the tweet response with pre-defined configuration from the tweepy API. 
    :param client: Tweepy client object.
    :param twid: Tweet id.
    """

    tweet=client.get_tweet(twid,
                           expansions=['attachments.media_keys', 'author_id'],
                           media_fields = ['media_key','url', 'preview_image_url', 'variants'], 
                           user_fields =['name', 'username', 'profile_image_url'],
                           tweet_fields = ['text', 'attachments','referenced_tweets', 'public_metrics', 'created_at', 'lang'])
    
    return tweet

def list_tweets(client, tweets_list):
    
    """ Extract the valuable info a list of tweets to assemble the HTML representation. It returns
    a list of tweet_infos.
    :param tweet: A tweet response from the tweepy API.
    """

    twlist=[]
    for twi in tweets_list.data:
        tweet_i=get_tweet(client, twi.id)
        twlist.append(tweet_info(client, tweet_i))
    
    return twlist

def tweet_info(client, tweet) -> dict:

    """ Extract the valuable info of the tweet to assemble the HTML representation. It
    returns a dictionary with the tweet text, attachments, user, username, user profile image, 
    urls for all media and quoted tweets.
    :param tweet: A tweet response from the tweepy API.
    """

    # Get tweet
    twi=tweet.data
    ref_tweet=twi.referenced_tweets
    user=tweet.includes['users'][0]
    media_urls=[]

    # Get media
    if 'media' in tweet.includes.keys():
        
        for  media_i in tweet.includes['media']:
            if media_i.type == 'photo':
                media_urls.append(media_i.url)
            if media_i.type == 'video':
                media_urls.append(media_i.data['variants'][1]['url'])
    
    # If present, then recursively extract Quoted tweet
    counter=0
    if type(ref_tweet) is list:
        
        if ref_tweet[0].type == 'quote' and counter < 1:
            counter+=1
            qid = twi.referenced_tweets[0]
            qtwi=get_tweet(client, qid.id)
            twquote=tweet_info(client, qtwi)
            qtweet='yes'

        else:

            qtweet='no'
            twquote=None
    
    else:

        qtweet='no'
        twquote=None

    # Build dictionary for output
    tweet_dict={
        'tweet_id': twi.id,
        'text' : twi.text,
        'attachments' : twi.attachments,
        'user' : user.name,
        'username' : user.username,
        'profile_url' : user.profile_image_url,
        'metrics' : twi.public_metrics,
        'created' : twi.created_at,
        'lang' : twi.lang,
        'media_url' : media_urls,
        'tw_quote':qtweet,
        'quote' : twquote
        }

    return tweet_dict

def tweets_from_pages(client, list_pages) -> dict:

    """ Extract the valuable info a list of tweets to assemble the HTML representation. It returns
    a list of tweet_infos.
    :param list_pages: A list of pages from the tweepy API.
    """

    tweetlist=[]
    for response in list_pages:

    # Exrtact user info
        all_users={}
        all_usernames={}
        all_userimages={}
        for user in response.includes['users']:
            all_usernames[user.id]=user.username
            all_users[user.id]=user.name
            all_userimages[user.id]=user.profile_image_url

        # Exrtact media info
        all_media={}
        for media in response.includes['media']:
            all_media[media.media_key]=media.url

        # Iterate over response data
        for tw_i in response.data:

            # Match attachments
            try:
                media_urls = [all_media[mediakey[0]] for mediakey in tw_i.attachments.values()]
            except:
                media_urls=None
            
            # Get quoted tweets
            qtweet='no'
            twquote=None
            if tw_i.referenced_tweets is not None:
                reft=tw_i.referenced_tweets[0]

                if reft.type == 'quoted':
                    qtwi=get_tweet(client, reft.id)
                    twquote=tweet_info(tweet_info, qtwi)
                    qtweet='yes'
                
            tweet_dict={
                'tweet_id': tw_i.id,
                'text': tw_i.text,
                'user':  all_users[tw_i.author_id],
                'username' : all_usernames[tw_i.author_id],
                'profile_url' : all_userimages[tw_i.author_id],
                'metrics' : tw_i.public_metrics,
                'created' : tw_i.created_at,
                'lang' : tw_i.lang,
                'media_url' : media_urls,
                'tw_quote':qtweet,
                'quote' : twquote
                }

            tweetlist.append(tweet_dict)
    
    return tweetlist

def config_tweepy_client(config):

    """ Shorter call function to setup a tweepy client.
    :param config: dictionary with the token info. The required fields are BEARER_TOKEN, API_KEY, API_KEY_SECRET, ACCESS_TOKEN and ACCESS_SECRET.
    """

    client = tweepy.Client(bearer_token=config['BEARER_TOKEN'],
    consumer_key=config['API_KEY'], consumer_secret=config['API_KEY_SECRET'],
    access_token=config['ACCESS_TOKEN'], access_token_secret=config['ACCESS_SECRET'])

    return client

def get_n_tweets(config):

    """Get the tweets per pages and number of pages for a request
    :param config: dictionary with the NTWEETS info.
    """

    n=int(config['NTWEETS'])

    if n <= 100:
        max_results=n
        limit=1
    else:
        max_results=100
        limit=int(n/100)

    return max_results, limit

def get_list_of_pages(client, list_id, max_results=100, limit=10):

    list_pages = tweepy.Paginator(client.get_list_tweets, list_id, 
                           expansions=['attachments.media_keys', 'author_id'],
                           media_fields = ['media_key','url', 'preview_image_url', 'variants'], 
                           user_fields =['name', 'username', 'profile_image_url'],
                           tweet_fields = ['text', 'attachments','referenced_tweets', 'public_metrics', 'created_at', 'lang'], 
                           max_results=max_results, limit=limit)

    return list_pages