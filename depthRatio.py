import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# 1. Fetch Data from MySQL
def fetch_order_book_data():
    """Fetch bid and ask order data from the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='crypto_data',
            user='root',
            password='password'
        )
        
        if connection.is_connected():
            # Fetch the best bid and ask prices
            best_bid_query = "SELECT MAX(price) as price FROM bid_order_book"
            best_ask_query = "SELECT MIN(price) as price FROM ask_order_book"
            best_bid = pd.read_sql(best_bid_query, connection).iloc[0]['price']
            best_ask = pd.read_sql(best_ask_query, connection).iloc[0]['price']
            
            # Fetch all bid and ask data
            bid_query = "SELECT price, quantity FROM bid_order_book"
            ask_query = "SELECT price, quantity FROM ask_order_book"
            df_bids = pd.read_sql(bid_query, connection)
            df_asks = pd.read_sql(ask_query, connection)
            
            return best_bid, best_ask, df_bids, df_asks
    
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None, None, None, None
    finally:
        if connection.is_connected():
            connection.close()

# 2. Calculate Mid-Market Price
def calculate_mid_market_price(best_bid, best_ask):
    """Calculate the mid-market price."""
    return (best_bid + best_ask) / 2

# 3. Define Price Ranges and 4. Filter Orders
def calculate_depth_ratios(mid_market_price, df_bids, df_asks, percentage_ranges):
    """Calculate depth ratios for various percentage ranges around the mid-market price."""
    depth_ratios = []
    
    for pct in percentage_ranges:
        # Calculate the price range boundaries
        lower_bound = mid_market_price * (1 - pct)
        upper_bound = mid_market_price * (1 + pct)
        
        # Filter bid and ask orders within the range
        filtered_bids = df_bids[(df_bids['price'] >= lower_bound) & (df_bids['price'] <= upper_bound)]
        filtered_asks = df_asks[(df_asks['price'] >= lower_bound) & (df_asks['price'] <= upper_bound)]
        
        # Calculate total volume within the range
        total_bid_volume = filtered_bids['quantity'].sum()
        total_ask_volume = filtered_asks['quantity'].sum()
        
        # Calculate depth ratio
        if total_ask_volume == 0:
            depth_ratio = float('inf')
        else:
            depth_ratio = total_bid_volume / total_ask_volume
        
        depth_ratios.append(depth_ratio)
    
    return depth_ratios

# 6. Plot the Curve
def plot_depth_ratio_curve(percentage_ranges, depth_ratios):
    """Plot the depth ratio curve."""
    plt.figure(figsize=(10, 6))
    plt.plot(percentage_ranges, depth_ratios, marker='o', linestyle='-')
    plt.xlabel('Percentage Range Around Mid-Market Price')
    plt.ylabel('Depth Ratio')
    plt.title('Depth Ratio vs. Price Range')
    plt.grid(True)
    plt.show()

# Main function to run all steps
def main():
    # 1. Fetch the data
    best_bid, best_ask, df_bids, df_asks = fetch_order_book_data()
    
    if best_bid is not None and best_ask is not None:
        # 2. Calculate the mid-market price
        mid_market_price = calculate_mid_market_price(best_bid, best_ask)
        print("mid_market_price", mid_market_price)
        
        # 3. Define percentage ranges
        percentage_ranges = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0]
        
        # 4. Filter orders and 5. Calculate depth ratios
        depth_ratios = calculate_depth_ratios(mid_market_price, df_bids, df_asks, percentage_ranges)
        
        # 6. Plot the depth ratio curve
        plot_depth_ratio_curve(percentage_ranges, depth_ratios)
    else:
        print("Data not available.")

# Run the main function
main()