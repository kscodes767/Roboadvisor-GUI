from finance_data import finStats, findTicker, stockPrice, companyOverview
from graph_data import compareCompStocks, compareCompReturns, compareCompVol
from forecasting import plotSMA, plotEMA, futurePrice, plotARIMA
import sys


# User chooses to look at two companies or just one company 
def getUserChoice():
    while True:
        userChoice = input("1. Just One Company \n2. Two Companies \n3. Compare Company Data \n4. Forecasting \nEnter Choice: ").strip()
        if userChoice == "1":
            return ("single", getCompanyName())
        elif userChoice == "2":
            return ("double", getTwoCompNames())
        elif userChoice == "3":
            tickers = getCompareNames()
            return ("compare", tickers)
        elif userChoice == "4":
            return("Forecast" ,getForecastName())
        else:
            print("invalid option")
         
    

# Get company name from user:
def getCompanyName():
    while True:
        company_name = input("Enter a company name: ").strip()
        ticker = findTicker(company_name)
        if ticker:
            return ticker
        else:
            print("Invalid company name")
      

def getTwoCompNames():
    while True:
        compName1 = input("Enter name of first company: ").strip()
        ticker1 = findTicker(compName1)
        if ticker1:
            break
    while True:
        compName2 = input ("Enter name of second company: ").strip()
        ticker2 = findTicker(compName2)
        if ticker2:
            break
    return ticker1, ticker2

# Get company names for a comparison
def getCompareNames():
    numTickers = int(input("How many companies would you like to compare: ").strip())
    tickerList = []
    for i in range (numTickers):
        name = input(f"Please enter company name {i + 1}: ").strip()
        ticker = findTicker(name)
        if ticker:
            print(f"Added ticker: {ticker.ticker}")
            tickerList.append(ticker)
        else:
            print(f"Ticker not found for: {name}")
    # compareOptions(tickerList)
    return tickerList


def compareOptions(tickerList):
        if not tickerList:
            print("Invalid options")
            return 
        compareOption = input("What would you like to compare: \n1. Stock Prices \n2. Volume Traded \n3. Returns \nEnter Option: ").strip()
        if compareOption == '1':
            compareCompStocks(tickerList)
        elif compareOption == '2':
            compareCompVol(tickerList)
        elif compareOption == '3':
            compareCompReturns(tickerList)
        else:
            print("Invalid option selected")


# Get user option 
def getUserInput(ticker):
    category = input("What would you like to see: \n 1. Financial Statements \n 2. Stocks \n 3. Company Overview \nEnter Option:").strip()
    if category == "1":
        financial_option = input("Choose financial statement: \n1. Balance Sheet\n2. Cash Flow \n3. Earnings\nEnter Choice:").strip()
        finStats(financial_option,ticker)
        return financial_option
    elif category == "2":
        stock_option = input("View stock prices for:\n1. 1 Day \n2. 5 Days \n3. 1 Month\nEnter Choice: ").strip()
        stockPrice(stock_option, ticker)
    elif category == "3":
        companyOverview(ticker)
    else:
        print("Invalid Choice")
        return getUserInput(ticker)
    
def getForecastName():
    while True:
        compName1 = input("Enter name of the company: ").strip().lower()
        ticker = findTicker(compName1)
        if ticker:
            return ticker
        else:
            print("Invalid ticker, please try again.")

def forecastMenu(ticker):
    forecastOption = input("What would you like to calculate: \n1: Simple Moving Average (SMA) \n2. Exponential Moving Average (EMA) \n3. Look at future stock prices \n4. ARIMA Model \nEnter Choice: ").strip().lower()
    if forecastOption == "1":
        plotSMA(ticker)
    elif forecastOption == "2":
        plotEMA(ticker)
    elif forecastOption == "3":
        futurePrice(ticker)
    elif forecastOption == "4":
        plotARIMA(ticker)
    else:
        print("Invalid option.")
        forecastMenu(ticker)
    
def mainMenu(userChoice, restartFunc):
    while True:
        menuChoice = input("What would you like to do next?\n1. Go back to original menu \n2. Repeat last action \n3. Exit\nEnter Choice: ").strip()
        if menuChoice == "1":
            restartFunc()
            break
        elif menuChoice == "2":
            if userChoice == '1':
                ticker = getCompanyName()
                getUserInput(ticker)
            elif userChoice == "2":
                ticker1, ticker2 = getTwoCompNames()
                print("\nCompany 1 Stats:")
                getUserInput(ticker1)
                print("\nCompany 2 Stats:")
                getUserInput(ticker2)
            elif userChoice == "3":
                tickerList = getCompareNames()
                compareOptions(tickerList)
            elif userChoice == "4":
                ticker = getForecastName()
                forecastMenu(ticker)
        elif menuChoice == "3":
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid choice")


        