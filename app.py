import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
from chat_bot import askLlama

from finance_data import (
    findTicker, stockPrice,                      
    finStats, companyOverview,
    companyRatio,
)
from forecasting import plotSMA, plotEMA, futurePrice, plotARIMA
from graph_data import compareCompStocks          
from save_data import saveData      
from  graph_data import compareCompReturns, compareCompStocks, compareCompVol          


def showPriceChart(df, symbol, interactive: bool):
    if interactive:
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x = df.index, y= df['Close'],
                name = 'Close', mode = 'lines',
                hovertemplate="Date: %{x|%Y-%m-%d}<br>Price: $%{y:.2f}"
                
            )
        )
        fig.update_layout(
            title = f"{symbol} price",
            xaxis_title = "Date", yaxis_title = "Price (USD)",
            template = 'plotly_white', height = 500

        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.line_chart(df["Close"], use_container_width= True)

def singleMenuTicker(ticker):
        st.subheader(f"Single Company Menu – {ticker.ticker}")
        option = st.selectbox(
            "Choose Analysis Option:",
            [
            "Company Overview",
            "Financial Statements",
            "Quick View (1,5,30 Day Table)",
            "Custom Price Window",
            "Company Statistics",
            "Plot SMA",
            "Plot EMA",
            "Future Forecast (Linear)",
            "Future Forecast (ARIMA)"
            ]


        )

        if option == "Company Overview":
            companyOverview(ticker)
        elif option == "Financial Statements":
            finStats(ticker)
        elif option == "Quick View (1,5,30 Day Table)":
            stockPrice(ticker)
        elif option == "Custom Price Window":
            col1, col2 = st.columns(2)
            with col1:
                start = st.date_input("Start Date", date(2024, 1, 1))
            with col2:
                end = st.date_input("End Date", date.today())
            
            chartType = st.checkbox("Interactive Chart (Plotly)", True)
            if start < end and st.button("Show Window"):
                df = ticker.history(start = str(start), end = str(end))
                if df.empty:
                    st.error("No price for that time period")
                else:
                    st.dataframe(df)
                    showPriceChart(df, ticker.ticker, chartType)
                    saveData(df)
        elif option == "Company Statistics":
            companyRatio(ticker)
        elif option == "Plot SMA":
            plotSMA(ticker)
        elif option == "Plot EMA":
            plotEMA(ticker)
        elif option == "Future Forecast (Linear)":
            futurePrice(ticker)
        elif option == "Future Forecast (ARIMA)":
            plotARIMA(ticker)

def compareCompanyMenu(tickerList):
        st.subheader("Compare Company Menu")
        compareOption = st.selectbox(
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


def getUserChoice():
    st.title("Stock Analysis and Forecasting Tool")

    choice = st.radio(
        "What would you like to do: ",
        ["Analyze One Company", "Forecast", "Compare Companies"]
    )
    if choice in ["Analyze One Company", "Forecast"]:
        company = st.text_input("Please enter the company you would like to explore (e.g. Apple)")
        if company:
            ticker = findTicker(company)
            if ticker:
                st.success(f"Found ticker {ticker.ticker}")
                return("single" if choice == "Analyze One Company" else "forecast", ticker)
            else:
                st.error("Ticker not found, please enter company")
        else:
            st.error("Company not found, please enter a different company")
    elif choice == "Compare Companies":
       with st.form("compare_Form"):
           numCompanies = st.number_input("How many companies would you like to compare?",
                min_value= 1, step=1, max_value=10)
           companyNames = []
           for i in range(int(numCompanies)):           
               name = st.text_input(f"Company {i + 1}", key = f"company_{i}")
               companyNames.append(name.strip())
           submitted = st.form_submit_button("Compare")
           if submitted:
               validNames = [name for name in companyNames if name]
               if not validNames:
                   st.error("Please enter at least one valid name")
               else: 
                   st.success(f"Comparing {",".join(validNames)}")
                   tickers = [findTicker(name) for name in validNames if findTicker(name)]
                   if not tickers:
                       st.error("No tickers were found")
                       return None, None
                   else:
                       st.session_state.compare_mode = True
                       st.session_state.tickers_to_compare = tickers
                   return "compare", tickers 
    if st.session_state.get("compare_mode") and st.session_state.get("tickers_to_compare"):
        return "compare", st.session_state.tickers_to_compare
               
    return None, None



def main():
    choice_type, data = getUserChoice()

    if choice_type == "single" and data:
        singleMenuTicker(data)

    elif choice_type == "forecast" and data:
        st.subheader(f"Forecasts for {data.ticker}")
        method = st.radio("Forecast method", ["Linear Regression", "ARIMA"])
        futurePrice(data) if method == "Linear Regression" else plotARIMA(data)
    
    elif choice_type == "compare":
        compareCompanyMenu(data)

    elif choice_type is None:
        st.info("👆 Select an option to begin.")


if __name__ == "__main__":
    main()


