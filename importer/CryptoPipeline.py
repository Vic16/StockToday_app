import tweepy
import json
import pandas as pd
import traceback
import time
import random

from config.config import config

from importer import grafics
from importer import CryptoModule
from importer import apiConnectors

# Cargar credenciales desde el archivo JSON
with open('credentials.json') as config_file:
    credentials = json.load(config_file)


bearer_token=credentials['bearer_token']
consumer_key=credentials['API_Key']
consumer_secret=credentials['API_key_secret']
access_token=credentials['Access_Token']
access_token_secret=credentials['Acces_Token_Secret']

crytoTweetsBase = config["Cryptotweets"]
cryptoList = config["Crypto"]["CryptCodes"]
cryptoList = [item for item in cryptoList if item["enable"] == "True"]

for currency in cryptoList:
    cryptoName = currency["name"]
    ticker = currency["ticker"]
    currency = CryptoModule.Crypto(crypto_name=cryptoName, cryptoTicker=ticker)
    status = currency.get_current_status()
    fig = currency.plot_price()
    img = grafics.saveFigMemory(fig=fig)

    client_v1 = apiConnectors.get_twitter_conn_v1(consumer_key=consumer_key, consumer_secret=consumer_secret, 
                                                access_token=access_token, access_token_secret=access_token_secret)
    client_v2 = apiConnectors.get_twitter_conn_v2(consumer_key=consumer_key, consumer_secret=consumer_secret,  
                                                access_token=access_token, access_token_secret=access_token_secret)
    media = client_v1.media_upload(filename="temp.png", file=img)
    tweetBase = random.choice(crytoTweetsBase)
    
    # Publicar el Tweet con la imagen
    tweet_text = tweetBase.replace("{crypto_name}",cryptoName)
    tweet_text = tweet_text.replace("{current_price}",str(round(status["Current Price"],3)))
    tweet_text = tweet_text.replace("{variation}",str(status["Variation"]))
    tweet_text = tweet_text.replace("{emoji}", status["Emoji"])
    tweet_text = tweet_text.replace("{","").replace("}","")
    tweet_text += "\n\n"
    #tweet_text = f'"🔍 Tracking the latest trends in {cryptoName}! Current price: ${current_price}, variation: {variation}% {emoji}. Stay updated on the market movements. 📊 #Crypto #Blockchain #DeFi"' + "\n\n" 
    response = client_v2.create_tweet(text=tweet_text, media_ids=[media.media_id])
    print("Tweet Done!, sleeping")
    time.sleep(150)
