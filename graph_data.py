import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st
pio.renderers.default = 'browser'



def compareCompStocks(tickerList):
        graphType = st.radio (
            "What kind of graph would you like",
            options = [
            "Static Graph",
            "Interactive Graph"
            ]
            
        )
        
        if graphType == "Static Graph":
            plt.figure(figsize = (10,5))
            for ticker in tickerList:
                data = ticker.history(period ="1mo")['Close']
                plt.plot(data,label = ticker.ticker)
            plt.title("Stock Price Comparison")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.xlabel('Date')
            plt.ylabel('Price(USD)')
            st.pyplot(plt)

        elif graphType == "Interactive Graph":
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
            st.plotly_chart(fig, use_container_width=True)
            


def compareCompVol(tickerList):
        graphType = st.radio(
             "What type of graph would you like",
             options = [
            "Static Graph",
             "Interactive Graph"         
             ]

        )
        if graphType == "Static Graph":
            plt.figure(figsize = (10,5))
            for ticker in tickerList:
                volume = ticker.history(period ="1mo")['Volume']
                plt.plot(volume,label = ticker.ticker)
            plt.title("Volume Comparison")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.xlabel("Date")
            plt.ylabel("Volume Traded")
            st.pyplot(plt)
        elif graphType == "Interactive Graph":
            fig = go.Figure()

            for ticker in tickerList:
                data = ticker.history(period = "1mo")
                volume = data['Volume']
                fig.add_trace(
                    go.Scatter(
                        x = volume.index,
                        y = volume.values,
                        mode = 'lines',
                        name = ticker.ticker,
                        hovertemplate='Date: %{x}<br>Volume: %{y: .2f}<extra>%{name}</extra>'
                    )
                )
                fig.update_layout(
                    title = 'Volume Traded Comparison (Interactive)',
                    xaxis_title = 'Date',
                    yaxis_title = 'Volume Traded',
                    hovermode = 'x unified',
                    template = 'plotly_white',
                    height = 500,
                    width = 900
                )
            st.plotly_chart(fig, use_container_width=True)



def compareCompReturns(tickerList):
        graphType = st.radio(
             "What type of graph would you like",
             options = [
                  "Static Graph",

                  "Interactive Graph"
             ]
        )
        if graphType == "Static Graph":
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
            st.pyplot(plt)

        elif graphType == "Interactive Graph":
            fig = go.Figure()

            for ticker in tickerList:
                data = ticker.history(period ="1mo")
                close = data['Close']
                returns = close.pct_change()
                fig.add_trace(
                    go.Scatter(
                        x = returns.index,
                        y = returns.values,
                        mode = 'lines',
                        name = ticker.ticker,
                        hovertemplate='Date: %{x}<br>Returns: %{y: .2f}<extra>%{name}</extra>'
                    )
                )
                fig.update_layout(
                    title = 'Daily Returns Comparison (Interactive)',
                    xaxis_title = 'Date',
                    yaxis_title = 'Returns',
                    hovermode = 'x unified',
                    template = 'plotly_white',
                    height = 500,
                    width = 900
                )
            st.plotly_chart(fig, use_container_width=True)


def graphStock(ticker, period):
        graphOption = st.radio(
            "Would you like to graph this data as well",
            options = [
                 "Yes",
                 "No"
            ] 
        )
        symbol = ticker.ticker
        if graphOption == "Yes":
            plt.figure(figsize = (10,5))
            data = ticker.history(period = period)['Close']
            plt.plot(data,label = ticker.ticker)
            plt.title(f"Stock Price for {symbol}")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.xlabel('Date')
            plt.ylabel('Price(USD)')
            st.pyplot(plt)
        elif graphOption == "No":
            pass




    
