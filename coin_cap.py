import requests
import pandas as pd
import talib
import matplotlib.pyplot as plt
from datetime import datetime
import json

def load_json():
    # Load JSON data from file
    with open('your_file.json', 'r') as file:
        data = json.load(file)

    # Extract the Price dictionary
    price_data = data.get('Price', {})

    # Convert timestamp keys to datetime and create the date-risk dictionary
    date_risk_dict = {pd.to_datetime(timestamp, unit='s'): risk for timestamp, risk in price_data.items()}

    # Print the result
    # for date, risk in date_risk_dict.items():
    #     print(f"{date}: {risk}")

    return date_risk_dict


def days_until_current_date(target_date):
    # Convert the input date to a datetime object
    target_datetime = datetime.strptime(target_date, "%Y-%m-%d")

    # Get the current date
    current_datetime = datetime.now()

    # Calculate the difference in days
    days_difference = (current_datetime - target_datetime).days

    return days_difference

# Function to get historical Bitcoin prices from CoinGecko API
def get_historical_prices(days):
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
    params = {
        'vs_currency': 'eur',
        'days': days,
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
    ax1.set_yscale('log')  # Set y-axis scale to logarithmic
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel('RSI', color='tab:red')
    ax2.plot(prices['time'], prices['rsi'], color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    plt.title(f'Bitcoin Price and RSI Over the Last Year ({timeframe})')
    plt.show()

def simulate_trading(prices, from_date=None, until_date=None):
    # Filter prices based on the specified date range
    if from_date:
        prices = prices[prices['time'] >= pd.to_datetime(from_date)]
    if until_date:
        prices = prices[prices['time'] <= pd.to_datetime(until_date)]

    capital = 0
    holding = 0  # Initial holding in BTC
    invested_amount = 0  # Track the total fiat money used to buy BTC
    rsi_buy_threshold = 80
    rsi_sell_threshold = 85
    base_buy_amount = 1500  # Base amount to buy in fiat currency
    buy_count = 0

    # Track the last month to determine when to buy
    last_month = None

    for index, row in prices.iterrows():
        current_month = row['time'].month

        # Adjust buy amount based on RSI
        rsi_adjusted_buy_amount = base_buy_amount * (1 - row['rsi'] / 100)

        # Buy BTC every month when RSI is under the threshold and it's a new month
        if row['rsi'] <= rsi_buy_threshold and current_month != last_month:
            # Buy BTC
            btc_bought = rsi_adjusted_buy_amount / row['price']
            holding += btc_bought
            invested_amount += rsi_adjusted_buy_amount
            buy_count += 1
            print(f"Buy {rsi_adjusted_buy_amount:.2f} EUR of BTC at {row['time']} - RSI: {row['rsi']}, Price: {row['price']}, Holding: {holding}")

        elif row['rsi'] >= rsi_sell_threshold and holding > 0:
            # Sell all BTC
            capital += holding * row['price']
            holding = 0
            print(f"Sell BTC at {row['time']} - RSI: {row['rsi']}, Price: {row['price']}, Capital: {capital}")

        last_month = current_month

    # If still holding at the end, sell
    if holding > 0:
        capital += holding * prices.iloc[-1]['price']
        print(f"Sell remaining BTC at {prices.iloc[-1]['time']} - Price: {prices.iloc[-1]['price']}, Capital: {capital}")

    # Calculate the investment return
    investment_return = (capital + holding * prices.iloc[-1]['price'] - invested_amount) / invested_amount * 100

    print(f"Invested: {invested_amount}")
    print(f"Investment Return: {investment_return:.2f}%")
    print(f"Number of buys: {buy_count}")

    return capital


def main():
    target_date = "2014-01-01"
    days = days_until_current_date(target_date)

    # Get historical Bitcoin prices
    bitcoin_prices = get_historical_prices(days)

    # Convert to weekly prices
    timeframe = 'M'  # You can change this to 'M' for monthly, 'D' for daily, etc.
    bitcoin_prices_timeframe = convert_to_timeframe(bitcoin_prices, timeframe)

    # Calculate RSI
    bitcoin_prices_timeframe = calculate_rsi(bitcoin_prices_timeframe)

    from_date = '2020-05-01'
    until_date = '2021-02-28'

    # Simulate trading
    final_capital = simulate_trading(bitcoin_prices_timeframe, from_date, until_date)
    print(f"Final capital after simulation: {final_capital} EUR")

    # from_date = '2014-01-01'
    # until_date = '2018-02-02'

    # # Simulate trading
    # final_capital = simulate_trading(bitcoin_prices_timeframe, from_date, until_date)
    # print(f"Final capital after simulation: {final_capital} EUR")

    # Plot data
    # plot_data(bitcoin_prices_timeframe, timeframe)

    print("Done.")

if __name__ == "__main__":
    main()

