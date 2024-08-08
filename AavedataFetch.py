import requests
import mysql.connector
import pandas as pd
import datetime

def fetch_aave_data(days=30):
    """Fetch past 30 days of trading volume and price data for AAVE."""
    url = "https://api.coingecko.com/api/v3/coins/aave/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': days
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def process_data(data):
    """Process price and volume data into lists."""
    # Extract price and volume data
    prices = data['prices']
    volumes = data['total_volumes']
    
    # Convert timestamps to datetime and store in lists
    price_data = [(datetime.datetime.fromtimestamp(price[0] / 1000), price[1]) for price in prices]
    volume_data = [(datetime.datetime.fromtimestamp(volume[0] / 1000), volume[1]) for volume in volumes]
    return price_data, volume_data

def store_data_to_mysql(price_data, volume_data):
    """Store the processed data into MySQL tables."""
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

            # Create tables if they don't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS aave_price (
                    date DATETIME PRIMARY KEY,
                    price FLOAT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS aave_volume (
                    date DATETIME PRIMARY KEY,
                    volume FLOAT
                )
            """)

            # Insert price data
            price_insert_query = "REPLACE INTO aave_price (date, price) VALUES (%s, %s)"
            cursor.executemany(price_insert_query, price_data)

            # Insert volume data
            volume_insert_query = "REPLACE INTO aave_volume (date, volume) VALUES (%s, %s)"
            cursor.executemany(volume_insert_query, volume_data)

            # Commit the transaction
            connection.commit()

    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Fetch Aave data for the past 30 days
data = fetch_aave_data(30)

if data:
    # Process the data
    price_data, volume_data = process_data(data)
    
    # Store data to MySQL database
    store_data_to_mysql(price_data, volume_data)
