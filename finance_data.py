import yfinance as yf
from yahooquery import search 
import pandas as pd
from save_data import saveData
from graph_data import graphStock


def findTicker(company_name):
    try: 
        results = search(company_name)
        ticker_symbol = results["quotes"][0]["symbol"]
        print(f"Ticker Symbol: {ticker_symbol}")
        ticker = yf.Ticker(ticker_symbol)
        return ticker
    except (KeyError, IndexError, TypeError):
        print("Error: Could not find a valid ticker symbol for that company")
        return None
    except Exception as e:
        print(f"Unexpected error occurred {e}")
        return None

def finStats(user_option,ticker):
    finOptions = {
        "1": "balance_sheet",
        "2": "cashflow",
        "3": "income_stmt"
    }
    attrName = finOptions.get(user_option)
    if not attrName :
        print("Incorrect Option")
        return
    else:
        data = getattr(ticker, attrName)
        data = pd.DataFrame(data)
        print(data)
        saveData(data)

def stockPrice(stock_option, ticker):
    stockOptionMap = {
        "1": "1d",
        "2": "5d",
        "3": "1mo"
    }
    period = stockOptionMap.get(stock_option)
    if period:
        data = pd.DataFrame(ticker.history(period =  period))
        print(data)
        graphStock(ticker, period)
        saveData(data)
    else:
        print("Invalid Option")



def companyOverview(ticker):
    info = ticker.info
    print(f"Name: {info.get('longName', 'N/A')}")
    print(f"Sector: {info.get('sector', 'N/A')}")
    print(f"Industry: {info.get('industry', 'N/A')}")
    print(f"Description: {info.get('longBusinessSummary', 'N/A')}")

