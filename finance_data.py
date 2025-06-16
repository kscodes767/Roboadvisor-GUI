import yfinance as yf
from yahooquery import search 
import pandas as pd
from save_data import saveData



def findTicker(company_name):
    results = search(company_name)
    if "quotes" in results and len(results["quotes"]) > 0:
        ticker_symbol = results["quotes"][0]["symbol"]
        print(f"Ticker Symbol: {ticker_symbol}")
        ticker = yf.Ticker(ticker_symbol)
        return ticker
    else:
        print("No ticker found")
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
    saveData(data)


def companyOverview(ticker):
    info = ticker.info
    print(f"Name: {info.get('longName', 'N/A')}")
    print(f"Sector: {info.get('sector', 'N/A')}")
    print(f"Industry: {info.get('industry', 'N/A')}")
    print(f"Description: {info.get('longBusinessSummary', 'N/A')}")

