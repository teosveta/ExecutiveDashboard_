import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_finance_data():
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')

    base_revenue = 120000
    growth_trend = np.linspace(0, 40000, len(dates))
    seasonal_pattern = 15000 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25 + np.pi/2)
    weekly_cycle = 8000 * np.sin(2 * np.pi * np.arange(len(dates)) / 7)
    noise = np.random.normal(0, 8000, len(dates))
    revenue = (base_revenue + growth_trend + seasonal_pattern + weekly_cycle + noise).clip(50000, 250000)

    base_expenses = 75000
    expense_growth = np.linspace(0, 25000, len(dates))
    expense_seasonal = 8000 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
    expense_noise = np.random.normal(0, 5000, len(dates))
    expenses = (base_expenses + expense_growth + expense_seasonal + expense_noise).clip(45000, 140000)

    profit = revenue - expenses

    base_customers = 450
    customer_growth = np.linspace(0, 350, len(dates))
    customer_seasonal = 80 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25 + np.pi/4)
    customer_noise = np.random.normal(0, 30, len(dates))
    customers = (base_customers + customer_growth + customer_seasonal + customer_noise).clip(200, 1200).astype(int)

    base_satisfaction = 82
    satisfaction_trend = np.linspace(0, 8, len(dates))
    satisfaction_noise = np.random.normal(0, 2.5, len(dates))
    customer_satisfaction = (base_satisfaction + satisfaction_trend + satisfaction_noise).clip(70, 98)

    data = {
        'Date': dates,
        'Revenue': revenue.round(2),
        'Expenses': expenses.round(2),
        'Profit': profit.round(2),
        'Department': np.random.choice(['Sales', 'Marketing', 'Engineering', 'Customer Success'], len(dates), p=[0.35, 0.25, 0.25, 0.15]),
        'Product': np.random.choice(['Enterprise Suite', 'Professional Plan', 'Starter Package'], len(dates), p=[0.5, 0.35, 0.15]),
        'Region': np.random.choice(['North America', 'Europe', 'Asia Pacific', 'Latin America'], len(dates), p=[0.45, 0.30, 0.15, 0.10]),
        'Customers': customers,
        'Customer_Satisfaction': customer_satisfaction.round(2)
    }

    df = pd.DataFrame(data)
    df['Profit_Margin'] = (df['Profit'] / df['Revenue'] * 100).round(2)
    df['Revenue_Per_Customer'] = (df['Revenue'] / df['Customers']).round(2)

    return df

def generate_sales_data():
    np.random.seed(123)
    dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')

    base_sales = 55000
    trend = np.linspace(0, 45000, len(dates))
    seasonal = 12000 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
    quarterly_boost = 8000 * np.array([1 if (i % 90) < 7 else 0 for i in range(len(dates))])
    noise = np.random.normal(0, 6000, len(dates))
    sales = (base_sales + trend + seasonal + quarterly_boost + noise).clip(25000, 160000)

    base_units = 180
    units_trend = np.linspace(0, 120, len(dates))
    units_seasonal = 40 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
    units_noise = np.random.normal(0, 20, len(dates))
    units_sold = (base_units + units_trend + units_seasonal + units_noise).clip(80, 450).astype(int)

    new_customers_base = 18
    new_customers_trend = np.linspace(0, 12, len(dates))
    new_customers_noise = np.random.normal(0, 5, len(dates))
    new_customers = (new_customers_base + new_customers_trend + new_customers_noise).clip(5, 60).astype(int)

    base_churn = 2.5
    churn_improvement = -np.linspace(0, 1.2, len(dates))
    churn_noise = np.random.normal(0, 0.4, len(dates))
    churn_rate = (base_churn + churn_improvement + churn_noise).clip(0.5, 4.5)

    base_ltv = 4500
    ltv_growth = np.linspace(0, 2500, len(dates))
    ltv_noise = np.random.normal(0, 500, len(dates))
    customer_lifetime_value = (base_ltv + ltv_growth + ltv_noise).clip(2000, 12000)

    data = {
        'Date': dates,
        'Sales': sales.round(2),
        'Units_Sold': units_sold,
        'Department': np.random.choice(['Sales', 'Marketing', 'Engineering', 'Customer Success'], len(dates), p=[0.40, 0.25, 0.20, 0.15]),
        'Product': np.random.choice(['Premium Analytics', 'Business Intelligence', 'Data Insights', 'Enterprise Reports'], len(dates), p=[0.35, 0.30, 0.20, 0.15]),
        'Sales_Rep': np.random.choice(['Emily Chen', 'Marcus Rodriguez', 'Sarah Thompson', 'David Park'], len(dates), p=[0.28, 0.26, 0.24, 0.22]),
        'Region': np.random.choice(['North America', 'Europe', 'Asia Pacific'], len(dates), p=[0.50, 0.35, 0.15]),
        'New_Customers': new_customers,
        'Churn_Rate': churn_rate.round(2),
        'Customer_Lifetime_Value': customer_lifetime_value.round(2)
    }

    df = pd.DataFrame(data)
    df['Revenue'] = df['Sales']
    df['Average_Order_Value'] = (df['Sales'] / df['Units_Sold']).round(2)
    df['Monthly_Recurring_Revenue'] = (df['Sales'] * 0.7).round(2)

    return df

def generate_operations_data():
    np.random.seed(789)
    dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')

    base_production = 1100
    production_improvement = np.linspace(0, 500, len(dates))
    production_weekly = 120 * np.sin(2 * np.pi * np.arange(len(dates)) / 7)
    production_noise = np.random.normal(0, 80, len(dates))
    production_units = (base_production + production_improvement + production_weekly + production_noise).clip(600, 2200).astype(int)

    base_defect = 3.2
    defect_improvement = -np.linspace(0, 1.8, len(dates))
    defect_noise = np.random.normal(0, 0.4, len(dates))
    defect_rate = (base_defect + defect_improvement + defect_noise).clip(0.5, 5.0)

    base_cost = 68000
    cost_inflation = np.linspace(0, 15000, len(dates))
    cost_seasonal = 5000 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
    cost_noise = np.random.normal(0, 4000, len(dates))
    production_cost = (base_cost + cost_inflation + cost_seasonal + cost_noise).clip(45000, 115000)

    base_hours = 280
    hours_trend = np.linspace(0, 80, len(dates))
    hours_weekly = 30 * np.sin(2 * np.pi * np.arange(len(dates)) / 7)
    hours_noise = np.random.normal(0, 20, len(dates))
    labor_hours = (base_hours + hours_trend + hours_weekly + hours_noise).clip(150, 550).astype(int)

    base_uptime = 91
    uptime_improvement = np.linspace(0, 5, len(dates))
    uptime_noise = np.random.normal(0, 1.5, len(dates))
    machine_uptime = (base_uptime + uptime_improvement + uptime_noise).clip(85, 99.5)

    base_inventory = 2800
    inventory_cycle = 600 * np.sin(2 * np.pi * np.arange(len(dates)) / 30)
    inventory_noise = np.random.normal(0, 200, len(dates))
    inventory_level = (base_inventory + inventory_cycle + inventory_noise).clip(1500, 4800).astype(int)

    base_fulfillment = 3.5
    fulfillment_improvement = -np.linspace(0, 1.2, len(dates))
    fulfillment_noise = np.random.normal(0, 0.5, len(dates))
    order_fulfillment_time = (base_fulfillment + fulfillment_improvement + fulfillment_noise).clip(1.2, 6.5)

    data = {
        'Date': dates,
        'Production_Units': production_units,
        'Defect_Rate': defect_rate.round(2),
        'Production_Cost': production_cost.round(2),
        'Labor_Hours': labor_hours,
        'Machine_Uptime': machine_uptime.round(2),
        'Department': np.random.choice(['Manufacturing', 'Quality Control', 'Logistics', 'Maintenance'], len(dates), p=[0.45, 0.25, 0.20, 0.10]),
        'Shift': np.random.choice(['Morning', 'Afternoon', 'Night'], len(dates), p=[0.38, 0.35, 0.27]),
        'Inventory_Level': inventory_level,
        'Order_Fulfillment_Time': order_fulfillment_time.round(2)
    }

    df = pd.DataFrame(data)
    unit_price = 135 + np.linspace(0, 25, len(dates)) + np.random.normal(0, 10, len(dates))
    df['Revenue'] = (df['Production_Units'] * unit_price).round(2)
    df['Efficiency_Score'] = ((df['Production_Units'] / df['Labor_Hours']) * df['Machine_Uptime'] / 100).round(2)
    df['Cost_Per_Unit'] = (df['Production_Cost'] / df['Production_Units']).round(2)

    return df

def generate_startup_growth_data():
    np.random.seed(456)
    dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')

    growth_multiplier = np.exp(np.linspace(0, 2.2, len(dates)))

    base_mrr = 8000
    mrr_noise = np.random.normal(0, 800, len(dates))
    mrr = (base_mrr * growth_multiplier + mrr_noise).clip(8000, 85000)

    base_users = 250
    users_noise = np.random.normal(0, 15, len(dates))
    active_users = (base_users * growth_multiplier + users_noise).astype(int).clip(250, 2500)

    base_signups = 12
    signups_growth = np.linspace(0, 35, len(dates))
    signups_weekly = 8 * np.sin(2 * np.pi * np.arange(len(dates)) / 7)
    signups_noise = np.random.normal(0, 5, len(dates))
    new_signups = (base_signups + signups_growth + signups_weekly + signups_noise).clip(3, 120).astype(int)

    base_churn = 8
    churn_improvement = -np.linspace(0, 4, len(dates))
    churn_noise = np.random.normal(0, 2, len(dates))
    churn = (base_churn + churn_improvement + churn_noise).clip(1, 18).astype(int)

    base_cac = 185
    cac_optimization = -np.linspace(0, 50, len(dates))
    cac_noise = np.random.normal(0, 25, len(dates))
    cac = (base_cac + cac_optimization + cac_noise).clip(80, 280)

    base_ltv = 1200
    ltv_improvement = np.linspace(0, 1800, len(dates))
    ltv_noise = np.random.normal(0, 200, len(dates))
    ltv = (base_ltv + ltv_improvement + ltv_noise).clip(800, 4500)

    base_burn = 45000
    burn_trend = np.linspace(0, 25000, len(dates))
    burn_noise = np.random.normal(0, 5000, len(dates))
    burn_rate = (base_burn + burn_trend + burn_noise).clip(25000, 95000)

    revenue_multiple = mrr / 8000
    runway_base = 18
    runway_variation = 6 * (revenue_multiple / burn_rate * 100000)
    runway_noise = np.random.normal(0, 2, len(dates))
    runway_months = (runway_base + runway_variation + runway_noise).clip(8, 30)

    base_adoption = 35
    adoption_improvement = np.linspace(0, 40, len(dates))
    adoption_noise = np.random.normal(0, 5, len(dates))
    feature_adoption = (base_adoption + adoption_improvement + adoption_noise).clip(25, 90)

    base_satisfaction = 78
    satisfaction_improvement = np.linspace(0, 15, len(dates))
    satisfaction_noise = np.random.normal(0, 3, len(dates))
    customer_satisfaction = (base_satisfaction + satisfaction_improvement + satisfaction_noise).clip(70, 96)

    data = {
        'Date': dates,
        'MRR': mrr.round(2),
        'Active_Users': active_users,
        'New_Signups': new_signups,
        'Churn': churn,
        'CAC': cac.round(2),
        'LTV': ltv.round(2),
        'Burn_Rate': burn_rate.round(2),
        'Runway_Months': runway_months.round(1),
        'Department': np.random.choice(['Product', 'Sales', 'Marketing', 'Engineering'], len(dates), p=[0.30, 0.28, 0.25, 0.17]),
        'Feature_Adoption': feature_adoption.round(2),
        'Customer_Satisfaction': customer_satisfaction.round(2)
    }

    df = pd.DataFrame(data)
    df['Revenue'] = df['MRR']
    df['LTV_CAC_Ratio'] = (df['LTV'] / df['CAC']).round(2)
    df['Net_New_Users'] = df['New_Signups'] - df['Churn']
    df['Growth_Rate'] = ((df['Active_Users'] - df['Active_Users'].shift(30)) / df['Active_Users'].shift(30) * 100).round(2)

    return df

def get_sample_dataset(dataset_type='Finance'):
    if dataset_type == 'Finance':
        return generate_finance_data()
    elif dataset_type == 'Sales':
        return generate_sales_data()
    elif dataset_type == 'Operations':
        return generate_operations_data()
    elif dataset_type == 'Startup Growth':
        return generate_startup_growth_data()
    else:
        return generate_finance_data()

def get_dataset_description(dataset_type):
    descriptions = {
        'Finance': {
            'title': 'Finance Performance Dataset',
            'description': 'Comprehensive financial metrics including revenue, expenses, profit margins, and departmental performance',
            'metrics': ['Revenue', 'Expenses', 'Profit', 'Profit Margin', 'Customer Satisfaction'],
            'time_range': '2 years of daily data'
        },
        'Sales': {
            'title': 'Sales Analytics Dataset',
            'description': 'Sales performance data with customer acquisition, lifetime value, and regional breakdowns',
            'metrics': ['Sales', 'New Customers', 'Churn Rate', 'Average Order Value', 'Customer Lifetime Value'],
            'time_range': '2 years of daily data'
        },
        'Operations': {
            'title': 'Operations Management Dataset',
            'description': 'Production efficiency, quality control, and operational metrics',
            'metrics': ['Production Units', 'Defect Rate', 'Machine Uptime', 'Efficiency Score', 'Order Fulfillment'],
            'time_range': '2 years of daily data'
        },
        'Startup Growth': {
            'title': 'Startup Growth Metrics',
            'description': 'SaaS and startup-focused metrics including MRR, user growth, and unit economics',
            'metrics': ['MRR', 'Active Users', 'CAC', 'LTV', 'LTV/CAC Ratio', 'Burn Rate'],
            'time_range': '2 years of daily data'
        }
    }
    return descriptions.get(dataset_type, descriptions['Finance'])
