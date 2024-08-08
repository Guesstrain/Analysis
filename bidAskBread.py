import requests
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timezone
import schedule
import time

def get_current_utc_date():
    # Get the current date and time in UTC, accurate to the second
    now_utc = datetime.now(timezone.utc)
    return now_utc.strftime('%Y-%m-%d %H:%M:%S')

def get_bid_ask_spread(symbol='UNIUSDT'):
    # Define the Binance API endpoint for the ticker book
    url = f"https://api.binance.com/api/v3/ticker/bookTicker"
    params = {'symbol': symbol}

    # Make a request to the Binance API
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        print("data: ", data)
        bid_price = float(data['bidPrice'])
        ask_price = float(data['askPrice'])
        spread = ask_price - bid_price
        return bid_price, ask_price, spread
    else:
        return None, None, None

def insert_bid_ask_spread(bid_price, ask_price):
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            database='crypto_data',
            user='root',
            password='password'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            # SQL statement for inserting data
            insert_query = """
            INSERT INTO bid_ask_spread (datetime, bid_price, ask_price, spread)
            VALUES (%s, %s, %s, %s)
            """
            
            spread = ask_price - bid_price
            current_utc_datetime = get_current_utc_date()
            data = (current_utc_datetime, bid_price, ask_price, spread)
            cursor.execute(insert_query, data)
            
            # Commit the transaction
            connection.commit()
            print(f"Inserted record with datetime: {current_utc_datetime}, bid: {bid_price}, ask: {ask_price}, spread: {spread}.")
        
    except Error as e:
        print(f"Error: {e}")
        if connection.is_connected():
            cursor.close()
            connection.rollback()
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close() 

def fetch_and_store_bid_ask_spread():
    symbol = 'UNIUSDT'
    bid_price, ask_price, spread = get_bid_ask_spread(symbol)
    insert_bid_ask_spread(bid_price, ask_price)

fetch_and_store_bid_ask_spread()
schedule.every(10).minutes.do(fetch_and_store_bid_ask_spread)

print("Starting the scheduler...")

while True:
    schedule.run_pending()
    time.sleep(1)







