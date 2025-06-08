# Indian Stock PnL Statement Analyzer 📈

A comprehensive Streamlit web application for analyzing Indian stock Profit & Loss statements with interactive visualizations and detailed insights.

## 🚀 Features

### 1. Revenue & Operating Performance Analysis
- **Revenue Trends**: 4-year revenue growth visualization
- **Operating Profit Analysis**: Operating profit trends and margins
- **Operating Profit Margin (OPM)**: Percentage analysis with trends
- **Visual Representations**: Interactive charts and graphs
- **Key Insights**: Automated bullet-point analysis

### 2. Profitability & EPS Analysis
- **PBT (Profit Before Tax)**: Trend analysis over 4 years
- **PAT (Profit After Tax)**: Net income analysis
- **EPS (Earnings Per Share)**: Per-share earnings trends
- **EPS Growth Rate**: Year-over-year growth analysis
- **Interactive Charts**: Comprehensive visual representation

### 3. Smart Stock Recognition
- Enter stock symbols (e.g., RELIANCE.NS, TCS.NS)
- Enter company names (e.g., "Reliance", "TCS", "HDFC Bank")
- Popular stocks dropdown for quick selection
- Auto-formatting for Indian stock exchanges (NSE/BSE)

## 🛠️ Installation & Setup

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/indian-stock-analyzer.git
cd indian-stock-analyzer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Access the app**
Open your browser and go to `http://localhost:8501`

### Deploy to Streamlit Cloud (Free)

1. **Fork this repository** to your GitHub account
2. **Go to [Streamlit Cloud](https://share.streamlit.io/)**
3. **Click "New app"**
4. **Connect your GitHub repository**
5. **Set the following:**
   - Repository: `yourusername/indian-stock-analyzer`
   - Branch: `main`
   - Main file path: `app.py`
6. **Click "Deploy"**

Your app will be live at: `https://yourusername-indian-stock-analyzer-app-xxxxx.streamlit.app/`

## 📊 Supported Analysis

### Revenue Metrics
- Total Revenue/Net Sales
- Revenue Growth Rate (4-year CAGR)
- Year-over-year revenue trends
- Revenue performance insights

### Operating Performance
- Operating Income/EBIT
- Operating Profit Margin (OPM)
- Operating efficiency analysis
- Margin trend analysis

### Profitability Metrics
- Profit Before Tax (PBT)
- Profit After Tax (PAT)
- Net profit margins
- Profitability trends

### EPS Analysis
- Earnings Per Share calculation
- EPS growth rates
- Year-over-year EPS trends
- Shareholder value analysis

## 🏢 Supported Indian Stocks

The app supports all NSE and BSE listed stocks. Popular pre-configured stocks include:

- **Banking**: HDFC Bank, ICICI Bank, SBI, Axis Bank, Kotak Mahindra Bank
- **IT**: TCS, Infosys, Wipro
- **Conglomerates**: Reliance Industries, ITC, L&T
- **Telecom**: Bharti Airtel
- **Auto**: Maruti Suzuki
- **FMCG**: Nestle India, Asian Paints
- **Pharma**: Sun Pharma
- **Materials**: UltraTech Cement

## 📱 Usage Guide

### Step 1: Enter Stock Information
- Type the stock symbol (e.g., "RELIANCE.NS") or company name (e.g., "Reliance")
- Or select from the popular stocks dropdown

### Step 2: Click Analyze
- Click the "🚀 Analyze Stock" button
- Wait for data fetching and processing

### Step 3: Review Analysis
- **Company Overview**: Basic company information
- **Revenue Analysis**: Revenue trends and operating performance
- **Profitability Analysis**: PBT, PAT, and EPS insights
- **Investment Summary**: Key strengths and considerations

## 🔧 Technical Details

### Data Source
- **Yahoo Finance API**: Real-time and historical financial data
- **yfinance Library**: Python wrapper for Yahoo Finance API
- **Data Coverage**: Last 4 years of annual financial statements

### Visualization
- **Plotly**: Interactive charts and graphs
- **Multiple Chart Types**: Line charts, bar charts, subplots
- **Responsive Design**: Works on desktop and mobile

### Calculations
- **Growth Rates**: CAGR and year-over-year calculations
- **Ratios**: Operating margins, profit margins
- **EPS**: Simplified earnings per share calculation

## ⚠️ Important Disclaimers

1. **Not Investment Advice**: This tool provides analytical insights based on historical data and should not be considered as investment advice.

2. **Data Limitations**: 
   - Data sourced from Yahoo Finance may have delays
   - Some companies may have limited data availability
   - Calculations are simplified for educational purposes

3. **Professional Consultation**: Always consult with qualified financial advisors before making investment decisions.

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📋 Future Enhancements

- [ ] Add debt analysis section
- [ ] Include cash flow statement analysis
- [ ] Peer comparison features
- [ ] Export analysis reports (PDF)
- [ ] Email alerts for stock updates
- [ ] Portfolio tracking
- [ ] Technical analysis integration

## 🐛 Known Issues

- Some stocks may have limited financial data availability
- EPS calculation is simplified and may not match exact reported EPS
- Data refresh depends on Yahoo Finance API availability

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/indian-stock-analyzer/issues) page
2. Create a new issue with detailed description
3. Include error messages and stock symbols that caused issues

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Yahoo Finance** for providing financial data API
- **Streamlit** for the amazing web app framework
- **Plotly** for interactive visualization capabilities
- **Indian Stock Market** community for inspiration

---

**Built with ❤️ for Indian Stock Market Analysis**

*Happy Investing! 📈*
