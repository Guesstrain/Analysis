import mysql.connector
import requests
import pandas as pd
import datetime

def fetch_uni_historical_prices(days=30):
    """Fetch historical price data for UNI."""
    url = "https://api.coingecko.com/api/v3/coins/uniswap/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': days
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        prices = data['prices']
        price_data = [(datetime.datetime.fromtimestamp(price[0] / 1000), price[1]) for price in prices]
        return price_data
    else:
        print(f"Error fetching data: {response.status_code}")
        return []

def store_prices_in_db(price_data):
    """Store price data in MySQL database."""
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
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS uni_price (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    date DATETIME,
                    price FLOAT
                )
            """)

            # Insert data into the table
            for date, price in price_data:
                cursor.execute("INSERT INTO uni_price (date, price) VALUES (%s, %s)", (date, price))
            
            connection.commit()
            print("Data inserted successfully.")

    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Fetch the past 30 days of price data for UNI
uni_price_data = fetch_uni_historical_prices(30)

# Store the data in the database
store_prices_in_db(uni_price_data)
