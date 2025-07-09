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
            "One Company",
            "Two Companies",
            "Compare Company Data",
            "Forecasting"

            ]

        )

        if "One Company" in userChoice:
            ticker = getCompanyName()
            return ("single", ticker)
        elif "Two Companies" in userChoice:
            ticker = getTwoCompNames()
            return ("double", ticker)
        elif "Compare Company Data" in userChoice:
            tickers = getCompareNames()
            return ("compare", tickers)
        elif "Forecasting" in userChoice:
            ticker = getForecastName()
            return("forecast" ,ticker)
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
    tickerList = []
    with st.form("compare_form"): 

        numTickers = st.number_input(
            "How many companies would you like to compare:",
            min_value=1,
            step=1,
            format="%d"
        )

        names = [
            st.text_input(
                f"Enter company {i + 1}:",
                key=f"compare_{i}"
            ).strip()
            for i in range(int(numTickers))
        ]

        submitted = st.form_submit_button("Look up tickers")

        if submitted:
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

    return tickerList if tickerList else None


def compareOptions(tickerList):
        compareOption = st.radio(
            "What would you like to compare?",
            options = [
            "1. Stock Prices",
            "2. Volume Traded",
            "3. Returns"
            ]
            )
        if compareOption == "1. Stock Prices":
            compareCompStocks(tickerList)
        elif compareOption == "2. Volume Traded":
            compareCompVol(tickerList)
        elif compareOption == "3. Returns":
            compareCompReturns(tickerList)
        else:
            st.error("Invalid option selected")


# Get user option 
def getUserInput(ticker):
    category = st.radio (
        "What would you like to see?",
        options = [
            "Financial Statements",
            "Stocks",
            "Company Overview"
        ]
    )
    if category == "Financial Statements":
        financialOption = st.radio(
            "Choose financial statement",
            options = [
                "Balance Sheet",
                "Cash Flow",
                "Earnings"
            ]
        )
        finStats(financialOption,ticker)
        return financialOption
    elif category == "Stocks":
        stockOption = st.radio (
            "View stock prices",
            options = [
                "1 Day",
                "5 Days",
                "Month"
            ]
        )
        stockPrice(stockOption, ticker)

    elif category == "Company Overview":
        companyOverview(ticker)
    else:
        st.error("Invalid Choice")

        return getUserInput(ticker)
    
def getForecastName():
        with st.form("forecast_form"):
            compName = st.text_input("Enter name of the company: ").strip().lower()
            submitted = st.form_submit_button("Find Ticker")
        if submitted:
            if compName:
                ticker = findTicker(compName)
                if ticker:
                    st.success(f"Found ticker: {ticker}")
                    return ticker
                else:
                    st.error("Invalid ticker, please try again.")
            else:
                st.error("Invalid company name")
        return None

def forecastMenu(ticker):
    st.subheader("Forecasting Tools")
    st.write("Select a forecasting method to visualize future stock behavior.")
    forecastOption = st.radio(
        "What would you like to calculate",
        options = [
            "Simple Moving Average (SMA)",
            "Exponential Moving Average (EMA)",
            "Look at future stock price trends",
            "ARIMA Model"
        ]
    )
    
    if forecastOption == "Simple Moving Average (SMA)":
        plotSMA(ticker)
    elif forecastOption == "Exponential Moving Average (EMA)":
        plotEMA(ticker)
    elif forecastOption == "Look at future stock price trends":
        futurePrice(ticker)
    elif forecastOption == "ARIMA Model":
        plotARIMA(ticker)
    else:
        st.error("Invalid option.")

    
def mainMenu(userChoice, restartFunc):
        menuChoice = st.radio(
            "What would you like to do next",
            options = [
                "Go back to original menu",
                "Repeat last action",
                "Exit"
            ]
        )
        if menuChoice == "Go back to original menu":
            restartFunc()
        elif menuChoice == "Repeat last action":
            if userChoice == "single":
                ticker = getCompanyName()
                getUserInput(ticker)
            elif userChoice == "double":
                ticker1, ticker2 = getTwoCompNames()
                st.write("Company 1 Stats:")
                getUserInput(ticker1)
                st.write("Company 2 Stats:")
                getUserInput(ticker2)
            elif userChoice == "compare":
                tickerList = getCompareNames()
                compareOptions(tickerList)
            elif userChoice == "forecast":
                ticker = getForecastName()
                forecastMenu(ticker)
        else:
            st.write("Goodbye! Please refresh the page to restart the app")
            st.stop()



        