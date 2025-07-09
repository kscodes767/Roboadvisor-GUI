import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date

from finance_data import (
    findTicker, stockPrice,                       # CLI helpers you wrote
    finStats, companyOverview                     # ← already Streamlit-friendly
)
from forecasting import plotSMA, plotEMA, futurePrice, plotARIMA
from graph_data import compareCompStocks          # we’ll reuse for interactive chart
from save_data import saveData                    # still works


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
            "Plot SMA",
            "Plot EMA",
            "Future Forecast (Linear)",
            "Forecast (ARIMA)"
            ]


        )

        if option == "Company Overview":
            companyOverview(ticker)
        elif option == "Financial Statements":
            finStats(ticker)
        elif option == "Quick 1,5,30 Day Table":
            timeFrame = st.radio(
                "Pick a time frame: ",
                options = ["1 Day", "5 Days", "30 Days"], horizontal=True,
                
            )
            tf_map = {"1 Day":"1", "5 Days": "2", "30 Days":"3"}
            stockPrice(tf_map[timeFrame], ticker)   

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
        elif option == "Plot SMA":
            plotSMA(ticker)
        elif option == "Plot EMA":
            plotEMA(ticker)
        elif option == "Future Forecast (Linear)":
            futurePrice(ticker)
        elif option == "Future Forecast (ARIMA)":
            plotARIMA(ticker)


def getUserChoice():
    st.title("Stock Analysis and Forecasting Tool")

    choice = st.radio(
        "What would you like to do: ",
        ["Analyze One Company", "Forecast", "Compare Companies (Coming Soon)"]
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
    return None, None


def main():
    choice_type, data = getUserChoice()

    if choice_type == "single" and data:
        singleMenuTicker(data)

    elif choice_type == "forecast" and data:
        st.subheader(f"Forecasts for {data.ticker}")
        method = st.radio("Forecast method", ["Linear Regression", "ARIMA"])
        futurePrice(data) if method == "Linear Regression" else plotARIMA(data)

    elif choice_type is None:
        st.info("👆 Select an option to begin.")


if __name__ == "__main__":
    main()


