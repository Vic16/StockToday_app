import yfinance as yf
import requests
from bs4 import BeautifulSoup

class StockDataFetcher:
    def __init__(self, yahooticker, googleticker, googleMarketCode, CompanyName, Country):
        self.yahooticker = yahooticker
        self.googleticker = googleticker
        self.googleMarketCode = googleMarketCode
        self.CompanyName = CompanyName
        self.Country = Country 

    def getYahooData(self, period, interval):
        """
        :param period: Período de tiempo para obtener datos históricos (por defecto: "1mo").
                       Ejemplos: "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"
        :param interval: Intervalo de los datos (por defecto: "1d").
                         Ejemplos: "1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"
        
        :return: DataFrame con los datos históricos del ticker.
        """
        stock = yf.Ticker(self.yahooticker)
        data = stock.history(period=period)
        historical_data = stock.history(period=period, interval=interval)
        return historical_data

    def getYahooDataCloseprice(self):
        """
        """
        closePrice = self.getYahooData(period="5d", interval="1d")
        closePrice = closePrice["Close"].iloc[-2]
        return float(round(closePrice,2))
    
    def getGoogleCurrentPrice(self):
        """
        """
        url = "https://www.google.com/finance/quote/{}:{}?".format(self.googleticker, self.googleMarketCode)
        response = None
        soup = None
        headers = {"Cache-Control": "no-cache","Pragma": "no-cache"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        price = soup.find(class_="YMlKec fxKbKc").text.replace(",","")
        return float(price[1:])
    
    def getCurrentStatus(self):
        """
        """
        closePrice = self.getYahooDataCloseprice()
        currentPrice = self.getGoogleCurrentPrice()
        change = round(((currentPrice - closePrice)/closePrice)*100,2)
        
        return {"Stock":self.googleticker, 
                "CurrentPrice":currentPrice,
                "ClosePrice":closePrice,
                "Variation": change,
                "Name": self.CompanyName,
                "Country": self.Country,
                "Market": self.googleMarketCode}