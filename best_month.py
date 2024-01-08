import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def get_historical_prices(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data['Close']

def simulate_investment_strategy(prices, monthly_contribution):
    capital = 0
    holding = 0
    investments = []

    for index, row in prices.iterrows():
        # Make a monthly contribution
        capital += monthly_contribution

        # Buy as much of the S&P 500 as possible
        bought_units = capital / row['Close']
        holding += bought_units
        capital = 0

        # Record the investment at the end of each month
        investments.append({'Date': row.name, 'Holding': holding, 'Capital': capital})

    return investments

if __name__ == "__main__":
    # Define the S&P 500 ticker symbol (^GSPC)
    sp500_ticker = "^GSPC"

    # Define the date range for historical data
    start_date = "2020-01-01"
    end_date = pd.to_datetime("today").strftime("%Y-%m-%d")

    # Get historical prices for S&P 500
    sp500_prices = get_historical_prices(sp500_ticker, start_date, end_date)

    # Simulate investment strategy with a monthly contribution of 500 euros
    monthly_contribution = 500
    investments = simulate_investment_strategy(sp500_prices, monthly_contribution)

    # Convert the investment data to a DataFrame for analysis
    investment_df = pd.DataFrame(investments)
    investment_df.set_index('Date', inplace=True)

    # Plot the investment strategy results
    plt.figure(figsize=(10, 6))
    plt.plot(investment_df.index, investment_df['Holding'], label='Holding')
    plt.title('Investment Strategy with Monthly Contributions')
    plt.xlabel('Date')
    plt.ylabel('Investment Value (EUR)')
    plt.legend()
    plt.show()
