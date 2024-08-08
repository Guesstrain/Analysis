import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

def prepare_heatmap_data(df_bids, df_asks):
    """Prepare data for heatmap visualization."""
    # Merge bid and ask data with an indicator column
    df_bids['type'] = 'bid'
    df_asks['type'] = 'ask'
    
    df_orders = pd.concat([df_bids, df_asks])

    # Pivot the table to have price levels as index and 'bid'/'ask' as columns
    df_pivot = df_orders.pivot_table(index='price', columns='type', values='quantity', fill_value=0)

    # If there are missing columns, fill them with zeros
    if 'bid' not in df_pivot:
        df_pivot['bid'] = 0
    if 'ask' not in df_pivot:
        df_pivot['ask'] = 0

    return df_pivot

def plot_order_book_heatmap(df_pivot):
    """Plot heatmap for the order book."""
    plt.figure(figsize=(12, 8))

    # Plot heatmap with bid and ask columns
    sns.heatmap(df_pivot.T, cmap='viridis', cbar_kws={'label': 'Order Quantity'})

    plt.title('Order Book Heatmap for UNI/USDT')
    plt.xlabel('Price')
    plt.ylabel('Order Type')
    plt.show()

df_bids, df_asks = fetch_data_from_db()

if df_bids is not None and df_asks is not None:
    # Prepare the data for plotting
    df_pivot = prepare_heatmap_data(df_bids, df_asks)

    # Plot
    plot_order_book_heatmap(df_pivot)
else:
    print("No data available.")