import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

def fetch_trading_volume_data():
    """Fetch trading volume data from the MySQL database."""
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            database='crypto_data',
            user='root',
            password='password'
        )

        if connection.is_connected():
            # Fetch trading volume data
            query = "SELECT date, volume FROM uni_volume"
            df_volume = pd.read_sql(query, connection)
            return df_volume

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection.is_connected():
            connection.close()

# Fetch trading volume data
df_volume = fetch_trading_volume_data()

# Convert the date column to datetime format
df_volume['date'] = pd.to_datetime(df_volume['date'])

# Ensure volume is a numeric column
df_volume['volume'] = pd.to_numeric(df_volume['volume'])

def plot_trading_volume(df_volume):
    """Plot the trading volume data."""
    plt.figure(figsize=(12, 6))
    plt.plot(df_volume['date'], df_volume['volume'], marker='o', linestyle='-')

    plt.xlabel('Time')
    plt.ylabel('Trading Volume')
    plt.title('UNI Trading Volume Over Time')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Plot the trading volume data
plot_trading_volume(df_volume)