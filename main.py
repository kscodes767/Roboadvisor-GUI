from user_input import getUserChoice, getUserInput, getCompareNames, mainMenu, compareOptions
from user_input import getUserChoice, getUserInput, getCompareNames, mainMenu, forecastMenu
from forecasting import plotSMA 

def main():
    choice_type, data = getUserChoice()

    if choice_type == "single":
        ticker = data
        print("\nCompany Stats:")
        getUserInput(ticker)
        mainMenu("1", main)

    elif choice_type == "double":
        ticker1, ticker2 = data
        print("\nCompany 1 Stats:")
        getUserInput(ticker1)
        print("\nCompany 2 Stats:")
        getUserInput(ticker2)
        mainMenu("2", main)

    elif choice_type == "compare":
        tickerList = data
        compareOptions(tickerList)
        mainMenu("3", main)

    elif choice_type == "Forecast":
        ticker = data
        forecastMenu(ticker)
        mainMenu("4", main)

if __name__ == "__main__":
    main()