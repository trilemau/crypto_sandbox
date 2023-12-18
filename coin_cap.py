import requests
import pandas as pd
import talib
import matplotlib.pyplot as plt

# Function to get historical Bitcoin prices from CoinGecko API
def get_historical_prices():
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
    params = {
        'vs_currency': 'eur',
        'days': '3500',
        'interval': 'daily',  # Change to daily interval
    }

    response = requests.get(url, params=params)
    data = response.json()

    prices = pd.DataFrame(data['prices'], columns=['time', 'price'])
    prices['time'] = pd.to_datetime(prices['time'], unit='ms')
    return prices

# Function to convert prices to the specified timeframe
def convert_to_timeframe(prices, timeframe='W'):
    prices.set_index('time', inplace=True)
    resampled_prices = prices.resample(timeframe).last()
    return resampled_prices.reset_index()

# Function to calculate RSI using TA-Lib
def calculate_rsi(prices, period=14):
    prices['rsi'] = talib.RSI(prices['price'], timeperiod=period)
    return prices

# Function to plot Bitcoin prices and RSI
def plot_data(prices, timeframe):
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot Bitcoin prices
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Bitcoin Price (EUR)', color='tab:blue')
    ax1.plot(prices['time'], prices['price'], color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel('RSI', color='tab:red')
    ax2.plot(prices['time'], prices['rsi'], color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    plt.title(f'Bitcoin Price and RSI Over the Last Year ({timeframe})')
    plt.show()

def main():
    # Get historical Bitcoin prices
    bitcoin_prices = get_historical_prices()

    # Convert to weekly prices
    timeframe = 'M'  # You can change this to 'M' for monthly, 'D' for daily, etc.
    bitcoin_prices_timeframe = convert_to_timeframe(bitcoin_prices, timeframe)

    # Calculate RSI
    bitcoin_prices_timeframe = calculate_rsi(bitcoin_prices_timeframe)

    # Plot data
    plot_data(bitcoin_prices_timeframe, timeframe)

    print("Done.")

if __name__ == "__main__":
    main()
