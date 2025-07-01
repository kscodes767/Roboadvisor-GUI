import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

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



