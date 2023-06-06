import pandas as pd
from nsepy import get_history

def buy_option_with_ATM_strike(symbol):
    # Fetch historical stock data from NSE
    print("inside the function")
    data = get_history(symbol=symbol, index='NIFTY', start=pd.to_datetime('2022-01-01'), end=pd.to_datetime('2023-06-01'))
    print(data)
    # Calculate 20-day simple moving average
    data['20sma'] = data['Close'].rolling(window=20).mean()

    # Check if strike price is above the 20-day SMA using high and low prices
    latest_price = data['Close'].iloc[-1]
    latest_high = data['High'].iloc[-1]
    latest_low = data['Low'].iloc[-1]
    latest_20sma = data['20sma'].iloc[-1]

    if latest_high > latest_20sma and latest_low > latest_20sma:
        print("Buy call option with ATM strike price")
    else:
        print("Do not buy call option with ATM strike price")

# Specify the stock symbol (e.g., NIFTY 50)
stock_symbol = 'NIFTY'
print("starting with function ")
# Call the function to check and buy the option
buy_option_with_ATM_strike(stock_symbol)