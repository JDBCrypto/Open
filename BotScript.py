import requests
import time
from telegram import Bot

# Your Telegram bot token
TOKEN = 'Popcat token listing'
CHAT_ID = 'JBNewExchangeListings'  # Your Telegram chat ID or group ID
COIN_ID = 'popcat'  # CoinGecko ID for the coin you're interested in

# Initialize the Telegram bot
bot = Bot(token=TOKEN)

# Function to check for new listings
def check_new_listings():
    url = f"https://api.coingecko.com/api/v3/coins/{COIN_ID}"
    response = requests.get(url).json()
    
    # Parse the exchanges where the coin is listed
    exchanges = response['tickers']
    exchange_names = set(ticker['market']['name'] for ticker in exchanges)
    
    return exchange_names

# Function to send notification
def send_notification(message):
    bot.send_message(chat_id=CHAT_ID, text=message)

# Main loop to monitor the listings
def main():
    previous_exchanges = check_new_listings()
    
    while True:
        current_exchanges = check_new_listings()
        
        # Check for new exchanges
        new_exchanges = current_exchanges - previous_exchanges
        
        if new_exchanges:
            for exchange in new_exchanges:
                message = f"{COIN_ID.capitalize()} is now listed on {exchange}!"
                send_notification(message)
                
        previous_exchanges = current_exchanges
        
        # Wait before checking again
        time.sleep(3600)  # Check every hour

if __name__ == '__main__':
    main()
