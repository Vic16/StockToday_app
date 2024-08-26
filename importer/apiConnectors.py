import tweepy


def get_twitter_conn_v1(consumer_key, consumer_secret, access_token, access_token_secret) -> tweepy.API:
    """Get twitter conn 1.1"""

    auth = tweepy.OAuth1UserHandler(consumer_key=consumer_key, consumer_secret=consumer_secret,
                                    access_token=access_token,access_token_secret=access_token_secret)
  
    return tweepy.API(auth)

def get_twitter_conn_v2(consumer_key, consumer_secret, access_token, access_token_secret) -> tweepy.Client:
    """Get twitter conn 2.0"""

    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    return client

def oauth(consumer_key, consumer_secret, access_token, access_token_secret):
    """ """
    auth = get_twitter_conn_v1(consumer_key, consumer_secret, access_token, access_token_secret)
    client = get_twitter_conn_v2(consumer_key, consumer_secret, access_token, access_token_secret)
    authParams = {"connV1":auth,"connV2":client}
    
    return authParams