import requests
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timezone

def get_current_utc_datetime():
    """Get the current date and time in UTC, accurate to the second."""
    now_utc = datetime.now(timezone.utc)
    return now_utc.strftime('%Y-%m-%d %H:%M:%S')

def get_order_book(symbol):
    url = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=10000"
    response = requests.get(url)
    order_book = response.json()
    return order_book

def insert_bid_order_book(symbol, bids, timestamp):
    """Insert bid order book data into the MySQL database."""
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
            # SQL statement for inserting data into bid_order_book table
            insert_query = """
            INSERT INTO bid_order_book (symbol, price, quantity, timestamp)
            VALUES (%s, %s, %s, %s)
            """

            # Insert each bid into the database
            for bid in bids:
                price, quantity = map(float, bid)
                data = (symbol, price, quantity, timestamp)
                cursor.execute(insert_query, data)

            # Commit the transaction
            connection.commit()
            print(f"Inserted {cursor.rowcount} bid rows into the database for {symbol} order book.")

    except Error as e:
        print(f"Error: {e}")
        if connection.is_connected():
            connection.rollback()
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def insert_ask_order_book(symbol, asks, timestamp):
    """Insert ask order book data into the MySQL database."""
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
            # SQL statement for inserting data into ask_order_book table
            insert_query = """
            INSERT INTO ask_order_book (symbol, price, quantity, timestamp)
            VALUES (%s, %s, %s, %s)
            """

            # Insert each ask into the database
            for ask in asks:
                price, quantity = map(float, ask)
                data = (symbol, price, quantity, timestamp)
                cursor.execute(insert_query, data)

            # Commit the transaction
            connection.commit()
            print(f"Inserted {cursor.rowcount} ask rows into the database for {symbol} order book.")
    except Error as e:
        print(f"Error: {e}")
        if connection.is_connected():
            connection.rollback()
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Example: Fetching order book for BTC/USDT
symbol = "UNIUSDT"
order_book_data = get_order_book(symbol)
current_utc_datetime = get_current_utc_datetime()

insert_bid_order_book(symbol, order_book_data.get('bids', []), current_utc_datetime)
insert_ask_order_book(symbol, order_book_data.get('asks', []), current_utc_datetime)

