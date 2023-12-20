import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def get_historical_prices(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data['Close']

if __name__ == "__main__":
    # Define the S&P 500 ticker symbol (^GSPC)
    sp500_ticker = "^GSPC"

    # Define the date range for historical data (set start_date to a date far in the past)
    start_date = "2020-01-01"
    end_date = pd.to_datetime("today").strftime("%Y-%m-%d")

    # Get historical prices for S&P 500
    sp500_prices = get_historical_prices(sp500_ticker, start_date, end_date)

    # Plot the historical data with logarithmic scale on the y-axis
    plt.figure(figsize=(10, 6))
    plt.semilogy(sp500_prices.index, sp500_prices, label='S&P 500 Index')
    plt.title('Historical Prices for S&P 500 Index (Logarithmic Scale)')
    plt.xlabel('Date')
    plt.ylabel('Closing Price (Log Scale)')
    plt.legend()
    plt.show()
