from finance_data import finStats, findTicker, stockPrice, companyOverview
from graph_data import compareCompStocks, compareCompReturns, compareCompVol
from forecasting import plotSMA, plotEMA, futurePrice, plotARIMA
import sys
import streamlit as st


# User chooses to look at two companies or just one company    

def getUserChoice():
        userChoice = st.radio(
            "Please Select a choice",
            options = [
            "1. One Company",
            "2. Two Companies",
            "3. Compare Company Data",
            "4. Forecasting"

            ]

        )

        if "1. One Company" in userChoice:
            ticker = getCompanyName()
            return ("single", ticker)
        elif "2. Two Companies" in userChoice:
            ticker = getTwoCompNames()
            return ("double", ticker)
        elif "3. Compare Company Data" in userChoice:
            tickers = getCompareNames()
            return ("compare", tickers)
        elif "4. Forecasting" in userChoice:
            ticker = getForecastName()
            return("Forecast" ,ticker)
        return None



# Get company name from user:
def getCompanyName():
        
        company_name = st.text_input("Enter a company name: ").strip()
        ticker = findTicker(company_name)
        if ticker:
            st.success(f"Found ticker: {ticker}")
            return ticker
        else:
            st.error("Invalid company name")
        return None
      

def getTwoCompNames():
        compName1 = st.text_input("Enter name of first company: ").strip()
        ticker1 = None
        ticker2 = None
        if compName1:
            ticker1 = findTicker(compName1)
            if ticker1:
                st.success(f"Found ticker {ticker1}")
                compName2 = st.text_input("Enter name of second company: ").strip()
                if compName2:
                    ticker2 = findTicker(compName2)
                    if ticker2:
                        st.success(f"Found ticker {ticker2}")  
                        return(ticker1, ticker2)  
                    else:
                        st.error("Invalid ticker1")
                else:
                    st.warning("Please enter the second company name")
            else:
                st.error("Invalid ticker2")
        return None

         

# Get company names for a comparison
def getCompareNames():
    with st.form("compare_form"):  # Start the form block

        numTickers = st.number_input(
            "How many companies would you like to compare:",
            min_value=1,
            step=1,
            format="%d"
        )

        # Collect company names using a list comprehension
        names = [
            st.text_input(
                f"Enter company {i + 1}:",
                key=f"compare_{i}"
            ).strip()
            for i in range(int(numTickers))
        ]

        # Must be inside the form block
        submitted = st.form_submit_button("Look up tickers")

    # Outside the form block
    if submitted:
        tickerList = []
        for name in names:
            if name:
                ticker = findTicker(name)
                if ticker:
                    st.success(f"Added ticker: {ticker}")
                    tickerList.append(ticker)
                else:
                    st.error(f"Ticker not found for: {name}")
                    return None
            else:
                st.error("Invalid company name")
                return None

        return tickerList

    return None

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


        