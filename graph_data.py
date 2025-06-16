import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = 'browser'

# def compareCompStocks(tickerList):
#     plt.figure(figsize = (10,5))
#     for ticker in tickerList:
#         data = ticker.history(period ="1mo")['Close']
#         plt.plot(data,label = ticker.ticker)
#     plt.title("Stock Price Comparison")
#     plt.legend()
#     plt.grid(True)
#     plt.tight_layout()
#     plt.show()

def compareCompStocks(tickerList):
    graphType = input("Press 1 for static graph and 2 for interactive graph \nEnter Choice: ")
    if graphType == "1":
        plt.figure(figsize = (10,5))
        for ticker in tickerList:
            data = ticker.history(period ="1mo")['Close']
            plt.plot(data,label = ticker.ticker)
        plt.title("Stock Price Comparison")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        plt.xlabel('Date')
        plt.ylabel('Price(USD)')
    elif graphType == "2":
        fig = go.Figure()

        for ticker in tickerList:
            data = ticker.history(period = "1mo")['Close']
            fig.add_trace(
                go.Scatter(
                    x = data.index,
                    y = data.values,
                    mode = 'lines',
                    name = ticker.ticker,
                    hovertemplate='Date: %{x}<br>Price: $%{y: .2f}<extra>%{name}</extra>'
                )
            )
            fig.update_layout(
                title = 'Stock Price Comparison (Interactive)',
                xaxis_title = 'Date',
                yaxis_title = 'Closing Price USD',
                hovermode = 'x unified',
                template = 'plotly_white',
                height = 500,
                width = 900
            )
            fig.show()
    else:
        print("Invalid Option")
            


def compareCompVol(tickerList):
    plt.figure(figsize = (10,5))
    for ticker in tickerList:
        volume = ticker.history(period ="1mo")['Volume']
        plt.plot(volume,label = ticker.ticker)
    plt.title("Volume Comparison")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def compareCompReturns(tickerList):
    plt.figure(figsize = (10,5))
    for ticker in tickerList:
        data = ticker.history(period ="1mo")
        close = data['Close']
        returns = close.pct_change()
        plt.plot(returns,label = ticker.ticker)
    plt.title("Daily Returns Comparison")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


    
