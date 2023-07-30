import ccxt

# Replace 'YOUR_API_KEY' and 'YOUR_SECRET_KEY' with your actual KuCoin Futures API credentials
api_key = 'YOUR_API_KEY'
secret_key = 'YOUR_SECRET_KEY'

# Create the KuCoin Futures exchange object
exchange = ccxt.kucoin({
    'apiKey': api_key,
    'secret': secret_key,
    'password': 'YOUR_API_PASSWORD',  # Replace with your API password
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future',
    },
})

def martingale_strategy(pair, initial_position_size, max_trades):
    position_size = initial_position_size
    current_trades = 0

    while current_trades < max_trades:
        try:
            # Fetch the latest ticker data
            ticker = exchange.fetch_ticker(pair)

            # Check the current price
            current_price = ticker['ask']  # Use 'bid' for short selling

            # Calculate the order amount and create the order
            order_amount = position_size * (2 ** current_trades)
            order = exchange.create_market_buy_order(pair, order_amount)

            print(f"Trade {current_trades + 1} - Bought {order_amount} BTC at {current_price}")

            # Reset trades counter on successful trade
            current_trades = 0
        except ccxt.InsufficientFunds:
            # If there are not enough funds, exit the loop
            print("Insufficient funds for the trade.")
            break
        except Exception as e:
            # Handle other exceptions
            print(f"An error occurred: {str(e)}")

            # Increment the trades counter on a losing trade
            current_trades += 1

    print("Martingale strategy execution complete.")

# Replace 'BTC/USDT' with your desired trading pair and set the initial position size and max trades
martingale_strategy('BTC/USDT', initial_position_size=0.001, max_trades=5)
