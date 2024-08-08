import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to the MySQL database
def fetch_data_from_db():
    """Fetch bid and ask order data from the MySQL database."""
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            database='crypto_data',
            user='root',
            password='password'
        )

        if connection.is_connected():
            # Fetch bids data
            bid_query = "SELECT price, quantity FROM bid_order_book ORDER BY price DESC"
            df_bids = pd.read_sql(bid_query, connection)

            # Fetch asks data
            ask_query = "SELECT price, quantity FROM ask_order_book ORDER BY price ASC"
            df_asks = pd.read_sql(ask_query, connection)

            return df_bids, df_asks

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None, None
    finally:
        if connection.is_connected():
            connection.close()

def prepare_depth_chart_data(df_bids, df_asks):
    """Prepare data for plotting the depth chart."""
    # Calculate cumulative quantity for bids
    df_bids['cumulative_quantity'] = df_bids['quantity'].cumsum()

    # Calculate cumulative quantity for asks
    df_asks['cumulative_quantity'] = df_asks['quantity'].cumsum()

    return df_bids, df_asks

def plot_depth_chart(df_bids, df_asks):
    """Plot the depth chart using bid and ask data."""
    plt.figure(figsize=(10, 6))

    # Plot bid data
    plt.plot(df_bids['price'], df_bids['cumulative_quantity'], color='green', label='Bids')

    # Plot ask data
    plt.plot(df_asks['price'], df_asks['cumulative_quantity'], color='red', label='Asks')

    plt.xlabel('Price (USD)')
    plt.ylabel('Cumulative Quantity')
    plt.title('Order Book Depth Chart for UNI/USDT')
    plt.legend()
    plt.grid(True)
    plt.show()


# Fetch bid and ask data from the database
df_bids, df_asks = fetch_data_from_db()

if df_bids is not None and df_asks is not None:
    # Prepare the data for plotting
    df_bids, df_asks = prepare_depth_chart_data(df_bids, df_asks)

    # Plot the depth chart
    plot_depth_chart(df_bids, df_asks)
else:
    print("No data available.")
