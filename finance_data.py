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
    if user_option not in ["1", "2", "3"]:
        print("Incorrect option")
        # getUserInput(ticker)
    elif user_option == "1":
        data = pd.DataFrame(ticker.balance_sheet)
        print(data)
    elif user_option == "2":
        data = pd.DataFrame(ticker.cashflow)
        print(data)
    elif user_option == '3':
        data = pd.DataFrame(ticker.income_stmt)
        print(data)
    saveData(data)

    

def stockPrice(stock_option, ticker):
    if stock_option == "1":
        data = ticker.history(period = "1d")
        print(data)
    elif stock_option == "2":
       data = ticker.history(period = "5d")
       print(data)
    elif stock_option == "3":
        data = ticker.history(period = "1mo")
        print(data)
    else:
        print("Invalid choice")
    graphStock(ticker)
    saveData(data)


def companyOverview(ticker):
    info = ticker.info
    print(f"Name: {info.get('longName', 'N/A')}")
    print(f"Sector: {info.get('sector', 'N/A')}")
    print(f"Industry: {info.get('industry', 'N/A')}")
    print(f"Description: {info.get('longBusinessSummary', 'N/A')}")

