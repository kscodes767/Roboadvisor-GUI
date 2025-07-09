import streamlit as st
from finance_data import findTicker, stockPrice
from forecasting import plotSMA, plotEMA, futurePrice, plotARIMA

def singleMenu(ticker):
    st.subheader(f"Single Company Menu for {ticker.ticker}")

    option = st.selectbox("Choose an analysis option", [
        "View 1-Day Price",
        "View 5-Day Price",
        "View 1-Month Price",
        "Plot SMA",
        "Plot EMA",
        "Forecast (Linear)",
        "Forecast (ARIMA)"
    ])

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
    elif option == "Forecast (Linear)":
        futurePrice(ticker)
    elif option == "Forecast (ARIMA)":
        plotARIMA(ticker)


def getUserChoice():
    st.title("📈 Stock Analysis & Forecasting Tool")
    
    choice = st.radio("What would you like to do?", [
        "Analyze One Company",
        "Compare Two Companies (Coming Soon)",
        "Compare Multiple Companies (Coming Soon)",
        "Forecast Only"
    ])

    if choice in ["Analyze One Company", "Forecast Only"]:
        company = st.text_input("Enter a company name:")
        if company:
            ticker = findTicker(company)
            if ticker:
                st.success(f"Found ticker: {ticker.ticker}")
                return ("single" if choice == "Analyze One Company" else "Forecast", ticker)
            else:
                st.error("Ticker not found.")
    return None, None


def main():
    choice_type, data = getUserChoice()

    if choice_type == "single":
        ticker = data
        singleMenu(ticker)

    elif choice_type == "Forecast":
        ticker = data
        st.subheader(f"Forecast Menu for {ticker.ticker}")
        forecast_option = st.radio("Select forecast method", ["Linear Regression", "ARIMA"])
        if forecast_option == "Linear Regression":
            futurePrice(ticker)
        else:
            plotARIMA(ticker)

    # Placeholder for future comparison menus
    elif choice_type in ["double", "compare"]:
        st.warning("Comparison features coming soon!")


if __name__ == "__main__":
    main()


