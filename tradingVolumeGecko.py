import requests
import pandas as pd
import datetime
import mysql.connector
from mysql.connector import Error

def get_uni_historical_volume(days=30):
    # Define the endpoint and parameters
    url = f"https://api.coingecko.com/api/v3/coins/uniswap/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': days
    }

    # Make a request to the CoinGecko API
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Extract the trading volume data (total_volumes)
        volumes = data['total_volumes']
        # Convert the timestamps to readable dates and store the volumes
        volume_data = [(datetime.datetime.fromtimestamp(vol[0] / 1000), vol[1]) for vol in volumes]
        return volume_data
    else:
        return f"Error: {response.status_code}"

def insert_volume_data(volume_data):
    """Insert the fetched volume data into the MySQL database."""
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
            INSERT INTO uni_volume (date, volume)
            VALUES (%s, %s)
            """
            
            # Insert each record into the database
            for record in volume_data:
                date, volume = record
                cursor.execute(insert_query, (date, volume))
            
            # Commit the transaction
            connection.commit()
            print(f"Inserted {cursor.rowcount} rows into the database.")

    except Error as e:
        print(f"Error: {e}")
        if connection.is_connected():
            connection.rollback()
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Fetch the past 30 days of trading volume for UNI
uni_volume_data = get_uni_historical_volume(30)

if uni_volume_data:
    insert_volume_data(uni_volume_data)

# Convert the data to a DataFrame for easy manipulation and display
df = pd.DataFrame(uni_volume_data, columns=['Date', 'Volume'])
print(df)