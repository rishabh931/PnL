import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

# Configure page
st.set_page_config(page_title="Stock Analyzer", layout="wide")
st.sidebar.title("📊 Indian Stock Analyzer")

# Input: Stock symbol
stock_query = st.sidebar.text_input("Enter NSE stock symbol (e.g., RELIANCE, INFY)", "")

# Section selector
section = st.sidebar.radio("Select Analysis Section", ["P&L Statement", "Quarterly Statement"])

def format_number(num):
    if abs(num) >= 1e7:
        return f"₹{num/1e7:,.2f} Cr"
    elif abs(num) >= 1e5:
        return f"₹{num/1e5:,.2f} L"
    elif abs(num) >= 1000:
        return f"₹{num/1000:,.2f} K"
    return f"₹{num:,.2f}"

def find_stock_symbol(query):
    query = query.upper().strip()
    if not query.endswith(".NS"):
        query += ".NS"
    if not re.match(r"^[A-Z0-9.-]{1,20}\.NS$", query):
        return None
    return query

@st.cache_data
def get_financials(ticker_symbol, quarterly=False):
    try:
        stock = yf.Ticker(ticker_symbol)
        if stock.info.get("regularMarketPrice") is None:
            return None, None, "Invalid stock symbol"

        if quarterly:
            income_stmt = stock.quarterly_financials
            balance_sheet = stock.quarterly_balance_sheet
        else:
            income_stmt = stock.financials
            balance_sheet = stock.balance_sheet

        financial_data = {}

        if 'Total Revenue' in income_stmt.index:
            financial_data['Revenue'] = income_stmt.loc['Total Revenue'].head(4).values[::-1]
        elif 'Revenue' in income_stmt.index:
            financial_data['Revenue'] = income_stmt.loc['Revenue'].head(4).values[::-1]
        else:
            return None, None, "Revenue data not available"

        if 'Operating Income' in income_stmt.index:
            financial_data['Operating Profit'] = income_stmt.loc['Operating Income'].head(4).values[::-1]
        elif 'Operating Profit' in income_stmt.index:
            financial_data['Operating Profit'] = income_stmt.loc['Operating Profit'].head(4).values[::-1]
        else:
            return None, None, "Operating Profit data not available"

        if 'Pretax Income' in income_stmt.index:
            financial_data['PBT'] = income_stmt.loc['Pretax Income'].head(4).values[::-1]
        else:
            return None, None, "PBT data not available"

        if 'Net Income' in income_stmt.index:
            financial_data['PAT'] = income_stmt.loc['Net Income'].head(4).values[::-1]
        else:
            return None, None, "PAT data not available"

        if 'Ordinary Shares Number' in balance_sheet.index:
            shares_outstanding = balance_sheet.loc['Ordinary Shares Number'].head(4).values[::-1]
        elif 'Share Issued' in balance_sheet.index:
            shares_outstanding = balance_sheet.loc['Share Issued'].head(4).values[::-1]
        else:
            shares = stock.info.get('sharesOutstanding')
            if shares:
                shares_outstanding = np.array([shares] * 4)
            else:
                return None, None, "Shares outstanding data not available"

        financial_data['EPS'] = financial_data['PAT'] / (shares_outstanding / 1e6)
        financial_data['OPM %'] = (financial_data['Operating Profit'] / financial_data['Revenue']) * 100

        eps_growth = [0]
        for i in range(1, len(financial_data['EPS'])):
            if financial_data['EPS'][i - 1] != 0:
                growth = ((financial_data['EPS'][i] - financial_data['EPS'][i - 1]) / abs(financial_data['EPS'][i - 1])) * 100
            else:
                growth = 0
            eps_growth.append(growth)
        financial_data['EPS Growth %'] = eps_growth

        periods = income_stmt.columns[:4].strftime('%Y' if not quarterly else '%b-%Y').values[::-1]

        return pd.DataFrame(financial_data, index=periods), periods, None
    except Exception as e:
        return None, None, str(e)

def show_analysis(df, label):
    st.header(f"{label} Financials")
    st.dataframe(df.style.format({
        'Revenue': format_number,
        'Operating Profit': format_number,
        'PBT': format_number,
        'PAT': format_number,
        'EPS': lambda x: f"₹{x:.2f}",
        'OPM %': lambda x: f"{x:.1f}%",
        'EPS Growth %': lambda x: f"{x:.1f}%"
    }))

    st.subheader("Trends")
    fig, ax = plt.subplots(figsize=(10, 6))
    df[['Revenue', 'Operating Profit', 'PAT']] = df[['Revenue', 'Operating Profit', 'PAT']] / 1e7
    df[['Revenue', 'Operating Profit', 'PAT']].plot(kind='bar', ax=ax)
    plt.ylabel("₹ Crores")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Main App Logic
if stock_query:
    ticker = find_stock_symbol(stock_query)
    if not ticker:
        st.error("Invalid stock symbol format.")
    else:
        st.title(f"📉 Analysis for {stock_query.upper()}")
        quarterly = (section == "Quarterly Statement")
        df, periods, err = get_financials(ticker, quarterly=quarterly)
        if err:
            st.error(f"Error: {err}")
        else:
            show_analysis(df, section)
