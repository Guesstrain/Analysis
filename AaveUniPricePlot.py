import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

def fetch_price_data(table_name):
    """Fetch price data from the specified MySQL table."""
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            database='crypto_data',
            user='root',
            password='password'
        )

        if connection.is_connected():
            # Fetch price data from the specified table
            query = f"SELECT date, price FROM {table_name} ORDER BY date ASC"
            df_price = pd.read_sql(query, connection)
            return df_price

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection.is_connected():
            connection.close()

# Fetch price data for UNI and AAVE
df_uni_price = fetch_price_data('uni_price')
df_aave_price = fetch_price_data('aave_price')

if df_uni_price is not None and df_aave_price is not None:
    # Convert 'date' columns to datetime
    df_uni_price['date'] = pd.to_datetime(df_uni_price['date'])
    df_aave_price['date'] = pd.to_datetime(df_aave_price['date'])
    
    # Scale UNI prices for trend comparison (e.g., scale by 18 times)
    scaling_factor = 13
    df_uni_price['scaled_price'] = df_uni_price['price'] * scaling_factor
    
    # Plot the price data
    plt.figure(figsize=(14, 7))
    
    plt.plot(df_aave_price['date'], df_aave_price['price'], label='AAVE Price (USD)', color='blue')
    plt.plot(df_uni_price['date'], df_uni_price['scaled_price'], label=f'Scaled UNI Price (x{scaling_factor})', color='orange')
    
    plt.xlabel('Date')
    plt.ylabel('Price (USD) and Scaled UNI')
    plt.title('UNI vs AAVE Price Trend Comparison')
    plt.legend()
    plt.grid()
    plt.show()
