import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

def fetch_bid_ask_spread_data():
    """Fetch bid-ask spread data from the MySQL table."""
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            database='crypto_data',
            user='root',
            password='password'
        )

        if connection.is_connected():
            # Fetch bid-ask spread data
            query = "SELECT datetime, spread FROM bid_ask_spread ORDER BY datetime ASC"
            df_spread = pd.read_sql(query, connection)
            return df_spread

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection.is_connected():
            connection.close()

# Fetch bid-ask spread data for UNI
df_spread = fetch_bid_ask_spread_data()

if df_spread is not None:
    # Convert 'date' column to datetime
    df_spread['datetime'] = pd.to_datetime(df_spread['datetime'])
    
    # Plot the bid-ask spread data
    plt.figure(figsize=(14, 7))
    
    plt.plot(df_spread['datetime'], df_spread['spread'], label='UNI Bid-Ask Spread', color='green')
    
    plt.xlabel('Date')
    plt.ylabel('Bid-Ask Spread')
    plt.title('UNI Bid-Ask Spread Changes Over Time')
    plt.legend()
    plt.grid()
    plt.show()
