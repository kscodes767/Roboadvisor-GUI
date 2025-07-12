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



@st.cache_data
def getStockPrice(symbol, period):
    ticker = getTicker(symbol)
    rawStockData = ticker.history(period= period)
    return pd.DataFrame(rawStockData)


def stockPrice(ticker):

    option = st.radio(
        "What timeframe would you like to look at: ",
        options = [ "1 Day", "5 Days", "1 Month"],
        horizontal= True
    )
    stockOptionMap = {
        "1 Day": "1d",
        "5 Days": "5d",
        "1 Month": "1mo"
    }
    period = stockOptionMap.get(option)
    if not period:
        st.error("Invalid Option")
        return
    with st.spinner("Loadin stock data..."):
        symbol = ticker.ticker.strip().upper()
        data = getStockPrice(symbol, period)
        if data.empty:
            st.error("No data found!")
        else:
            st.dataframe(data)
            graphOption = st.radio(
                "Would you like to graph this as well?",
                options = ["Yes", "No"],
                horizontal=True
            )
            if graphOption == "Yes":
                graphStock(ticker, period)
            else:
                return

    


def companyOverview(ticker):
    info = ticker.info
    st.write(f"Name: {info.get('longName', 'N/A')}")
    st.write(f"Sector: {info.get('sector', 'N/A')}")
    st.write(f"Industry: {info.get('industry', 'N/A')}")
    st.write(f"Description: {info.get('longBusinessSummary', 'N/A')}")

def peRatio(ticker):
    pe = ticker.info.get("trailingPE", None)
    if pe is not None:
        st.metric("PE Ratio (Trailing)", value = f"{pe:.2f}")
    else:
        st.warning("PE ratio not available for this company")

def companyRatio(ticker):
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    with row1_col1:
       pe = ticker.info.get("trailingPE", None)
       if pe is not None:
            st.metric("PE Ratio (Trailing)", value = f"{pe:.2f}")
       else:
            st.warning("PE ratio not available for this company")
    # with row1_col2:
    #     pegRatio = ticker.info.get("pegRatio", "N/A")
    #     if pegRatio is not None:
    #         st.metric("PEG Ratio", value = f"{pegRatio:.2f}" )
    #     else:
            st.warning("PEG Ratio is not found")
    with row1_col3:
        priceToBook = ticker.info.get("priceToBook", None)
        if priceToBook is not None:
            st.metric("Price To Book", value = f"{priceToBook:.2f}")
        else:
            st.warning("Price to Book not available for this company")
    st.divider()
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    with row2_col1:
        marketCap = ticker.info.get("marketCap", None)
        if marketCap is not None:
            st.metric("Market Cap", value = f"{marketCap:,}")
        else:
            st.warning("Market Cap not available for this company")
    with row2_col2:
        ebitda = ticker.info.get("enterpriseToEbitda", None)
        if ebitda is not None:
            st.metric("EV/EBITDA", value = f"{ebitda:.2f}")
        else:
            st.warning("EV/EBITDA not available for this company")
    with row2_col3:
        trailingEps = ticker.info.get("trailingEps" , None)
        forwardEps = ticker.info.get("forwardEps", None)
        if trailingEps is not None:
            st.metric("Trailing EPS", value = f"{trailingEps:.2f}")
        else:
            st.warning("Trailing EPS not available for this company")
        if forwardEps is not None:
              st.metric("Forward EPS", value = f"{forwardEps:.2f}")
        else:
            st.warning("Forward EPS not available")
        
    


