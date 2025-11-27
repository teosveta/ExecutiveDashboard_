# Executive Business Performance Dashboard

A comprehensive, interactive business intelligence dashboard built with Python and Streamlit that transforms raw business data into actionable strategic insights for executive decision-making.

![Dashboard Screenshot](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.51.0-FF4B4B.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Overview

This executive-focused dashboard consolidates revenue, customer, operational, and financial metrics into a unified intelligence platform. Designed for business leaders who need real-time visibility into company health, the system enables rapid, data-driven decision-making through advanced analytics, predictive forecasting, and scenario modeling.

## Key Features

### 📊 Executive Overview Dashboard
- **Real-time KPI Monitoring** - Track critical business metrics with dynamic percentage changes
- **Performance Alerts** - Automated detection of significant deviations from baseline performance
- **Multi-dimensional Analysis** - Department, product, and regional performance breakdowns
- **Interactive Visualizations** - Drill-down capabilities with Plotly charts

### 🔮 Predictive Analytics
- **Multiple Forecasting Models**
  - Linear Regression with R² scoring
  - Facebook Prophet for seasonal patterns
  - ARIMA for time-series analysis
  - Polynomial regression for non-linear trends
  - Moving averages and exponential smoothing
- **Model Comparison** - Side-by-side evaluation of forecasting methods
- **Confidence Intervals** - Statistical confidence ranges for predictions
- **Trend Detection** - Automated identification of upward, downward, and stable trends

### 🎯 Scenario Modeling
- **Revenue Growth Projections** - Compound growth modeling over custom time periods
- **What-If Analysis** - Multi-metric scenario simulation
- **Break-Even Analysis** - Cost-volume-profit modeling with visual breakdowns
- **Sensitivity Analysis** - Impact assessment of percentage changes across metrics

### 📈 Advanced Analytics
- **Custom Chart Builder** - User-defined visualizations (line, bar, area, scatter, pie)
- **Multi-Metric Comparisons** - Trend lines, grouped bars, and stacked visualizations
- **Statistical Summaries** - Descriptive statistics with quartile analysis
- **Data Quality Validation** - Automated checks for missing data and anomalies

### 💾 Data Management
- **Flexible Data Import** - CSV and Excel file support
- **Database Persistence** - PostgreSQL-backed data storage
- **Sample Datasets** - Pre-loaded finance, sales, operations, and startup growth data
- **Export Capabilities** - Download processed data and statistical summaries

## Technology Stack

### Core Framework
- **Python 3.11+** - Primary development language
- **Streamlit 1.51.0** - Interactive web application framework

### Data Processing & Analysis
- **Pandas 2.3.3** - Data manipulation and time-series handling
- **NumPy 2.3.5** - Numerical computations

### Machine Learning & Forecasting
- **scikit-learn 1.7.2** - Regression models and forecasting algorithms
- **Prophet 1.2.1** - Facebook's time-series forecasting library
- **statsmodels 0.14.5** - ARIMA and statistical analysis

### Visualization
- **Plotly 6.5.0** - Interactive charting and visualizations

### Database & Persistence
- **SQLAlchemy 2.0.44** - ORM for database operations
- **psycopg2-binary 2.9.11** - PostgreSQL adapter

### Additional Libraries
- **openpyxl 3.1.5** - Excel file processing
- **reportlab 4.4.5** - PDF report generation

## Installation

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/executive-boardroom.git
cd executive-boardroom
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

Or install from pyproject.toml:
```bash
pip install -e .
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Access the dashboard**
Open your browser and navigate to `http://localhost:8501`

## Project Structure

```
executive-boardroom/
├── app.py                      # Main Streamlit application
├── main.py                     # Entry point
├── pyproject.toml              # Project configuration
├── uv.lock                     # Dependency lock file
├── utils/
│   ├── __init__.py
│   ├── data_processor.py       # Data validation and processing
│   ├── data_storage.py         # Database CRUD operations
│   ├── database.py             # SQLAlchemy models
│   ├── forecasting.py          # Forecasting algorithms
│   ├── sample_data.py          # Synthetic data generation
│   ├── scenario_modeling.py    # What-if analysis and modeling
│   └── visualizations.py       # Plotly chart creation
└── README.md
```

## Usage Guide

### Loading Data

**Option 1: Demo Data**
1. Navigate to the Home page
2. Select a sample dataset (Finance, Sales, Operations, or Startup Growth)
3. Click "Load Demo Data"

**Option 2: Upload Custom Data**
1. Prepare a CSV or Excel file with your business metrics
2. Ensure it includes columns like: Date, Revenue, Expenses, Customers, Department, Product
3. Upload via the file uploader on the Home page
4. Review the validation report
5. Click "Use This Data" if validation passes

### Navigating the Dashboard

**Executive Overview**
- View KPIs and performance metrics
- Filter by date range (Last 7/30/90 days or All Time)
- Review automated performance alerts
- Analyze department, product, and regional breakdowns

**Drill-Down Analytics**
- Build custom visualizations
- Compare multiple metrics
- View statistical summaries

**Forecasting**
- Select a metric to forecast
- Choose forecast periods (7-90 days)
- Select forecasting method (Auto recommended)
- Compare multiple models side-by-side
- Analyze trends and growth rates

**Scenario Modeling**
- Project revenue growth with custom rates
- Run what-if analyses on multiple metrics
- Calculate break-even points

**Data Management**
- Save datasets to database
- Load previously saved datasets
- Export data and statistics

## Key Algorithms & Methodologies

### Forecasting
- **Linear Regression**: y = mx + b using Ordinary Least Squares
- **Prophet**: Additive model with trend, seasonality, and holiday effects
- **ARIMA**: AutoRegressive Integrated Moving Average for stationary series
- **Polynomial**: Curved line fitting for non-linear patterns
- **Moving Average**: Smoothing-based simple forecasting
- **Exponential Smoothing**: Weighted recent observations

### Statistical Analysis
- **Descriptive Statistics**: Mean, standard deviation, quartiles
- **Trend Detection**: Linear regression slope analysis
- **Volatility Measurement**: Coefficient of variation
- **Alert Detection**: Deviation from rolling averages

### Business Modeling
- **Compound Growth**: R(n) = R₀ × (1 + r)ⁿ
- **Break-Even Analysis**: Fixed Costs / Contribution Margin
- **Percentage Adjustments**: Multiplicative scenario modeling

## Database Schema

The application uses PostgreSQL with the following tables:

- **datasets** - Stores uploaded and generated datasets
- **forecast_results** - Saves forecasting outputs and parameters
- **alerts** - Tracks performance alerts and thresholds
- **analytics_results** - Archives custom analytics queries
- **data_connections** - Manages external data source configurations

## Configuration

### Environment Variables
```bash
DATABASE_URL=postgresql://user:password@host:port/dbname
```

### Streamlit Configuration
Customize appearance and behavior by creating `.streamlit/config.toml`:

```toml
[server]
headless = true
address = "localhost"
port = 8501

[theme]
primaryColor = "#1a2a6c"
backgroundColor = "#f5f7fa"
secondaryBackgroundColor = "#ffffff"
textColor = "#1a2a6c"
```

## Performance Considerations

- **Data Limits**: Optimized for datasets up to 100K rows
- **Forecasting**: Requires minimum 10 data points for basic models, 15+ for polynomial
- **Caching**: Streamlit caching enabled for data processing functions
- **Database**: Connection pooling for efficient multi-user access

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **Streamlit** - For the excellent web framework
- **Facebook Prophet** - For advanced time-series forecasting
- **Plotly** - For interactive visualizations
- **scikit-learn** - For machine learning algorithms

## Contact

For questions, feedback, or collaboration opportunities, please open an issue on GitHub.

---

**Built with Python 🐍 | Powered by Streamlit ⚡ | Designed for Business Leaders 📊**
