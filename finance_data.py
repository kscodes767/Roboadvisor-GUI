import yfinance as yf
from yahooquery import search 
import pandas as pd
from save_data import saveData
from graph_data import graphStock
import streamlit as st


@st.cache_resource
def findTicker(company_name):
    try: 
        results = search(company_name)
        ticker_symbol = results["quotes"][0]["symbol"]
        (f"Ticker Symbol: {ticker_symbol}")
        ticker = yf.Ticker(ticker_symbol)
        return ticker
    except (KeyError, IndexError, TypeError):
        st.error("Error: Could not find a valid ticker symbol for that company")
        return None
    except Exception as e:
        st.error(f"Unexpected error occurred {e}")
        return None



@st.cache_resource
def getTicker(symbol):
    return (yf.Ticker(symbol))

@st.cache_data
def getFinData(symbol, attrName):
    ticker = getTicker(symbol)
    rawData = getattr(ticker, attrName)
    return pd.DataFrame(rawData)
    

def finStats(ticker):
    st.subheader("View Financial Statements")
    show = st.checkbox("Click to load financial statements")
    if not show:
        return
    
    option = st.radio(
    "What would you like to look at: ",

      options =  [
        "Balance Sheet",
        "Cash Flow",
        "Income Statement"  
       ] 
    )
    finOptions = {
        "Balance Sheet": "balance_sheet",
        "Cash Flow": "cashflow",
        "Income Statement": "income_stmt"
    }
    attrName = finOptions.get(option)
    if not attrName :
        st.error("Incorrect Option")
        return
    with st.spinner("Loading financial data..."):
        data = getFinData(ticker.ticker.strip().upper(), attrName)
        if data.empty:
            st.error("No data found!")
        else:
            st.dataframe(data)




def stockPrice(period, ticker):

    # option = st.radio(
    #     "What timeframe would you like to look at: ",
    #     options = [ "1 Day", "5 Days", "1 Month"],
    # )
    # stockOptionMap = {
    #     "1 Day": "1d",
    #     "5 Days": "5d",
    #     "1 Month": "1mo"
    # }
    # period = stockOptionMap.get(option)
    if period:
        data = pd.DataFrame(ticker.history(period =  period))
        st.dataframe(data)
        # graphStock(ticker, period)
        saveData(data)
    else:
        st.error("Invalid Option")



def companyOverview(ticker):
    info = ticker.info
    st.write(f"Name: {info.get('longName', 'N/A')}")
    st.write(f"Sector: {info.get('sector', 'N/A')}")
    st.write(f"Industry: {info.get('industry', 'N/A')}")
    st.write(f"Description: {info.get('longBusinessSummary', 'N/A')}")

