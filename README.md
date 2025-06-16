# Stock Analysis & Comparison Tool

This is a command-line Python project that allows users to search for companies, retrieve financial and stock data using the `yfinance` and `yahooquery` APIs, and visualize or save that data for further analysis.

---

## Features

- **Search companies** by name and retrieve their ticker symbols
- **View stock data** for 1 day, 5 days, or 1 month
- **Access financial statements** including:
  - Balance Sheet
  - Cash Flow
  - Earnings
- **Get company overview** (industry, sector, business summary)
- **Compare multiple companies** on:
  - Stock price trends (static or interactive Plotly charts)
  - Trading volume
  - Daily returns
- **Save results** to `.csv` or `.xlsx` with custom filenames and sheet names

---

## Technologies Used

- Python 3.x
- `yfinance` – for stock data
- `yahooquery` – for company symbol search
- `pandas` – for data manipulation
- `matplotlib` – for static graphs
- `plotly` – for interactive charts
- `openpyxl` – for Excel writing

---

## Project Structure

project/
│
├── main.py                # Main program with menu system
├── finance_data.py        # Handles ticker search, stock & financial data
├── graph_data.py          # Static & interactive comparisons
├── save_data.py           # CSV/Excel save functionality
├── README.md              # This file
└── requirements.txt       # List of required package

---


## How to Use

**Installation**: Clone the repo and install the dependcies (pip install -r requirements.txt)
**Running the Program**: Type python main.py into user terminal
**Interact with Program**: Follow on screen prompts and interact as you choose

## Future Plans

	•	Expand options for an interactive graph to returns and trading volume
	•	Integrate regression or ARIMA-based price forecasting
	•	Deploy as a Streamlit web app
	•	Add stock alerts


