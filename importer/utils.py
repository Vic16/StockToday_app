import pandas as pd
from config.config import config

def prepareDF(df):
    """
    """
    ##### Previus transfom
    #data = pd.DataFrame(stocks)
    columns = ["Stock Code", 'Current Price', 'Close Price', 'Variation', 'Company Name', 'Country','Market']
    colsOrder = ["Stock Code","Company Name","Variation","Current Price","Close Price","Market","Country"]
    df.columns = columns 
    df = df[colsOrder]
    #df.set_index('Stock Code', inplace=True)
    df = df[["Stock Code","Company Name","Variation","Current Price","Close Price"]]
    df.sort_values("Variation", ascending=False)
    return df 

def createStockMovers(df, chartEmoji,UpEmoji, FlatEmoji, DownEmoji):
    df = df.sort_values(by='Variation', ascending=False)
    
    top_gainers = df.head(3)
    top_losers = df.tail(3)
    up_emoji = UpEmoji
    down_emoji = DownEmoji
    flat_emoji = FlatEmoji

    # Crear el texto del tweet
    tweet_text = f"{chartEmoji} Top Movers Today:\n\n"

    # Añadir los 3 mayores aumentos
    tweet_text += "🔼 Gainers:\n"
    for _, row in top_gainers.iterrows():
        emoji = up_emoji if row['Variation'] > 0 else (down_emoji if row['Variation'] < 0 else flat_emoji)
        tweet_text += f"{row['Stock Code']}: {row['Variation']}% {emoji}\n"

    # Añadir los 3 mayores descensos
    tweet_text += "\n🔽 Losers:\n"
    for _, row in top_losers.iterrows():
        emoji = down_emoji if row['Variation'] < 0 else (up_emoji if row['Variation'] > 0 else flat_emoji)
        tweet_text += f"{row['Stock Code']}: {row['Variation']}% {emoji}\n"

    return tweet_text