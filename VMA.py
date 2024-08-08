import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
import numpy as np

def fetch_volume_data():
    """Fetch volume data from the MySQL database."""
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            database='crypto_data',
            user='root',
            password='password'
        )

        if connection.is_connected():
            # Fetch volume data
            query = "SELECT date, volume FROM uni_volume ORDER BY date ASC"
            df_volume = pd.read_sql(query, connection)
            return df_volume

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection.is_connected():
            connection.close()

# Fetch the volume data
df_volume = fetch_volume_data()

def calculate_volume_moving_average(df_volume, window_size):
    """Calculate the volume moving average."""
    df_volume['VMA'] = df_volume['volume'].rolling(window=window_size).mean()
    return df_volume

# Define the window size (e.g., 5 days, 10 days, 20 days)
window_size = 10

# Calculate the Volume Moving Average
df_volume = calculate_volume_moving_average(df_volume, window_size)

def find_turning_points(df_volume):
    """Find turning points (local maxima and minima) in the volume data."""
    # Calculate first derivative
    df_volume['diff'] = np.sign(df_volume['volume'].diff())

    # Find turning points (where diff changes sign)
    turning_points = df_volume[(df_volume['diff'].shift(-1) != df_volume['diff']) & (df_volume['diff'] != 0)]

    # Extract dates and volumes of turning points
    dates = turning_points['date']
    volumes = turning_points['volume']

    return dates, volumes

dates, volumes = find_turning_points(df_volume)

def plot_turning_points(df_volume, dates, volumes):
    """Plot the volume data and highlight the turning points."""
    plt.figure(figsize=(12, 6))
    plt.plot(df_volume['date'], df_volume['volume'], label='Volume')
    plt.scatter(dates, volumes, color='red', label='Turning Points')
    
    for date, volume in zip(dates, volumes):
        plt.text(date, volume, date.strftime('%Y-%m-%d'), fontsize=8, ha='left')

    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.title('UNI Trading Volume with Turning Points')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Plot the volume data and turning points
plot_turning_points(df_volume, dates, volumes)
