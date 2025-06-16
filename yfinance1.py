from pprint import pprint 
import yfinance as yf 
from yahooquery import search 
import pandas as pd

# Get company name from user:
def getCompanyName():
    company_name = input("Enter a company name: ")

# Search for ticker symbol
    results = search(company_name)
    if "quotes" in results and len(results["quotes"]) > 0:
        ticker_symbol = results["quotes"][0]["symbol"]
        print(f"Ticker Symbol: {ticker_symbol}")
        ticker = yf.Ticker(ticker_symbol)
        getUserInput(ticker)
        return ticker

def getUserInput(ticker):
    user_option = input("What would you like to see: \n 1. Balance Sheet \n 2. Cash Flow \n 3. Earnings \n Option:")
    getStats(user_option,ticker)
    return user_option

def getStats(financial_option,ticker):
    if financial_option not in ["1", "2", "3"]:
        print("Incorrect option")
        # getUserInput(ticker)
    elif financial_option == "1":
        balanceSheet = ticker.balance_sheet
        print(balanceSheet)
    elif financial_option == "2":
        cashFlow = ticker.cashflow 
        print(cashFlow)
    else:
        earnings = ticker.income_stmt
        print(earnings)




getCompanyName()