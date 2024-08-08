import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

def fetch_data_from_table(table_name):
    """Fetch data from the specified MySQL table."""
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            database='crypto_data',
            user='root',
            password='password'
        )

        if connection.is_connected():
            # Fetch data from the specified table
            query = f"SELECT date, volume FROM {table_name} ORDER BY date ASC"
            df_data = pd.read_sql(query, connection)
            return df_data

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection.is_connected():
            connection.close()

# Fetch trading volume data for UNI and AAVE
df_uni_volume = fetch_data_from_table('uni_volume')
df_aave_volume = fetch_data_from_table('aave_volume')

if df_uni_volume is not None and df_aave_volume is not None:
    # Convert 'date' columns to datetime
    df_uni_volume['date'] = pd.to_datetime(df_uni_volume['date'])
    df_aave_volume['date'] = pd.to_datetime(df_aave_volume['date'])
    
    # Plot the trading volume data
    plt.figure(figsize=(14, 7))
    
    plt.plot(df_uni_volume['date'], df_uni_volume['volume'], label='UNI Volume', color='blue')
    plt.plot(df_aave_volume['date'], df_aave_volume['volume'], label='AAVE Volume', color='orange')
    
    plt.xlabel('Date')
    plt.ylabel('Trading Volume')
    plt.title('UNI vs AAVE Trading Volume Over Time')
    plt.legend()
    plt.grid()
    plt.show()
