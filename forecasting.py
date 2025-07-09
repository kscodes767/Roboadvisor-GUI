import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import yfinance as yf
from statsmodels.tsa.stattools import adfuller

def plotSMA(ticker):

    try: 
        window = int(input("Enter window size for SMA: ").strip())
        data = ticker.history(period = '1mo')
        close = data['Close']

        sma = close.rolling(window = window).mean()


        plt.figure(figsize = (10,5))
        plt.plot(close, label = "Actual Price")
        plt.plot(sma, label=f"{window}-Day SMA", linestyle = "--")
        plt.legend()
        plt.grid(True)
        plt.xlabel("Day")
        plt.ylabel("Price")
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Error generating SMA plot: {e}")

    
def plotEMA(ticker):
    try: 
        window = int(input("Enter window size for EMA: ").strip())
        data = ticker.history(period = '1mo')
        close = data['Close']

        ema = close.ewm(span = window).mean()
        plt.figure(figsize = (10,5))
        plt.plot(close, label = "Actual Price")
        plt.plot(ema, label=f"{window}-Day EMA", linestyle = "--")
        plt.legend()
        plt.grid(True)
        plt.xlabel("Day")
        plt.ylabel("Price")
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Error generating EMA plot: {e}")

def futurePrice(ticker):
    try:
        daysAhead = int(input("Enter number of days ahead to forecast: ").strip())
    except Exception as e:
        print("Invalid input, defaulting days ahead as 7")
        daysAhead = 7
    data = ticker.history(period = '1mo')['Close'].dropna()
    data = data[-90:]
    data=data.reset_index()

    data['Day'] = np.arange(len(data))
    X = data[['Day']]
    y = data['Close']

    model = LinearRegression()
    model.fit(X, y)

    futureDays = np.arange(len(data), len(data) + daysAhead).reshape(-1,1)
    futurePreds = model.predict(futureDays)

    lastDate = data['Date'].iloc[-1]
    futureDates = pd.date_range(start = lastDate + pd.Timedelta(days = 1), periods = daysAhead)

    plt.figure(figsize = (10,5))
    plt.plot(data['Date'], y, label="Historical")
    plt.plot(futureDates, futurePreds, linestyle = '--', color = 'orange', label = 'Forecast')
    plt.title(f"Stock Price Forecast for: {ticker.ticker}")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plotARIMA(ticker):
    data = ticker.history(period = "6mo")['Close'].dropna()
    data.index = pd.to_datetime(data.index)

    data.index = pd.to_datetime(data.index)
    data = data.asfreq('B') 

    # Plot original series

    plt.figure(figsize=(12,4))
    plt.plot(data, label = "Original Data")
    plt.title("Original Stock Price Series")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.tight_layout()


    # Plot first difference
    diff = data.diff().dropna()
    plt.figure(figsize=(12,4))
    plt.plot(diff, label = "First Difference")
    plt.title("First Difference of Stock Price Series")
    plt.xlabel("Date")
    plt.ylabel("Change in Price")
    plt.legend()
    plt.tight_layout()

    # Plot Rolling Mean and Standard Deviation of first difference

    rollingMean = diff.rolling(window = 10).mean()
    rollingStd = diff.rolling(window = 10).std()

    plt.figure(figsize=(12,4))
    plt.plot(diff, label = "First Difference")
    plt.plot(rollingMean, label = "Rolling Mean (window = 10)", linestyle = "--")
    plt.plot(rollingStd, label = "Rolling Standard Deviation (window = 10)", linestyle = "--" )
    plt.title("Stationary Check")
    plt.xlabel("Date")
    plt.ylabel("Change in Price")
    plt.legend()
    plt.tight_layout()


    # ADF Test

    adfResult = adfuller(diff)
    print("ADF Statistic: ", adfResult[0])
    print("p-value: ", adfResult[1])

    if adfResult[1] < 0.05:
        print("Likely Stationary")
    else:
        print("Likely non-stationary")

    model = ARIMA(data, order = (5, 1, 0))
    modelFit= model.fit()
    forecast = modelFit.forecast(steps = 7)

    #lastPrice = data.iloc[-1]
    forecast_price = forecast


    plt.figure(figsize=(10,5))
    plt.plot(data, label = 'Historical')
    #plt.plot(pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=7), forecast, label='Forecast', linestyle='--', color='orange')
    plt.plot(pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=7), 
         forecast_price, 
         label='Forecast', linestyle='--', color='orange')
    plt.title("ARIMA Stock Price Forecast")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
   



# ---------------------------------------
# main() for running ONLY the ARIMA plot
# ---------------------------------------
# import yfinance as yf

# def main():
#     ticker_symbol = input("Enter a stock ticker (e.g., AAPL, MSFT): ").upper()
#     try:
#         ticker = yf.Ticker(ticker_symbol)
#         plotARIMA(ticker)
#         #futurePrice(ticker)
#         plt.show()          # <-- your function defined above
#     except Exception as e:
#         print(f"❌ Error processing ticker '{ticker_symbol}': {e}")

# if __name__ == "__main__":
#     main()






