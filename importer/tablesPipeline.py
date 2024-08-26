import tweepy
import json
import pandas as pd
import traceback
import time
import random

from config.config import config
from importer import utils
from importer import grafics
from importer import StockDataFetcher
from importer import apiConnectors

# Cargar credenciales desde el archivo JSON
with open('credentials.json') as config_file:
    credentials = json.load(config_file)

dfCodes = pd.read_excel("data/StocksDB.xlsx")


bearer_token=credentials['bearer_token']
consumer_key=credentials['API_Key']
consumer_secret=credentials['API_key_secret']
access_token=credentials['Access_Token']
access_token_secret=credentials['Acces_Token_Secret']


###################################
###### Taks 1 Europe Markets ######
###################################

europeMarkets = config["Markets"]["Europe"]
europeMarkets = [item for item in europeMarkets if item["Enable"] == "True"]
random.shuffle(europeMarkets)

for market in europeMarkets:
    print(market["Name"])
    df_sample = dfCodes[dfCodes["CodigoGoogleMercado"]==market["Name"]]#.sample(5)
    stocks = []

    for index, row in df_sample.iterrows():
        try:
            stockData = StockDataFetcher.StockDataFetcher(yahooticker=row['CodigoYahooFinance'], 
                                                            googleticker=row['CodigoGoogleFinance'], 
                                                            googleMarketCode=row['CodigoGoogleMercado'],
                                                            CompanyName=row["Nombre de la empresa"],
                                                            Country=row["Country"]).getCurrentStatus()
            stocks.append(stockData)
            print(stockData)
            print("-------")
        except Exception as e:
            print(e)
            print("******************************************")
            print(traceback.format_exc())
            continue
    
    df_stocks = pd.DataFrame(stocks)
    df_stocks = utils.prepareDF(df_stocks)

    chartEmoji = config["Emojis"]["chart_emoji"].encode().decode('unicode_escape')
    chartUp = config["Emojis"]["up_emoji"].encode().decode('unicode_escape')
    chartDown = config["Emojis"]["down_emoji"].encode().decode('unicode_escape')
    chartFlat = config["Emojis"]["flat_emoji"].encode().decode('unicode_escape')

    moversText = utils.createStockMovers(df=df_stocks, chartEmoji=chartEmoji, UpEmoji=chartUp, FlatEmoji=chartFlat, DownEmoji=chartDown)
    


    styled = grafics.setTableStyles(df_stocks.sample(5))
    img = grafics.saveDFMemory(styled)
    client_v1 = apiConnectors.get_twitter_conn_v1(consumer_key=consumer_key, consumer_secret=consumer_secret, 
                                                access_token=access_token, access_token_secret=access_token_secret)
    client_v2 = apiConnectors.get_twitter_conn_v2(consumer_key=consumer_key, consumer_secret=consumer_secret,  
                                                access_token=access_token, access_token_secret=access_token_secret)
    media = client_v1.media_upload(filename="temp.png", file=img)
    # Publicar el Tweet con la imagen
    flag = market["Flag"].encode().decode('unicode_escape')
    tweet_text = f'Here are some stocks 🚀📈💰! #{market["Name"]} {flag}' + ' ' + market["Hashtags"] + "\n\n" + moversText
    response = client_v2.create_tweet(text=tweet_text, media_ids=[media.media_id])
    
    waitTime = random.randint(5 * 60, 8 * 60)
    print("Sleeping...")
    time.sleep(waitTime)


