import tweepy
import json
import pandas as pd
import traceback

from importer import utils
from importer import grafics
from importer import StockDataFetcher
from importer import apiConnectors

# Cargar credenciales desde el archivo JSON
with open('credentials.json') as cred_file:
    credentials = json.load(cred_file)

bearer_token = credentials['bearer_token']
consumer_key = credentials['API_Key']
consumer_secret = credentials['API_key_secret']
access_token = credentials['Access_Token']
access_token_secret = credentials['Acces_Token_Secret']

dfCodes = pd.read_excel("data/StocksDB.xlsx")
dfCodes = dfCodes[dfCodes["CodigoGoogleMercado"]=="VIE"]
dfCodes = dfCodes.sample(12)


stocks = []
for index, row in dfCodes.iterrows():
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
styled = grafics.setTableStyles(df_stocks)

img = grafics.saveDFMemory(styled)
client_v1 = apiConnectors.get_twitter_conn_v1(consumer_key=consumer_key, consumer_secret=consumer_secret, 
                                              access_token=access_token, access_token_secret=access_token_secret)
client_v2 = apiConnectors.get_twitter_conn_v2(consumer_key=consumer_key, consumer_secret=consumer_secret,  
                                              access_token=access_token, access_token_secret=access_token_secret)



# https://stackoverflow.com/questions/70891698/how-to-post-a-tweet-with-media-picture-using-twitter-api-v2-and-tweepy-python
# Subir la imagen a Twitter
media = client_v1.media_upload(filename="temp.png", file=img)

#media = client.media_upload(file=img, media_type='image/png')
# Publicar el Tweet con la imagen
tweet_text = 'Here are some stocks! #VIE' + ' ' + config["DefaultHashtags"]

response = client_v2.create_tweet(text=tweet_text, media_ids=[media.media_id])
