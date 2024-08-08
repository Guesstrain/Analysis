import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

def fetch_price_data():
    """Fetch price data from the MySQL database."""
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            database='crypto_data',
            user='root',
            password='password'
        )

        if connection.is_connected():
            # Fetch price datas
            query = "SELECT date, price FROM uni_price ORDER BY date ASC"
            df_price = pd.read_sql(query, connection)
            return df_price

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection.is_connected():
            connection.close()

def plot_price_data(df_price):
    """Plot price data over time."""
    plt.figure(figsize=(12, 6))
    plt.plot(df_price['date'], df_price['price'], label='UNI Price', color='blue')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.title('UNI Price Over Time')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Fetch the price data
df_price = fetch_price_data()


if df_price is not None:
    # Convert 'date' column to datetime if not already
    df_price['date'] = pd.to_datetime(df_price['date'])

    # Calculate mean, median, and mode
    mean_price = df_price['price'].mean()
    median_price = df_price['price'].median()
    
    # Calculating mode for a continuous variable might not be very meaningful, but can still be computed
    mode_price = df_price['price'].mode()

    print(f"Mean Price: {mean_price}")
    print(f"Median Price: {median_price}")
    if not mode_price.empty:
        print(f"Mode Price(s): {mode_price.tolist()}")

    # Calculate Range
    min_price = df_price['price'].min()
    max_price = df_price['price'].max()
    price_range = max_price - min_price
    
    # Calculate Variance
    variance = df_price['price'].var()
    
    # Calculate Standard Deviation
    std_deviation = df_price['price'].std()

    print(f"Price Range: {price_range}")
    print(f"Variance: {variance}")
    print(f"Standard Deviation: {std_deviation}")
    
    # Plot the price data
    plot_price_data(df_price)
