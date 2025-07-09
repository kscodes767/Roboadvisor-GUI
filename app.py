import streamlit as st
from finance_data import findTicker, stockPrice
from forecasting import plotSMA, plotEMA

st.title("📈 Stock Analysis & Forecasting Tool")

company = st.text_input("Enter a company name:")
if company:
    ticker = findTicker(company)
    if ticker:
        st.success(f"Found ticker: {ticker.ticker}")

        option = st.selectbox("Select an action", [
            "View 1-Day Price",
            "View 5-Day Price",
            "View 1-Month Price",
            "Plot SMA",
            "Plot EMA"
        ])

        if st.button("Run Analysis"):
            if option == "View 1-Day Price":
                stockPrice("1", ticker)
            elif option == "View 5-Day Price":
                stockPrice("2", ticker)
            elif option == "View 1-Month Price":
                stockPrice("3", ticker)
            elif option == "Plot SMA":
                plotSMA(ticker)
            elif option == "Plot EMA":
                plotEMA(ticker)
    else:
        st.error("Ticker not found. Try a different company.")


