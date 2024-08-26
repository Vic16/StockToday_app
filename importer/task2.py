from publishers import StockTweetPublisherLinePlot
import json
# Cargar credenciales desde el archivo JSON
with open('../credentials.json') as config_file:
    config = json.load(config_file)

bearer_token=config['bearer_token']
consumer_key=config['API_Key']
consumer_secret=config['API_key_secret']
access_token=config['Access_Token']
access_token_secret=config['Acces_Token_Secret']

twt = StockTweetPublisherLinePlot(yahooticker="AAPL", googleticker="AAPL", googleMarketCode="NASDAQ", CompanyName="Apple Inc.", Country="USA").plotClose(period="5y", interval="1d")
twt.publisTweetPlot(TweetText="Apple!", TweetHastags="#StockMarket", 
                    fig=twt, consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)