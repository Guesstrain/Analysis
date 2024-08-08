# Example order book data (price, volume)
bids = [[9.8, 300], [9.7, 200], [9.6, 100]]
asks = [[10.2, 400], [10.3, 300], [10.4, 200]]

# Calculate the mid-market price
best_bid_price = bids[0][0]
best_ask_price = asks[0][0]
mid_market_price = (best_bid_price + best_ask_price) / 2

# Define the percentage range (e.g., ±1%)
percentage_range = 0.03

# Determine the price limits
lower_bound = mid_market_price * (1 - percentage_range)
upper_bound = mid_market_price * (1 + percentage_range)

# Calculate cumulative buy volume (within the lower range)
cumulative_buy_volume = sum(volume for price, volume in bids if price >= lower_bound)

# Calculate cumulative sell volume (within the upper range)
cumulative_sell_volume = sum(volume for price, volume in asks if price <= upper_bound)

# Calculate the depth ratio
if cumulative_sell_volume > 0:  # To avoid division by zero
    depth_ratio = cumulative_buy_volume / cumulative_sell_volume
else:
    depth_ratio = float('inf')  # Indicating no sell orders within the range

print(f"Mid-Market Price: {mid_market_price}")
print(f"Lower Bound: {lower_bound}, Upper Bound: {upper_bound}")
print(f"Cumulative Buy Volume: {cumulative_buy_volume}")
print(f"Cumulative Sell Volume: {cumulative_sell_volume}")
print(f"Depth Ratio: {depth_ratio}")