import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

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

def smooth_data(df_volume, window_size=5):
    """Smooth the volume data using a moving average."""
    df_volume['smoothed_volume'] = df_volume['volume'].rolling(window=window_size).mean()
    return df_volume

df_volume = smooth_data(df_volume)

def find_prominent_turning_points(df_volume, prominence=1e6):
    """Find prominent turning points using volume data."""
    # Use smoothed volume data to find peaks
    volumes = df_volume['smoothed_volume'].dropna().values
    indices, properties = find_peaks(volumes, prominence=prominence)

    # Extract dates and volumes for these peaks
    turning_points = df_volume.iloc[indices]
    dates = turning_points['date']
    volumes = turning_points['volume']
    print("dates: ", dates)
    return dates, volumes

def plot_prominent_turning_points(df_volume, dates, volumes):
    """Plot volume data and highlight prominent turning points."""
    plt.figure(figsize=(12, 6))
    plt.plot(df_volume['date'], df_volume['volume'], label='Volume', alpha=0.5)
    plt.plot(df_volume['date'], df_volume['smoothed_volume'], label='Smoothed Volume', color='orange', alpha=0.8)
    plt.scatter(dates, volumes, color='red', label='Prominent Turning Points')
    
    for date, volume in zip(dates, volumes):
        plt.text(date, volume, date.strftime('%Y-%m-%d'), fontsize=8, ha='left')

    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.title('UNI Trading Volume with Prominent Turning Points')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Smooth the data
df_volume = smooth_data(df_volume)

# Find prominent turning points
prominence = 1e6  # Adjust this value based on your data's scale
dates, volumes = find_prominent_turning_points(df_volume, prominence)

# Plot the data with prominent turning points
plot_prominent_turning_points(df_volume, dates, volumes)


