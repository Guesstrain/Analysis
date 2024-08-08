import mysql.connector
import pandas as pd

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
            # Fetch bid and ask data
            bid_query = "SELECT price, quantity FROM bid_order_book ORDER BY price DESC"
            ask_query = "SELECT price, quantity FROM ask_order_book ORDER BY price ASC"
            df_bids = pd.read_sql(bid_query, connection)
            df_asks = pd.read_sql(ask_query, connection)
            
            return df_bids, df_asks
    
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None, None
    finally:
        if connection.is_connected():
            connection.close()

def calculate_mid_market_price(best_bid, best_ask):
    """Calculate the mid-market price."""
    return (best_bid + best_ask) / 2

def calculate_slippage(df_bids, df_asks, order_sizes):
    """Calculate slippage and weighted average price for different order sizes."""
    results = []
    best_bid = df_bids.iloc[0]['price']
    best_ask = df_asks.iloc[0]['price']
    mid_market_price = calculate_mid_market_price(best_bid, best_ask)
    
    for order_size in order_sizes:
        # Calculate weighted average execution price for buying
        remaining_quantity = order_size
        total_cost = 0
        for _, row in df_asks.iterrows():
            if remaining_quantity <= 0:
                break
            available_quantity = row['quantity']
            trade_quantity = min(remaining_quantity, available_quantity)
            total_cost += trade_quantity * row['price']
            remaining_quantity -= trade_quantity
        
        weighted_avg_buy_price = total_cost / order_size
        buy_slippage = (weighted_avg_buy_price - mid_market_price) / mid_market_price * 100
        
        # Calculate weighted average execution price for selling
        remaining_quantity = order_size
        total_revenue = 0
        for _, row in df_bids.iterrows():
            if remaining_quantity <= 0:
                break
            available_quantity = row['quantity']
            trade_quantity = min(remaining_quantity, available_quantity)
            total_revenue += trade_quantity * row['price']
            remaining_quantity -= trade_quantity
        
        weighted_avg_sell_price = total_revenue / order_size
        sell_slippage = (mid_market_price - weighted_avg_sell_price) / mid_market_price * 100
        
        # Store results
        results.append({
            'Order Size': order_size,
            'Weighted Avg Buy Price': weighted_avg_buy_price,
            'Buy Slippage (%)': buy_slippage,
            'Weighted Avg Sell Price': weighted_avg_sell_price,
            'Sell Slippage (%)': sell_slippage
        })
    
    return results

# Main function to run the calculations
def main():
    # 1. Fetch the order book data
    df_bids, df_asks = fetch_order_book_data()
    
    if df_bids is not None and df_asks is not None:
        # 2. Define the order sizes
        order_sizes = [1000, 10000, 100000]
        
        # 3. Calculate slippage and weighted average prices for each order size
        slippage_results = calculate_slippage(df_bids, df_asks, order_sizes)
        
        # 4. Print the results
        for result in slippage_results:
            print(f"Order Size: {result['Order Size']}")
            print(f"  Weighted Avg Buy Price: {result['Weighted Avg Buy Price']}")
            print(f"  Buy Slippage: {result['Buy Slippage (%)']:.2f}%")
            print(f"  Weighted Avg Sell Price: {result['Weighted Avg Sell Price']}")
            print(f"  Sell Slippage: {result['Sell Slippage (%)']:.2f}%\n")
    else:
        print("Failed to fetch order book data.")

# Run the main function
if __name__ == "__main__":
    main()