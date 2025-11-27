import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os
import plotly.graph_objects as go

sys.path.append(os.path.dirname(__file__))

from utils.sample_data import get_sample_dataset, get_dataset_description
from utils.data_processor import DataProcessor
from utils.forecasting import ForecastingEngine
from utils.visualizations import DashboardVisualizations
from utils.scenario_modeling import ScenarioModeler
from utils.database import init_db
from utils.data_storage import DataStorage

init_db()

st.set_page_config(
    page_title="Executive Business Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    }
    .stApp {
        background: #f5f7fa;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a2a6c 0%, #0f2027 100%);
        border-right: 3px solid #d4af37;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    .metric-card {
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
        border-left: 4px solid #d4af37;
    }
    .hero-section {
        background: linear-gradient(135deg, #1a2a6c 0%, #0f2027 100%);
        padding: 70px 30px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 40px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
    }
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(212, 175, 55, 0.1) 0%, transparent 100%);
        pointer-events: none;
    }
    .feature-card {
        background: linear-gradient(135deg, rgba(26, 42, 108, 0.95) 0%, rgba(15, 32, 39, 0.95) 100%);
        backdrop-filter: blur(10px);
        padding: 35px;
        border-radius: 15px;
        margin: 20px 0;
        border: 2px solid rgba(212, 175, 55, 0.3);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(212, 175, 55, 0.3);
        border-color: rgba(212, 175, 55, 0.6);
    }
    .feature-card h3 {
        color: #d4af37 !important;
        font-size: 1.3em !important;
        margin-bottom: 15px !important;
        font-weight: 700 !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    .feature-card p {
        color: #ffffff !important;
        font-size: 1.05em !important;
        line-height: 1.6 !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
    }
    h1, h2, h3 {
        color: #1a2a6c;
    }
    .stButton>button {
        background: linear-gradient(135deg, #1a2a6c 0%, #0f2027 100%);
        color: white;
        border: 2px solid #d4af37;
        padding: 12px 35px;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #d4af37 0%, #c9a942 100%);
        color: #1a2a6c;
        border-color: #1a2a6c;
        box-shadow: 0 6px 16px rgba(212, 175, 55, 0.4);
        transform: translateY(-2px);
    }
    .page-header {
        background: linear-gradient(135deg, #1a2a6c 0%, #0f2027 100%);
        padding: 25px 35px;
        border-radius: 12px;
        margin-bottom: 35px;
        color: white;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
        border-left: 5px solid #d4af37;
    }
    .page-header h1 {
        color: white !important;
        margin-bottom: 8px;
    }
    .breadcrumb {
        color: rgba(212, 175, 55, 0.9);
        font-size: 0.95em;
        font-weight: 500;
    }
    .data-status-banner {
        background: linear-gradient(135deg, #fff9e6 0%, #fff3cd 100%);
        border-left: 5px solid #d4af37;
        padding: 25px;
        border-radius: 10px;
        margin: 20px 0;
        font-size: 1.1em;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
    }
    .data-status-banner.success {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left-color: #28a745;
    }
    .help-tooltip {
        background: linear-gradient(135deg, #e7f3ff 0%, #d9eeff 100%);
        border-left: 4px solid #1a2a6c;
        padding: 18px;
        border-radius: 8px;
        margin: 12px 0;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.08);
    }
    div[data-testid="stMetricValue"] {
        font-size: 2em;
        font-weight: 700;
        color: #1a2a6c;
    }
    div[data-testid="stMetricDelta"] {
        font-size: 1.1em;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

if 'data' not in st.session_state:
    st.session_state.data = None
if 'data_source' not in st.session_state:
    st.session_state.data_source = None
if 'validation_report' not in st.session_state:
    st.session_state.validation_report = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Home'
if 'current_dataset_id' not in st.session_state:
    st.session_state.current_dataset_id = None

def show_page_header(title, description="", icon=""):
    """Display a consistent page header with breadcrumb navigation"""
    breadcrumb = f"Home > {st.session_state.current_page}"
    st.markdown(f"""
        <div class="page-header">
            <div class="breadcrumb">{breadcrumb}</div>
            <h1>{icon} {title}</h1>
            <p style="margin: 0; font-size: 1.1em;">{description}</p>
        </div>
    """, unsafe_allow_html=True)

def show_home_page():
    st.markdown("""
        <div class="hero-section">
            <h1 style="color: white; font-size: 3em; margin-bottom: 20px;">Executive Business Performance Dashboard</h1>
            <p style="font-size: 1.3em; margin-bottom: 30px;">Transform Data into Actionable Insights</p>
            <p style="font-size: 1.1em;">Experience an interactive journey from raw data to strategic intelligence. Monitor KPIs, forecast trends, and simulate scenarios in real-time.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <h3 style="color: white;">📤 Smart Data Processing</h3>
                <p style="color: white;">Upload CSV files or use demo data with automated validation and cleaning</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-card">
                <h3 style="color: white;">📈 Predictive Analytics</h3>
                <p style="color: white;">Forecast revenue, model scenarios, and track trends with advanced algorithms</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="feature-card">
                <h3 style="color: white;">🎯 Interactive Insights</h3>
                <p style="color: white;">Drill-down dashboards with real-time KPI monitoring and performance alerts</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.header("📊 Choose Your Data Source")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📦 Use Demo Data")
        st.write("Explore with pre-loaded business metrics and sample data")

        st.markdown("""
            <div class="help-tooltip">
                <strong>💡 New to dashboards?</strong> Start here! Demo data lets you explore all features without uploading files.
            </div>
        """, unsafe_allow_html=True)

        demo_options = ['Finance', 'Sales', 'Operations', 'Startup Growth']
        selected_demo = st.selectbox("Select Sample Dataset:", demo_options,
                                     help="Choose a dataset that matches your business type for the most relevant insights")

        if selected_demo:
            desc = get_dataset_description(selected_demo)
            st.info(f"**{desc['title']}**\n\n{desc['description']}")
            st.write(f"📅 {desc['time_range']}")
            st.write(f"📊 Key Metrics: {', '.join(desc['metrics'][:3])}")

            with st.expander("🔬 How Demo Data is Generated", expanded=False):
                st.markdown("""
                **Synthetic Data Generation Process:**

                **Mathematical Components:**
                1. **Base Value** - Starting point for the metric
                2. **Growth Trend** - Linear/exponential increase over time
                   - Formula: `np.linspace(start, end, periods)`
                3. **Seasonal Pattern** - Yearly cyclical variations
                   - Formula: `A × sin(2π × t / 365.25)`
                   - Creates realistic peaks and valleys
                4. **Weekly Cycles** - Day-of-week patterns
                   - Formula: `A × sin(2π × t / 7)`
                5. **Random Noise** - Natural variability
                   - Formula: `np.random.normal(μ=0, σ)`

                **Example Composition:**
                ```
                Revenue = Base + Trend + Seasonal + Weekly + Noise
                       = 120,000 + growth + 15,000×sin(...) + 8,000×sin(...) + random
                ```

                **Correlations:**
                - Expenses correlate with revenue (realistic business behavior)
                - Customer growth affects revenue
                - Metrics have realistic relationships

                **Library**: NumPy for mathematical functions, Pandas for data structure

                **Result**: Realistic business data patterns for testing and learning
                """)


        if st.button("Load Demo Data", key="load_demo"):
            st.session_state.data = get_sample_dataset(selected_demo)
            st.session_state.data_source = f"Demo: {selected_demo}"
            st.toast(f"✅ Successfully loaded {selected_demo} dataset with {len(st.session_state.data):,} records!", icon="✅")
            st.success(f"✅ Loaded {selected_demo} dataset with {len(st.session_state.data)} records!")
            st.rerun()
    
    with col2:
        st.subheader("📁 Upload Your Data")
        st.write("Import CSV files with your business metrics")

        st.markdown("""
            <div class="help-tooltip">
                <strong>📋 File Format Tips:</strong> Include columns like Date, Revenue, Expenses, Customers, Department, or Product for best results.
            </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Select CSV or Excel File",
            type=['csv', 'xlsx', 'xls'],
            help="Upload a file with columns like Date, Revenue, Department, Customers, etc. The system will automatically detect and validate your data structure."
        )
        
        if uploaded_file:
            with st.expander("🔍 Data Validation Process", expanded=False):
                st.markdown("""
                **Automated Data Validation Pipeline:**

                **Step 1: File Format Detection**
                - Supports: CSV, Excel (.xlsx, .xls)
                - Uses: Pandas `read_csv()` or `read_excel()`

                **Step 2: Data Quality Checks**
                1. **Structure Validation**
                   - Checks for minimum rows (>= 10)
                   - Verifies column presence
                   - Detects data types

                2. **Column Analysis**
                   - Identifies numeric columns (for metrics)
                   - Detects date/time columns (for time-series)
                   - Finds categorical columns (for grouping)

                3. **Missing Data Detection**
                   - Counts null/NaN values per column
                   - Calculates missing data percentage
                   - Warns if > 30% missing in key columns

                4. **Data Type Inference**
                   - Auto-detects and converts date formats
                   - Parses numeric strings to numbers
                   - Identifies categorical variables

                **Step 3: Data Cleaning**
                - Removes completely empty rows
                - Standardizes column names (spaces, special chars)
                - Converts date strings to datetime objects

                **Step 4: Validation Report**
                - ✅ Valid: Data meets minimum requirements
                - ⚠️ Warnings: Issues that don't block usage
                - ❌ Errors: Critical issues preventing analysis

                **Libraries**: Pandas (data manipulation), NumPy (numerical operations)
                """)

            processor = DataProcessor()
            data, validation_report = processor.process_uploaded_data(uploaded_file)

            if validation_report['valid']:
                st.success("✅ File validated successfully!")
                st.info(f"📊 {validation_report['info']['rows']} rows × {validation_report['info']['columns']} columns")
                
                if validation_report['warnings']:
                    with st.expander("⚠️ Validation Warnings"):
                        for warning in validation_report['warnings']:
                            st.warning(warning)
                
                if st.button("Use This Data", key="use_upload"):
                    st.session_state.data = data
                    st.session_state.data_source = f"Uploaded: {uploaded_file.name}"
                    st.session_state.validation_report = validation_report
                    st.toast(f"✅ Successfully loaded {uploaded_file.name} with {len(data):,} records!", icon="✅")
                    st.success("✅ Data loaded successfully!")
                    st.rerun()
            else:
                st.error("❌ File validation failed!")
                for error in validation_report['errors']:
                    st.error(error)

def show_executive_overview():
    show_page_header(
        "Executive Overview",
        "Monitor key performance indicators and business metrics at a glance",
        "📊"
    )

    if st.session_state.data is None:
        st.markdown("""
            <div class="data-status-banner">
                <h3 style="margin-top: 0;">⚠️ No Data Loaded</h3>
                <p>Please load data from the <strong>Home</strong> page first to view your executive dashboard.</p>
                <p style="margin-bottom: 0;">You can use demo data or upload your own CSV/Excel file.</p>
            </div>
        """, unsafe_allow_html=True)
        return

    df = st.session_state.data

    st.markdown(f"""
        <div class="data-status-banner success">
            <strong>✅ Data Loaded:</strong> {st.session_state.data_source} ({len(df):,} records)
        </div>
    """, unsafe_allow_html=True)
    
    processor = DataProcessor()
    key_metrics = processor.detect_key_metrics(df)
    
    date_col = key_metrics['date_columns'][0] if key_metrics['date_columns'] else None
    
    if date_col and date_col in df.columns:
        df_sorted = df.sort_values(date_col)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader("📅 Date Range Filter")
        with col2:
            date_range = st.selectbox("Period", ["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"], index=3)
        
        if date_range != "All Time":
            days_map = {"Last 7 Days": 7, "Last 30 Days": 30, "Last 90 Days": 90}
            days = days_map[date_range]
            cutoff_date = df_sorted[date_col].max() - pd.Timedelta(days=days)
            df_filtered = df_sorted[df_sorted[date_col] >= cutoff_date]
        else:
            df_filtered = df_sorted
    else:
        df_filtered = df
    
    st.markdown("### 📈 Key Performance Indicators")

    with st.expander("📊 How KPIs are Calculated", expanded=False):
        st.markdown("""
        **Metric Calculation Method:**
        - **Current Value**: Latest data point in the filtered dataset
        - **Previous Value**: First data point in the filtered dataset (baseline)
        - **Change Percentage**: `((Current - Previous) / Previous) × 100`

        **Statistical Approach:**
        - Uses simple percentage change to show growth or decline
        - Positive delta (green) indicates improvement
        - Negative delta (red) indicates decline
        - Handles division by zero gracefully

        **Note**: KPIs update dynamically based on your date range filter selection.
        """)

    numeric_cols = df_filtered.select_dtypes(include=[np.number]).columns.tolist()
    
    kpi_cols = []
    for col in numeric_cols[:4]:
        if 'id' not in col.lower():
            kpi_cols.append(col)
    
    cols = st.columns(len(kpi_cols) if kpi_cols else 1)
    
    for idx, col in enumerate(kpi_cols):
        with cols[idx]:
            current_value = df_filtered[col].iloc[-1] if len(df_filtered) > 0 else 0
            previous_value = df_filtered[col].iloc[0] if len(df_filtered) > 1 else current_value
            
            change = current_value - previous_value
            change_pct = (change / previous_value * 100) if previous_value != 0 else 0
            
            st.metric(
                label=col.replace('_', ' ').title(),
                value=f"{current_value:,.0f}" if abs(current_value) > 100 else f"{current_value:.2f}",
                delta=f"{change_pct:+.1f}%"
            )
    
    st.markdown("---")
    
    viz = DashboardVisualizations()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Revenue Trend")
        revenue_col = None
        for col in key_metrics['revenue_columns']:
            if col in df_filtered.columns:
                revenue_col = col
                break
        
        if not revenue_col and numeric_cols:
            revenue_col = numeric_cols[0]
        
        if revenue_col and date_col:
            trend_df = df_filtered.groupby(date_col)[revenue_col].sum().reset_index()
            fig = viz.create_area_chart(trend_df, date_col, revenue_col, f"{revenue_col} Over Time")
            st.plotly_chart(fig, use_container_width=True)
        elif revenue_col:
            st.line_chart(df_filtered[revenue_col].tail(50))
    
    with col2:
        st.subheader("📊 Department Performance")
        if 'Department' in df_filtered.columns and revenue_col:
            dept_df = df_filtered.groupby('Department')[revenue_col].sum().reset_index()
            dept_df = dept_df.sort_values(revenue_col, ascending=False)
            fig = viz.create_bar_chart(dept_df, 'Department', revenue_col, "Performance by Department")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Department column not found in data")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Product Distribution")
        if 'Product' in df_filtered.columns and revenue_col:
            product_df = df_filtered.groupby('Product')[revenue_col].sum().reset_index()
            fig = viz.create_pie_chart(product_df, 'Product', revenue_col, "Revenue by Product")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Product column not found in data")
    
    with col2:
        st.subheader("🌍 Regional Analysis")
        if 'Region' in df_filtered.columns and revenue_col:
            region_df = df_filtered.groupby('Region')[revenue_col].sum().reset_index()
            region_df = region_df.sort_values(revenue_col, ascending=False)
            fig = viz.create_bar_chart(region_df, 'Region', revenue_col, "Performance by Region", orientation='h')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Region column not found in data")
    
    st.markdown("---")
    st.subheader("🔔 Performance Alerts")

    with st.expander("📊 Alert Detection Methodology", expanded=False):
        st.markdown("""
        **Statistical Alert System:**

        **Algorithm:**
        1. **Recent Average**: Mean of last 7 data points
        2. **Overall Average**: Mean of entire dataset
        3. **Deviation Calculation**: `((Recent Avg - Overall Avg) / Overall Avg) × 100`

        **Alert Threshold:**
        - Alerts trigger when deviation exceeds ±10%
        - **Positive Alert** (📈): Recent performance > 10% above average
        - **Negative Alert** (📉): Recent performance > 10% below average

        **Purpose:**
        Identifies metrics showing significant recent changes compared to historical baseline,
        helping you spot trends, anomalies, or areas requiring attention.

        **Statistical Basis**: Moving average comparison with percentage deviation threshold.
        """)

    alerts = []
    for col in numeric_cols[:5]:
        if len(df_filtered) > 10:
            recent_avg = df_filtered[col].tail(7).mean()
            overall_avg = df_filtered[col].mean()
            
            deviation = ((recent_avg - overall_avg) / overall_avg * 100) if overall_avg != 0 else 0
            
            if abs(deviation) > 10:
                alert_type = "📈 Positive" if deviation > 0 else "📉 Negative"
                alerts.append({
                    'Metric': col.replace('_', ' ').title(),
                    'Alert': alert_type,
                    'Deviation': f"{deviation:+.1f}%",
                    'Status': 'Above Average' if deviation > 0 else 'Below Average'
                })
    
    if alerts:
        st.dataframe(pd.DataFrame(alerts), use_container_width=True, hide_index=True)
    else:
        st.info("All metrics are performing within normal ranges")

def show_analytics_page():
    show_page_header(
        "Drill-Down Analytics",
        "Build custom visualizations and perform multi-metric comparisons",
        "🔍"
    )

    if st.session_state.data is None:
        st.markdown("""
            <div class="data-status-banner">
                <h3 style="margin-top: 0;">⚠️ No Data Loaded</h3>
                <p>Please load data from the <strong>Home</strong> page first to access analytics.</p>
                <p style="margin-bottom: 0;">You can use demo data or upload your own CSV/Excel file.</p>
            </div>
        """, unsafe_allow_html=True)
        return

    df = st.session_state.data

    st.markdown(f"""
        <div class="data-status-banner success">
            <strong>✅ Data Loaded:</strong> {st.session_state.data_source} ({len(df):,} records)
        </div>
    """, unsafe_allow_html=True)
    
    processor = DataProcessor()
    key_metrics = processor.detect_key_metrics(df)
    viz = DashboardVisualizations()
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    date_col = key_metrics['date_columns'][0] if key_metrics['date_columns'] else None

    st.markdown("""
        <div class="help-tooltip">
            <strong>🔍 Custom Analytics:</strong> Build your own visualizations by selecting chart types and data columns.
            Perfect for exploring specific relationships in your data.
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔍 Custom Analysis Builder")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        chart_type = st.selectbox("Chart Type", ["Line Chart", "Bar Chart", "Area Chart", "Scatter Plot", "Pie Chart"])
    
    with col2:
        if date_col:
            x_axis = st.selectbox("X-Axis", [date_col] + categorical_cols + numeric_cols, index=0)
        else:
            x_axis = st.selectbox("X-Axis", categorical_cols + numeric_cols)
    
    with col3:
        y_axis = st.selectbox("Y-Axis", numeric_cols)
    
    if st.button("Generate Chart"):
        if chart_type == "Line Chart":
            if date_col and x_axis == date_col:
                df_sorted = df.sort_values(date_col)
                agg_df = df_sorted.groupby(date_col)[y_axis].mean().reset_index()
                fig = viz.create_line_chart(agg_df, x_axis, y_axis, f"{y_axis} Trend")
            else:
                fig = viz.create_line_chart(df, x_axis, y_axis, f"{y_axis} by {x_axis}")
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Bar Chart":
            agg_df = df.groupby(x_axis)[y_axis].sum().reset_index().sort_values(y_axis, ascending=False)
            fig = viz.create_bar_chart(agg_df, x_axis, y_axis, f"{y_axis} by {x_axis}")
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Area Chart":
            if date_col and x_axis == date_col:
                df_sorted = df.sort_values(date_col)
                agg_df = df_sorted.groupby(date_col)[y_axis].mean().reset_index()
                fig = viz.create_area_chart(agg_df, x_axis, y_axis, f"{y_axis} Over Time")
            else:
                fig = viz.create_area_chart(df, x_axis, y_axis, f"{y_axis} by {x_axis}")
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Scatter Plot":
            fig = viz.create_scatter_plot(df, x_axis, y_axis, f"{y_axis} vs {x_axis}")
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Pie Chart":
            if x_axis in categorical_cols:
                agg_df = df.groupby(x_axis)[y_axis].sum().reset_index()
                fig = viz.create_pie_chart(agg_df, x_axis, y_axis, f"{y_axis} Distribution by {x_axis}")
                st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📊 Multi-Metric Comparison")
    
    selected_metrics = st.multiselect("Select Metrics to Compare", numeric_cols, default=numeric_cols[:3])
    
    if selected_metrics and date_col:
        df_sorted = df.sort_values(date_col)
        
        comparison_type = st.radio("Comparison Type", ["Trend Lines", "Grouped Bars", "Stacked Bars"], horizontal=True)
        
        if comparison_type == "Trend Lines":
            agg_df = df_sorted.groupby(date_col)[selected_metrics].mean().reset_index()
            fig = viz.create_multi_line_chart(agg_df, date_col, selected_metrics, "Multi-Metric Trend Analysis")
            st.plotly_chart(fig, use_container_width=True)
        
        elif comparison_type == "Grouped Bars":
            if 'Department' in df.columns:
                agg_df = df.groupby('Department')[selected_metrics].sum().reset_index()
                fig = viz.create_grouped_bar_chart(agg_df, 'Department', selected_metrics, "Department Comparison")
                st.plotly_chart(fig, use_container_width=True)
        
        elif comparison_type == "Stacked Bars":
            if 'Department' in df.columns:
                agg_df = df.groupby('Department')[selected_metrics].sum().reset_index()
                fig = viz.create_stacked_bar_chart(agg_df, 'Department', selected_metrics, "Department Composition")
                st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📋 Data Summary Statistics")

    with st.expander("📊 Statistical Measures Explained", expanded=False):
        st.markdown("""
        **Descriptive Statistics Computed:**

        | Statistic | Formula | Description |
        |-----------|---------|-------------|
        | **Count** | n | Total number of non-null values |
        | **Mean** | Σx / n | Average value (sum divided by count) |
        | **Std Dev** | √(Σ(x - μ)² / n) | Standard deviation (spread from mean) |
        | **Min** | min(x) | Minimum value in dataset |
        | **25%** | Q1 | First quartile (25th percentile) |
        | **50%** | Q2 (Median) | Middle value when sorted |
        | **75%** | Q3 | Third quartile (75th percentile) |
        | **Max** | max(x) | Maximum value in dataset |

        **Interpretation:**
        - **Mean**: Central tendency of your data
        - **Std Dev**: Higher values indicate more variability
        - **Quartiles**: Show data distribution (helps identify outliers)
        - **Min/Max**: Range of your data

        **Library Used**: Pandas `.describe()` method (built on NumPy)
        """)

    summary = processor.get_summary_statistics(df)

    if summary and 'numeric' in summary:
        st.dataframe(summary['numeric'], use_container_width=True)

def show_forecasting_page():
    show_page_header(
        "Forecasting & Predictive Analytics",
        "Generate forecasts using multiple algorithms and compare model performance",
        "🔮"
    )

    if st.session_state.data is None:
        st.markdown("""
            <div class="data-status-banner">
                <h3 style="margin-top: 0;">⚠️ No Data Loaded</h3>
                <p>Please load data from the <strong>Home</strong> page first to generate forecasts.</p>
                <p style="margin-bottom: 0;">You can use demo data or upload your own CSV/Excel file.</p>
            </div>
        """, unsafe_allow_html=True)
        return

    df = st.session_state.data

    st.markdown(f"""
        <div class="data-status-banner success">
            <strong>✅ Data Loaded:</strong> {st.session_state.data_source} ({len(df):,} records)
        </div>
    """, unsafe_allow_html=True)
    
    processor = DataProcessor()
    key_metrics = processor.detect_key_metrics(df)
    forecaster = ForecastingEngine()
    viz = DashboardVisualizations()
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    date_col = key_metrics['date_columns'][0] if key_metrics['date_columns'] else None
    
    if not date_col:
        st.warning("⚠️ Time-series forecasting requires a date column in your data.")
        return

    st.markdown("""
        <div class="help-tooltip">
            <strong>📊 How Forecasting Works:</strong> Select a metric to predict future values based on historical patterns.
            The system uses advanced algorithms to analyze trends, seasonality, and patterns in your data.
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📈 Forecast Configuration")

    with st.expander("🔮 Forecasting Methods Explained", expanded=False):
        st.markdown("""
        **Available Forecasting Algorithms:**

        **1. Auto** 🤖
        - **Method**: Automatically selects best algorithm based on data characteristics
        - **When to Use**: Not sure which method to choose
        - **Backend**: Tries multiple methods and selects highest confidence

        **2. Linear Regression** 📈
        - **Formula**: y = mx + b (where m is slope, b is intercept)
        - **Method**: Fits a straight line through data points using Ordinary Least Squares (OLS)
        - **Best For**: Data with consistent linear trends
        - **Library**: scikit-learn `LinearRegression`
        - **Output**: Includes R² score (model fit quality, 0-1 scale)

        **3. Prophet (Facebook)** 🔮
        - **Method**: Additive model: y(t) = g(t) + s(t) + h(t) + εₜ
          - g(t): Trend component
          - s(t): Seasonal component
          - h(t): Holiday effects
          - εₜ: Error term
        - **Best For**: Data with strong seasonality and multiple patterns
        - **Library**: Facebook Prophet (if installed)
        - **Features**: Handles missing data, outliers, and trend changes

        **4. ARIMA** 📊
        - **Full Name**: AutoRegressive Integrated Moving Average
        - **Model**: ARIMA(p,d,q) where:
          - p: Auto-regressive order
          - d: Differencing order
          - q: Moving average order
        - **Best For**: Stationary time series with temporal dependencies
        - **Library**: statsmodels `ARIMA`

        **5. Polynomial** 🌊
        - **Formula**: y = a₀ + a₁x + a₂x² + a₃x³ + ...
        - **Method**: Fits curved line using polynomial regression (degree 2-3)
        - **Best For**: Data with non-linear patterns or curves
        - **Library**: NumPy `polyfit` + scikit-learn

        **6. Moving Average** 📉
        - **Formula**: MA(t) = (xₜ + xₜ₋₁ + ... + xₜ₋ₙ₊₁) / n
        - **Method**: Average of last N periods, extended forward
        - **Best For**: Smoothing noisy data, simple trends
        - **Window Size**: Adaptive (7-30 days based on data)

        **7. Exponential Smoothing** 🎯
        - **Formula**: Sₜ = αxₜ + (1-α)Sₜ₋₁ (where α is smoothing factor)
        - **Method**: Weighted average giving more weight to recent observations
        - **Best For**: Data where recent values are more important
        - **Library**: statsmodels `SimpleExpSmoothing`

        **Confidence Intervals:**
        - Calculated using standard error of predictions
        - Shows range where actual values likely to fall (typically 95% confidence)
        - Formula: ŷ ± (1.96 × SE)
        """)

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_to_forecast = st.selectbox("Select Metric to Forecast", numeric_cols)

    with col2:
        forecast_periods = st.slider("Forecast Periods (days)", 7, 90, 30)

    with col3:
        forecast_method = st.selectbox("Forecast Method", ["Auto", "Linear Regression", "Prophet (Facebook)", "ARIMA", "Polynomial", "Moving Average", "Exponential Smoothing"])
    
    method_map = {
        "Auto": "auto",
        "Linear Regression": "linear",
        "Prophet (Facebook)": "prophet",
        "ARIMA": "arima",
        "Polynomial": "polynomial",
        "Moving Average": "moving_average",
        "Exponential Smoothing": "exponential"
    }
    
    df_sorted = df.sort_values(date_col)
    data_length = len(df_sorted[metric_to_forecast].dropna())
    
    st.info(f"📊 Available data points: {data_length}. Minimum required: 10 for basic forecasts, 15 for polynomial.")
    
    if st.button("Generate Forecast", type="primary"):
        with st.spinner("Generating forecast..."):
            forecast_result = forecaster.forecast_metric(
                df, 
                metric_to_forecast, 
                date_col, 
                forecast_periods, 
                method_map[forecast_method]
            )
            
            if forecast_result:
                st.success(f"✅ Forecast generated using {forecast_result['method']}")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Confidence Level", forecast_result['confidence'])
                
                with col2:
                    if 'trend' in forecast_result:
                        st.metric("Trend Direction", forecast_result['trend'])
                
                with col3:
                    if 'r2_score' in forecast_result:
                        st.metric("Model Accuracy (R²)", f"{forecast_result['r2_score']:.2f}")
                
                st.markdown("### 📊 Forecast Visualization")
                
                df_sorted = df.sort_values(date_col)
                recent_data = df_sorted[metric_to_forecast].tail(90).values
                recent_dates = df_sorted[date_col].tail(90).values
                
                if 'forecast_dates' in forecast_result:
                    forecast_dates = forecast_result['forecast_dates']
                else:
                    last_date = pd.to_datetime(df_sorted[date_col].iloc[-1])
                    forecast_dates = pd.date_range(start=last_date, periods=forecast_periods+1, freq='D')[1:]
                
                lower_bound = forecast_result.get('lower_bound')
                upper_bound = forecast_result.get('upper_bound')
                
                fig = viz.create_forecast_chart(
                    recent_data,
                    forecast_result['forecast'],
                    recent_dates,
                    forecast_dates,
                    f"{metric_to_forecast} Forecast",
                    lower_bound,
                    upper_bound
                )
                st.plotly_chart(fig, use_container_width=True)
                
                if forecast_result.get('has_confidence_interval'):
                    st.info("📊 The shaded area represents the confidence interval for the forecast.")
                
                st.markdown("### 📊 Forecast Details")
                forecast_df = pd.DataFrame({
                    'Date': forecast_dates[:len(forecast_result['forecast'])],
                    'Forecasted Value': forecast_result['forecast']
                })
                st.dataframe(forecast_df, use_container_width=True, hide_index=True)
            else:
                st.error("❌ Unable to generate forecast. Insufficient data points or the selected method requires more historical data.")
                st.info("💡 Try: (1) Using 'Auto' or 'Moving Average' methods, or (2) Loading a dataset with more historical data.")
    
    st.markdown("---")
    st.markdown("### 🔄 Model Comparison")
    st.caption("Compare multiple forecasting models side-by-side to find the best fit for your data")
    
    comparison_metric = st.selectbox("Select Metric for Comparison", numeric_cols, key="comparison_metric")
    comparison_periods = st.slider("Comparison Forecast Periods", 7, 60, 30, key="comparison_periods")
    
    if st.button("Compare Models", type="primary"):
        with st.spinner("Generating forecasts across multiple models..."):
            comparison_results = forecaster.compare_forecasts(df, comparison_metric, date_col, comparison_periods)
            
            if comparison_results:
                st.success(f"✅ Generated {len(comparison_results)} forecast models")
                
                model_metrics = []
                for method, result in comparison_results.items():
                    model_metrics.append({
                        'Model': result['method'],
                        'Confidence': result['confidence'],
                        'R² Score': result.get('r2_score', 'N/A'),
                        'Has CI': '✓' if result.get('has_confidence_interval') else '✗'
                    })
                
                metrics_df = pd.DataFrame(model_metrics)
                st.dataframe(metrics_df, use_container_width=True, hide_index=True)
                
                df_sorted = df.sort_values(date_col)
                recent_data = df_sorted[comparison_metric].tail(60).values
                recent_dates = df_sorted[date_col].tail(60).values
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=recent_dates,
                    y=recent_data,
                    name='Historical',
                    line=dict(color=viz.color_scheme['primary'], width=2),
                    mode='lines'
                ))
                
                colors = [viz.color_scheme['warning'], viz.color_scheme['success'], 
                         viz.color_scheme['info'], viz.color_scheme['danger']]
                
                for i, (method, result) in enumerate(comparison_results.items()):
                    forecast_dates = result.get('forecast_dates', [])
                    if not forecast_dates:
                        last_date = pd.to_datetime(df_sorted[date_col].iloc[-1])
                        forecast_dates = pd.date_range(start=last_date, periods=comparison_periods+1, freq='D')[1:]
                    
                    fig.add_trace(go.Scatter(
                        x=forecast_dates,
                        y=result['forecast'],
                        name=result['method'],
                        line=dict(color=colors[i % len(colors)], width=2, dash='dash'),
                        mode='lines'
                    ))
                
                fig.update_layout(
                    title=f"{comparison_metric} - Model Comparison",
                    template='plotly_white',
                    hovermode='x unified',
                    height=500,
                    margin=dict(l=20, r=20, t=40, b=20),
                    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("❌ Unable to generate forecast comparisons. Insufficient data.")
    
    st.markdown("---")
    st.markdown("### 📊 Trend Analysis")

    with st.expander("📈 Trend Detection Algorithm", expanded=False):
        st.markdown("""
        **Trend Analysis Methods:**

        **1. Trend Direction Detection:**
        - **Method**: Linear regression slope analysis
        - **Formula**: slope = Σ((x - x̄)(y - ȳ)) / Σ(x - x̄)²
        - **Classification**:
          - Slope > 0.05: "Upward Trend"
          - Slope < -0.05: "Downward Trend"
          - -0.05 ≤ Slope ≤ 0.05: "Stable"

        **2. Volatility Measurement:**
        - **Formula**: Coefficient of Variation = (σ / μ) × 100
          - σ: Standard deviation
          - μ: Mean
        - **Interpretation**: Measures relative variability (higher = more volatile)

        **3. Growth Rate Calculation:**
        - **Formula**: ((Final Value - Initial Value) / Initial Value) × 100
        - **Period**: Entire dataset timespan
        - **Output**: Percentage change over time

        **Statistical Libraries**: NumPy, SciPy, Pandas
        """)

    selected_metric = st.selectbox("Select Metric for Trend Analysis", numeric_cols, key="trend_metric")

    if st.button("Analyze Trends"):
        df_sorted = df.sort_values(date_col)
        data_series = df_sorted[selected_metric].dropna()
        
        if len(data_series) > 10:
            trend_analysis = forecaster.detect_trends(data_series)
            
            if trend_analysis:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Trend Status", trend_analysis['trend'])
                
                with col2:
                    st.metric("Volatility", f"{trend_analysis['volatility']:.2f}%")
                
                with col3:
                    st.metric("Recent Average", f"{trend_analysis['recent_average']:,.2f}")
                
                growth = forecaster.calculate_growth_rate(data_series)
                if growth:
                    st.info(f"📈 Growth Rate: {growth['growth_rate']:+.2f}% over the period")

def show_scenario_modeling_page():
    show_page_header(
        "Scenario Modeling & What-If Analysis",
        "Simulate different business scenarios and perform break-even analysis",
        "🎯"
    )

    if st.session_state.data is None:
        st.markdown("""
            <div class="data-status-banner">
                <h3 style="margin-top: 0;">⚠️ No Data Loaded</h3>
                <p>Please load data from the <strong>Home</strong> page first to run scenario models.</p>
                <p style="margin-bottom: 0;">You can use demo data or upload your own CSV/Excel file.</p>
            </div>
        """, unsafe_allow_html=True)
        return

    df = st.session_state.data

    st.markdown(f"""
        <div class="data-status-banner success">
            <strong>✅ Data Loaded:</strong> {st.session_state.data_source} ({len(df):,} records)
        </div>
    """, unsafe_allow_html=True)
    
    modeler = ScenarioModeler()
    viz = DashboardVisualizations()

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    st.markdown("""
        <div class="help-tooltip">
            <strong>🎯 Scenario Modeling Explained:</strong> Test "what-if" scenarios by adjusting key business variables.
            See how changes in one metric affect others, plan for growth, and identify break-even points.
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 💡 Revenue Growth Scenario")

    with st.expander("📐 Revenue Growth Formula", expanded=False):
        st.markdown("""
        **Compound Growth Model:**

        **Formula**: R(n) = R₀ × (1 + r)ⁿ
        - **R(n)**: Revenue at month n
        - **R₀**: Initial/current revenue
        - **r**: Monthly growth rate (as decimal, e.g., 5% = 0.05)
        - **n**: Number of months

        **Example Calculation:**
        - If current revenue = $100,000
        - Growth rate = 5% per month
        - Month 3 revenue = $100,000 × (1.05)³ = $115,762.50

        **Type**: Exponential growth (compound interest formula)

        **Use Case**: Models realistic business growth where revenue builds on previous periods
        """)

    col1, col2, col3 = st.columns(3)
    
    revenue_cols = [col for col in numeric_cols if 'revenue' in col.lower() or 'sales' in col.lower()]
    base_revenue_col = revenue_cols[0] if revenue_cols else numeric_cols[0]
    
    with col1:
        current_revenue = df[base_revenue_col].mean()
        st.metric("Current Avg Revenue", f"${current_revenue:,.0f}")
    
    with col2:
        growth_rate = st.slider("Monthly Growth Rate (%)", -10.0, 50.0, 5.0, 0.5)
    
    with col3:
        projection_months = st.slider("Projection Period (months)", 3, 24, 12)
    
    if st.button("Run Revenue Scenario"):
        projections = modeler.revenue_growth_scenario(current_revenue, growth_rate, projection_months)
        
        months = list(range(1, projection_months + 1))
        projection_df = pd.DataFrame({
            'Month': months,
            'Projected Revenue': projections
        })
        
        fig = viz.create_line_chart(projection_df, 'Month', 'Projected Revenue', 
                                     f"Revenue Projection ({growth_rate:+.1f}% monthly growth)")
        st.plotly_chart(fig, use_container_width=True)
        
        final_revenue = projections[-1]
        total_growth = ((final_revenue - current_revenue) / current_revenue * 100)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Projected Final Revenue", f"${final_revenue:,.0f}", 
                     delta=f"{total_growth:+.1f}%")
        with col2:
            st.metric("Total Revenue Increase", f"${final_revenue - current_revenue:,.0f}")
    
    st.markdown("---")
    st.markdown("### 🎲 What-If Analysis")

    with st.expander("🔄 What-If Analysis Methodology", expanded=False):
        st.markdown("""
        **Percentage-Based Adjustment Model:**

        **Formulas:**
        1. **Adjusted Value** = Original Value × (1 + Adjustment%/100)
        2. **Absolute Change** = Adjusted Value - Original Value
        3. **Change Percentage** = (Change / Original) × 100

        **Example:**
        - Original Revenue: $150,000
        - Adjustment: +15%
        - Adjusted Revenue: $150,000 × 1.15 = $172,500
        - Change: $172,500 - $150,000 = +$22,500
        - Change %: +15%

        **Methodology:**
        - Uses multiplicative adjustments (preserves proportions)
        - Applies changes independently to each metric
        - Calculates both absolute and relative changes

        **Use Case**: Simulate impact of percentage changes in key metrics
        (e.g., "What if sales increase 20% but costs rise 10%?")
        """)

    st.write("Adjust multiple metrics simultaneously to see the combined impact")
    
    col1, col2 = st.columns(2)
    
    selected_metrics = numeric_cols[:4]
    adjustments = {}
    
    for i, metric in enumerate(selected_metrics):
        if i % 2 == 0:
            with col1:
                current_value = df[metric].mean()
                st.write(f"**{metric.replace('_', ' ').title()}**")
                st.caption(f"Current: {current_value:,.2f}")
                adjustment = st.slider(f"Adjust {metric} (%)", -50, 50, 0, key=f"adjust_{metric}")
                adjustments[metric] = adjustment
        else:
            with col2:
                current_value = df[metric].mean()
                st.write(f"**{metric.replace('_', ' ').title()}**")
                st.caption(f"Current: {current_value:,.2f}")
                adjustment = st.slider(f"Adjust {metric} (%)", -50, 50, 0, key=f"adjust_{metric}")
                adjustments[metric] = adjustment
    
    if st.button("Run What-If Analysis"):
        base_metrics = {metric: df[metric].mean() for metric in selected_metrics}
        results = modeler.what_if_analysis(base_metrics, adjustments)
        
        results_list = []
        for metric, values in results.items():
            results_list.append({
                'Metric': metric.replace('_', ' ').title(),
                'Original': f"{values['original']:,.2f}",
                'Adjusted': f"{values['adjusted']:,.2f}",
                'Change': f"{values['change']:,.2f}",
                'Change %': f"{values['change_percent']:+.1f}%"
            })
        
        results_df = pd.DataFrame(results_list)
        st.dataframe(results_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("### 💰 Break-Even Analysis")

    with st.expander("💰 Break-Even Formulas & Theory", expanded=False):
        st.markdown("""
        **Break-Even Analysis - Economic Model:**

        **Key Formulas:**

        1. **Contribution Margin** = Price per Unit - Variable Cost per Unit
           - Amount each unit contributes to covering fixed costs

        2. **Break-Even Units** = Fixed Costs / Contribution Margin
           - Number of units needed to cover all costs (no profit/loss)

        3. **Break-Even Revenue** = Break-Even Units × Price per Unit
           - Total sales revenue at break-even point

        **Mathematical Model:**
        - **Total Cost** = Fixed Costs + (Variable Cost × Units)
        - **Total Revenue** = Price × Units
        - **Profit** = Total Revenue - Total Cost

        **Break-Even Point**: Where Total Revenue = Total Cost

        **Example Calculation:**
        - Fixed Costs: $50,000
        - Variable Cost: $25/unit
        - Price: $50/unit
        - Contribution Margin: $50 - $25 = $25
        - Break-Even Units: $50,000 / $25 = 2,000 units
        - Break-Even Revenue: 2,000 × $50 = $100,000

        **Visual Representation:**
        The chart shows three lines:
        - **Total Revenue** (increases linearly with units)
        - **Total Costs** (fixed + variable costs)
        - **Profit** (revenue minus costs)

        The point where revenue crosses costs is your break-even point.

        **Financial Theory**: Based on cost-volume-profit (CVP) analysis
        """)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        fixed_costs = st.number_input("Fixed Costs ($)", min_value=0, value=50000, step=1000)
    
    with col2:
        variable_cost = st.number_input("Variable Cost per Unit ($)", min_value=0.0, value=25.0, step=1.0)
    
    with col3:
        price_per_unit = st.number_input("Price per Unit ($)", min_value=0.0, value=50.0, step=1.0)
    
    if st.button("Calculate Break-Even"):
        break_even = modeler.break_even_analysis(fixed_costs, variable_cost, price_per_unit)
        
        if break_even:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Break-Even Units", f"{break_even['break_even_units']:,.0f}")
            
            with col2:
                st.metric("Break-Even Revenue", f"${break_even['break_even_revenue']:,.0f}")
            
            with col3:
                st.metric("Contribution Margin", f"${break_even['contribution_margin']:.2f}")
            
            units_range = np.arange(0, break_even['break_even_units'] * 2, break_even['break_even_units'] / 50)
            total_costs = fixed_costs + (variable_cost * units_range)
            total_revenue = price_per_unit * units_range
            profit = total_revenue - total_costs
            
            analysis_df = pd.DataFrame({
                'Units': units_range,
                'Total Revenue': total_revenue,
                'Total Costs': total_costs,
                'Profit': profit
            })
            
            fig = viz.create_multi_line_chart(analysis_df, 'Units', 
                                              ['Total Revenue', 'Total Costs', 'Profit'],
                                              "Break-Even Analysis")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("❌ Invalid parameters. Price must be greater than variable cost.")

def show_data_management_page():
    show_page_header(
        "Data Management",
        "Save, load, and manage your datasets in the database",
        "💾"
    )
    
    storage = DataStorage()
    
    tab1, tab2 = st.tabs(["📁 Saved Datasets", "💾 Save Current Data"])
    
    with tab1:
        st.subheader("Saved Datasets")
        
        datasets = storage.list_datasets()
        
        if datasets:
            for ds in datasets:
                with st.expander(f"📊 {ds['name']} ({ds['rows']:,} rows)", expanded=False):
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        st.write(f"**Source:** {ds['source_type']}")
                        st.write(f"**Created:** {ds['created_at'].strftime('%Y-%m-%d %H:%M')}")
                    
                    with col2:
                        st.write(f"**Description:** {ds['description'] or 'No description'}")
                        st.write(f"**Updated:** {ds['updated_at'].strftime('%Y-%m-%d %H:%M')}")
                    
                    with col3:
                        if st.button("Load", key=f"load_{ds['id']}"):
                            df = storage.load_dataset(ds['id'])
                            if df is not None:
                                st.session_state.data = df
                                st.session_state.data_source = f"Database: {ds['name']}"
                                st.session_state.current_dataset_id = ds['id']
                                st.toast(f"✅ Successfully loaded {ds['name']} from database!", icon="✅")
                                st.success(f"✅ Loaded {ds['name']}")
                                st.rerun()
                        
                        if st.button("Delete", key=f"del_{ds['id']}"):
                            storage.delete_dataset(ds['id'])
                            st.success(f"✅ Deleted {ds['name']}")
                            st.rerun()
        else:
            st.info("No saved datasets found. Upload or create a dataset and save it from the 'Save Current Data' tab.")
    
    with tab2:
        st.subheader("Save Current Dataset")
        
        if st.session_state.data is not None:
            col1, col2 = st.columns(2)
            
            with col1:
                dataset_name = st.text_input("Dataset Name", value=st.session_state.data_source or "My Dataset")
            
            with col2:
                dataset_description = st.text_area("Description (optional)", height=100)
            
            if st.button("💾 Save to Database", type="primary"):
                try:
                    dataset_id = storage.save_dataset(
                        st.session_state.data,
                        dataset_name,
                        dataset_description,
                        "user_saved"
                    )
                    st.session_state.current_dataset_id = dataset_id
                    st.toast(f"✅ Dataset '{dataset_name}' saved successfully to database!", icon="💾")
                    st.success(f"✅ Dataset saved successfully! ID: {dataset_id}")
                except Exception as e:
                    st.error(f"❌ Error saving dataset: {str(e)}")
        else:
            st.warning("⚠️ No data loaded. Please load or upload data from the Home page first.")

def show_data_export_page():
    show_page_header(
        "Data Export & Reports",
        "Export your data and analytics in multiple formats",
        "📥"
    )

    if st.session_state.data is None:
        st.markdown("""
            <div class="data-status-banner">
                <h3 style="margin-top: 0;">⚠️ No Data Loaded</h3>
                <p>Please load data from the <strong>Home</strong> page first to export data.</p>
                <p style="margin-bottom: 0;">You can use demo data or upload your own CSV/Excel file.</p>
            </div>
        """, unsafe_allow_html=True)
        return

    df = st.session_state.data

    st.markdown(f"""
        <div class="data-status-banner success">
            <strong>✅ Data Loaded:</strong> {st.session_state.data_source} ({len(df):,} records)
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📊 Current Dataset Preview")
    st.dataframe(df.head(100), use_container_width=True)
    
    st.markdown(f"**Total Records:** {len(df):,}")
    st.markdown(f"**Columns:** {len(df.columns)}")
    
    st.markdown("---")
    st.markdown("### 📥 Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Export Full Dataset")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📄 Download as CSV",
            data=csv,
            file_name=f"dashboard_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )
    
    with col2:
        st.subheader("Export Summary Statistics")
        processor = DataProcessor()
        summary = processor.get_summary_statistics(df)
        
        if summary and 'numeric' in summary:
            summary_csv = summary['numeric'].to_csv().encode('utf-8')
            st.download_button(
                label="📊 Download Statistics",
                data=summary_csv,
                file_name=f"statistics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
            )

def main():
    with st.sidebar:
        st.markdown("## 🎯 Navigation")

        pages = {
            "🏠 Home": "Home",
            "💾 Data Management": "Data Management",
            "📊 Executive Overview": "Executive Overview",
            "🔍 Analytics": "Analytics",
            "🔮 Forecasting": "Forecasting",
            "🎯 Scenario Modeling": "Scenario Modeling",
            "📥 Data Export": "Data Export"
        }

        for icon_page, page in pages.items():
            is_active = st.session_state.current_page == page
            button_type = "primary" if is_active else "secondary"

            if is_active:
                st.markdown(f"**➤ {icon_page}**")
            else:
                if st.button(icon_page, key=page, use_container_width=True):
                    st.session_state.current_page = page
                    st.rerun()
        
        st.markdown("---")
        
        if st.session_state.data is not None:
            st.success("✅ Data Loaded")
            st.caption(st.session_state.data_source)
            st.caption(f"{len(st.session_state.data):,} records")
        else:
            st.info("ℹ️ No data loaded")
        
        st.markdown("---")
        st.markdown("### 📚 About")
        st.caption("Transform your business data into actionable insights with advanced analytics, forecasting, and scenario modeling.")
    
    if st.session_state.current_page == "Home":
        show_home_page()
    elif st.session_state.current_page == "Data Management":
        show_data_management_page()
    elif st.session_state.current_page == "Executive Overview":
        show_executive_overview()
    elif st.session_state.current_page == "Analytics":
        show_analytics_page()
    elif st.session_state.current_page == "Forecasting":
        show_forecasting_page()
    elif st.session_state.current_page == "Scenario Modeling":
        show_scenario_modeling_page()
    elif st.session_state.current_page == "Data Export":
        show_data_export_page()

if __name__ == "__main__":
    main()
