from StockDataFetcher import StockDataFetcher
from apiConnectors import oauth
from grafics import plot_stock_close, saveFigMemory


def StockTweetPublisherLinePlot()
    #def __init__(self, StockDataFetcher,yahooticker, googleticker, googleMarketCode, CompanyName, Country):
    stock_data_fetcher = StockDataFetcher(yahooticker, googleticker, googleMarketCode, CompanyName, Country)

    def plotClose(self,period, interval):
        data = self.StockDataFetcher().getYahooData(period, interval)
        plotFig = plot_stock_close(df=data, stock_code=self.stock_data_fetcher.googleticker)
        fig = saveFigMemory(fig=plotFig)
        return fig
        
    def publisTweetPlot(self, TweetText, TweetHastags, fig, consumer_key, consumer_secret, access_token, access_token_secret):
        authParams = oauth(consumer_key, consumer_secret, access_token, access_token_secret)
        media = authParams["connV1"].media_upload(filename="temp.png", file=fig)
        TweetText = TweetText + " " + TweetHastags
        createTweet = authParams["connV2"].create_tweet(text=TweetText, media_ids=[media.media_id])

        


