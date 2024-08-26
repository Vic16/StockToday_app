import json
import random
import os
from importer import apiConnectors
from config.config import config


# Definir la ruta del archivo de configuración
CONFIG_DIR = os.path.join(os.path.dirname(__file__), '..', 'config')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.json')


# Cargar credenciales desde el archivo JSON
with open('credentials.json') as config_file:
    credentials = json.load(config_file)


bearer_token=credentials['bearer_token']
consumer_key=credentials['API_Key']
consumer_secret=credentials['API_key_secret']
access_token=credentials['Access_Token']
access_token_secret=credentials['Acces_Token_Secret']


# Guardar el JSON de configuración
def save_config(data):
    with open('config.json', 'w') as file:
        json.dump(data, file, indent=4)

# Publicar el tweet (simulado aquí como un print)
def publish_tweet(tweet_text, client):
    response = client.create_tweet(text=tweet_text)
    print(f"Publishing tweet: {tweet_text}")

# Función principal para seleccionar y publicar un tweet
def main():
    # Cargar los tweets del archivo de configuración
    
    tweets = config['RandomPlaneTweets']
    
    # Filtrar los tweets no publicados
    unpublished_tweets = [tweet for tweet in tweets if tweet['published'] == 0]
    
    if not unpublished_tweets:
        print("No unpublished tweets available.")
        return

    # Seleccionar un tweet al azar
    tweet_to_publish = random.choice(unpublished_tweets)
    client =  apiConnectors.get_twitter_conn_v2(consumer_key=consumer_key, consumer_secret=consumer_secret,  
                                                access_token=access_token, access_token_secret=access_token_secret)
    # Publicar el tweet
    publish_tweet(tweet_to_publish['text'], client=client)
    
    # Marcar el tweet como publicado
    config['RandomPlaneTweets'][tweet_to_publish["id"]]["published"] = 1
    #tweet_to_publish['published'] = 1
    
    # Guardar los cambios en el archivo de configuración
    save_config(config)
    print(f"Tweet with ID {tweet_to_publish['id']} marked as published.")

if __name__ == "__main__":
    main()
