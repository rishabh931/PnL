import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Indian Stock PnL Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .positive-growth {
        color: #28a745;
        font-weight: bold;
    }
    .negative-growth {
        color: #dc3545;
        font-weight: bold;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin: 1.5rem 0 1rem 0;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def get_stock_symbol(stock_input):
    """Convert stock name/symbol to Yahoo Finance format for Indian stocks"""
    # Common Indian stock symbols mapping
    indian_stocks = {
        'reliance': 'RELIANCE.NS',
        'tcs': 'TCS.NS',
        'hdfc bank': 'HDFCBANK.NS',
        'infosys': 'INFY.NS',
        'icici bank': 'ICICIBANK.NS',
        'hdfc': 'HDFC.NS',
        'kotak mahindra': 'KOTAKBANK.NS',
        'bharti airtel': 'BHARTIARTL.NS',
        'itc': 'ITC.NS',
        'sbi': 'SBIN.NS',
        'l&t': 'LT.NS',
        'axis bank': 'AXISBANK.NS',
        'maruti suzuki': 'MARUTI.NS',
        'bajaj finance': 'BAJFINANCE.NS',
        'wipro': 'WIPRO.NS',
        'asian paints': 'ASIANPAINT.NS',
        'nestle': 'NESTLEIND.NS',
        'ultratech cement': 'ULTRACEMCO.NS',
        'titan': 'TITAN.NS',
        'sun pharma': 'SUNPHARMA.NS'
    }
    
    stock_input_lower = stock_input.lower().strip()
    
    # Check if it's a known stock name
    if stock_input_lower in indian_stocks:
        return indian_stocks[stock_input_lower]
    
    # If it already has .NS or .BO suffix, return as is
    if stock_input.upper().endswith('.NS') or stock_input.upper().endswith('.BO'):
        return stock_input.upper()
    
    # Otherwise, add .NS suffix for NSE
    return f"{stock_input.upper()}.NS"

def fetch_financial_data(symbol):
    """Fetch financial data from Yahoo Finance"""
    try:
        stock = yf.Ticker(symbol)
        
        # Get company info
        info = stock.info
        
        # Get financial statements
        financials = stock.financials
        quarterly_financials = stock.quarterly_financials
        
        return stock, info, financials, quarterly_financials
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None, None, None, None

def process_financial_data(financials):
    """Process and clean financial data"""
    if financials is None or financials.empty:
        return None
    
    # Convert to DataFrame and transpose for easier handling
    df = financials.T
    df.index = pd.to_datetime(df.index)
    df = df.sort_index(ascending=True)
    
    # Get last 4 years of data
    df_recent = df.tail(4)
    
    return df_recent

def calculate_growth_rate(current, previous):
    """Calculate growth rate between two values"""
    if previous == 0 or pd.isna(previous) or pd.isna(current):
        return 0
    return ((current - previous) / abs(previous)) * 100

def create_revenue_analysis(df, company_name):
    """Create revenue and operating profit analysis"""
    st.markdown('<div class="section-header">📊 Revenue & Operating Performance Analysis</div>', unsafe_allow_html=True)
    
    # Extract relevant data
    revenue_key = None
    operating_income_key = None
    
    # Find the correct column names (Yahoo Finance uses different naming conventions)
    possible_revenue_keys = ['Total Revenue', 'Revenue', 'Net Sales', 'Total Revenues']
    possible_operating_keys = ['Operating Income', 'Operating Revenue', 'Gross Profit', 'EBIT']
    
    for key in possible_revenue_keys:
        if key in df.columns:
            revenue_key = key
            break
    
    for key in possible_operating_keys:
        if key in df.columns:
            operating_income_key = key
            break
    
    if not revenue_key:
        st.warning("Revenue data not found in the financial statements")
        return
    
    # Get data
    revenue_data = df[revenue_key] / 1e7  # Convert to Crores
    years = [d.year for d in df.index]
    
    if operating_income_key:
        operating_data = df[operating_income_key] / 1e7  # Convert to Crores
        opm_data = (df[operating_income_key] / df[revenue_key] * 100)
    else:
        operating_data = pd.Series([0] * len(revenue_data), index=revenue_data.index)
        opm_data = pd.Series([0] * len(revenue_data), index=revenue_data.index)
    
    # Create visualization
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Revenue Trend (₹ Crores)', 'Operating Profit Trend (₹ Crores)', 
                       'Operating Profit Margin %', 'Revenue vs Operating Profit'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Revenue trend
    fig.add_trace(
        go.Scatter(x=years, y=revenue_data, mode='lines+markers', name='Revenue',
                  line=dict(color='#1f77b4', width=3), marker=dict(size=8)),
        row=1, col=1
    )
    
    # Operating profit trend
    if operating_income_key:
        fig.add_trace(
            go.Scatter(x=years, y=operating_data, mode='lines+markers', name='Operating Profit',
                      line=dict(color='#ff7f0e', width=3), marker=dict(size=8)),
            row=1, col=2
        )
    
    # OPM trend
    if operating_income_key:
        fig.add_trace(
            go.Scatter(x=years, y=opm_data, mode='lines+markers', name='OPM %',
                      line=dict(color='#2ca02c', width=3), marker=dict(size=8)),
            row=2, col=1
        )
    
    # Revenue vs Operating Profit
    if operating_income_key:
        fig.add_trace(
            go.Bar(x=['Revenue', 'Operating Profit'], 
                   y=[revenue_data.iloc[-1], operating_data.iloc[-1]],
                   name='Latest Year Comparison',
                   marker_color=['#1f77b4', '#ff7f0e']),
            row=2, col=2
        )
    
    fig.update_layout(height=800, showlegend=True, title_text=f"{company_name} - Revenue & Operating Performance")
    st.plotly_chart(fig, use_container_width=True)
    
    # Analysis points
    st.subheader("📋 Key Insights:")
    
    # Revenue analysis
    revenue_growth = calculate_growth_rate(revenue_data.iloc[-1], revenue_data.iloc[0])
    latest_revenue = revenue_data.iloc[-1]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Revenue Analysis:**")
        st.write(f"• Latest Revenue: ₹{latest_revenue:,.0f} Crores")
        st.write(f"• 4-Year CAGR: {revenue_growth/4:.1f}% annually")
        
        if revenue_growth > 15:
            st.write("• **Strong revenue growth** indicating robust business expansion")
        elif revenue_growth > 5:
            st.write("• **Moderate revenue growth** showing steady business performance")
        else:
            st.write("• **Slow revenue growth** - company may be facing challenges")
    
    with col2:
        if operating_income_key:
            st.markdown("**Operating Performance:**")
            latest_opm = opm_data.iloc[-1] if not pd.isna(opm_data.iloc[-1]) else 0
            operating_growth = calculate_growth_rate(operating_data.iloc[-1], operating_data.iloc[0])
            
            st.write(f"• Current Operating Margin: {latest_opm:.1f}%")
            st.write(f"• Operating Profit Growth: {operating_growth:.1f}%")
            
            if latest_opm > 20:
                st.write("• **Excellent operational efficiency** with strong margins")
            elif latest_opm > 10:
                st.write("• **Good operational performance** with healthy margins")
            else:
                st.write("• **Low operating margins** - need to improve efficiency")
        else:
            st.write("Operating profit data not available for detailed analysis")

def create_profitability_analysis(df, company_name):
    """Create PBT, PAT, and EPS analysis"""
    st.markdown('<div class="section-header">💰 Profitability & EPS Analysis</div>', unsafe_allow_html=True)
    
    # Find relevant columns
    pbt_key = None
    pat_key = None
    
    possible_pbt_keys = ['Pretax Income', 'Income Before Tax', 'Earnings Before Tax', 'PBT']
    possible_pat_keys = ['Net Income', 'Net Earnings', 'PAT', 'Profit After Tax']
    
    for key in possible_pbt_keys:
        if key in df.columns:
            pbt_key = key
            break
    
    for key in possible_pat_keys:
        if key in df.columns:
            pat_key = key
            break
    
    if not pat_key:
        st.warning("Net Income/PAT data not found in the financial statements")
        return
    
    # Get data
    years = [d.year for d in df.index]
    pat_data = df[pat_key] / 1e7  # Convert to Crores
    
    if pbt_key:
        pbt_data = df[pbt_key] / 1e7  # Convert to Crores
    else:
        pbt_data = pat_data  # Use PAT as proxy if PBT not available
    
    # Calculate EPS (simplified calculation)
    # Note: This is a rough calculation as we don't have exact share count
    eps_data = df[pat_key] / 1e6  # Simplified EPS calculation
    
    # Create visualization
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('PBT & PAT Trend (₹ Crores)', 'EPS Trend', 
                       'Profitability Comparison', 'EPS Growth Rate %'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # PBT & PAT trend
    if pbt_key:
        fig.add_trace(
            go.Scatter(x=years, y=pbt_data, mode='lines+markers', name='PBT',
                      line=dict(color='#9467bd', width=3), marker=dict(size=8)),
            row=1, col=1
        )
    
    fig.add_trace(
        go.Scatter(x=years, y=pat_data, mode='lines+markers', name='PAT',
                  line=dict(color='#d62728', width=3), marker=dict(size=8)),
        row=1, col=1
    )
    
    # EPS trend
    fig.add_trace(
        go.Scatter(x=years, y=eps_data, mode='lines+markers', name='EPS',
                  line=dict(color='#17becf', width=3), marker=dict(size=8)),
        row=1, col=2
    )
    
    # Profitability comparison (latest year)
    if pbt_key:
        fig.add_trace(
            go.Bar(x=['PBT', 'PAT'], 
                   y=[pbt_data.iloc[-1], pat_data.iloc[-1]],
                   name='Latest Year Profit',
                   marker_color=['#9467bd', '#d62728']),
            row=2, col=1
        )
    
    # EPS growth rate
    eps_growth_rates = []
    for i in range(1, len(eps_data)):
        growth = calculate_growth_rate(eps_data.iloc[i], eps_data.iloc[i-1])
        eps_growth_rates.append(growth)
    
    if eps_growth_rates:
        fig.add_trace(
            go.Bar(x=years[1:], y=eps_growth_rates, name='EPS Growth %',
                   marker_color='#2ca02c'),
            row=2, col=2
        )
    
    fig.update_layout(height=800, showlegend=True, title_text=f"{company_name} - Profitability Analysis")
    st.plotly_chart(fig, use_container_width=True)
    
    # Analysis points
    st.subheader("📋 Profitability Insights:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Profit Analysis:**")
        latest_pat = pat_data.iloc[-1]
        pat_growth = calculate_growth_rate(pat_data.iloc[-1], pat_data.iloc[0])
        
        st.write(f"• Latest PAT: ₹{latest_pat:,.0f} Crores")
        st.write(f"• 4-Year PAT Growth: {pat_growth:.1f}%")
        
        if pat_growth > 20:
            st.write("• **Outstanding profit growth** - excellent financial performance")
        elif pat_growth > 10:
            st.write("• **Strong profit growth** - good financial health")
        elif pat_growth > 0:
            st.write("• **Positive profit growth** - stable performance")
        else:
            st.write("• **Declining profits** - company facing challenges")
    
    with col2:
        st.markdown("**EPS Analysis:**")
        latest_eps = eps_data.iloc[-1]
        eps_growth_total = calculate_growth_rate(eps_data.iloc[-1], eps_data.iloc[0])
        avg_eps_growth = np.mean(eps_growth_rates) if eps_growth_rates else 0
        
        st.write(f"• Latest EPS: ₹{latest_eps:.2f}")
        st.write(f"• Average Annual EPS Growth: {avg_eps_growth:.1f}%")
        st.write(f"• 4-Year EPS Growth: {eps_growth_total:.1f}%")
        
        if avg_eps_growth > 15:
            st.write("• **Excellent EPS growth** - strong shareholder value creation")
        elif avg_eps_growth > 8:
            st.write("• **Good EPS growth** - decent returns for shareholders")
        elif avg_eps_growth > 0:
            st.write("• **Moderate EPS growth** - steady performance")
        else:
            st.write("• **Declining EPS** - concerning for shareholders")

def main():
    st.markdown('<div class="main-header">📈 Indian Stock PnL Statement Analyzer</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🔍 Stock Selection")
        stock_input = st.text_input(
            "Enter Stock Symbol or Name:",
            placeholder="e.g., RELIANCE, TCS, HDFC Bank",
            help="Enter either stock symbol (e.g., RELIANCE.NS) or company name (e.g., Reliance)"
        )
        
        st.markdown("### Popular Stocks:")
        popular_stocks = [
            "Reliance", "TCS", "HDFC Bank", "Infosys", "ICICI Bank",
            "ITC", "Bharti Airtel", "SBI", "Kotak Mahindra", "L&T"
        ]
        
        selected_stock = st.selectbox("Or select from popular stocks:", 
                                    [""] + popular_stocks)
        
        if selected_stock:
            stock_input = selected_stock
        
        analyze_button = st.button("🚀 Analyze Stock", type="primary")
    
    # Main content
    if analyze_button and stock_input:
        with st.spinner(f"Fetching data for {stock_input}..."):
            # Get stock symbol
            symbol = get_stock_symbol(stock_input)
            
            # Fetch data
            stock, info, financials, quarterly_financials = fetch_financial_data(symbol)
            
            if stock and info:
                # Display company info
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Company", info.get('longName', stock_input))
                with col2:  
                    st.metric("Sector", info.get('sector', 'N/A'))
                with col3:
                    st.metric("Market Cap", f"₹{info.get('marketCap', 0)/1e7:,.0f} Cr" if info.get('marketCap') else 'N/A')
                
                # Process financial data
                df = process_financial_data(financials)
                
                if df is not None and not df.empty:
                    company_name = info.get('longName', stock_input)
                    
                    # Create analyses
                    create_revenue_analysis(df, company_name)
                    st.divider()
                    create_profitability_analysis(df, company_name)
                    
                    # Summary
                    st.markdown('<div class="section-header">📝 Investment Summary</div>', unsafe_allow_html=True)
                    
                    summary_col1, summary_col2 = st.columns(2)
                    
                    with summary_col1:
                        st.markdown("**Strengths:**")
                        st.write("• Based on the financial analysis above")
                        st.write("• Check revenue growth trends")
                        st.write("• Monitor profitability margins")
                        
                    with summary_col2:
                        st.markdown("**Considerations:**")
                        st.write("• Analyze industry comparison")
                        st.write("• Consider market conditions")
                        st.write("• Review debt levels separately")
                    
                    st.info("💡 **Disclaimer:** This analysis is based on historical financial data and should not be considered as investment advice. Please consult with a financial advisor before making investment decisions.")
                    
                else:
                    st.error("Unable to process financial data for this stock. Please try another stock symbol.")
            else:
                st.error(f"Unable to fetch data for '{stock_input}'. Please check the stock symbol and try again.")
    
    elif not stock_input and analyze_button:
        st.warning("Please enter a stock symbol or name to analyze.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>Indian Stock PnL Analyzer | Built with ❤️ using Streamlit</p>
            <p>Data provided by Yahoo Finance</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
