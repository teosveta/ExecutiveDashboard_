import pandas as pd
import numpy as np

class ScenarioModeler:
    
    def __init__(self):
        self.scenarios = {}
    
    def revenue_growth_scenario(self, current_revenue, growth_rate, periods=12):
        revenues = [current_revenue]
        monthly_growth = growth_rate / 100
        
        for i in range(periods):
            new_revenue = revenues[-1] * (1 + monthly_growth)
            revenues.append(new_revenue)
        
        return revenues[1:]
    
    def cost_reduction_scenario(self, current_costs, reduction_rate, periods=12):
        costs = [current_costs]
        monthly_reduction = reduction_rate / 100
        
        for i in range(periods):
            new_cost = costs[-1] * (1 - monthly_reduction)
            costs.append(new_cost)
        
        return costs[1:]
    
    def customer_growth_scenario(self, current_customers, growth_rate, churn_rate, periods=12):
        customers = [current_customers]
        monthly_growth = growth_rate / 100
        monthly_churn = churn_rate / 100
        
        for i in range(periods):
            new_customers = customers[-1] * (1 + monthly_growth - monthly_churn)
            customers.append(max(0, new_customers))
        
        return customers[1:]
    
    def profit_margin_scenario(self, revenues, costs):
        profits = [r - c for r, c in zip(revenues, costs)]
        margins = [(p / r * 100) if r > 0 else 0 for p, r in zip(profits, revenues)]
        
        return {
            'profits': profits,
            'margins': margins,
            'total_profit': sum(profits),
            'average_margin': np.mean(margins)
        }
    
    def break_even_analysis(self, fixed_costs, variable_cost_per_unit, price_per_unit):
        if price_per_unit <= variable_cost_per_unit:
            return None
        
        break_even_units = fixed_costs / (price_per_unit - variable_cost_per_unit)
        break_even_revenue = break_even_units * price_per_unit
        
        return {
            'break_even_units': round(break_even_units, 2),
            'break_even_revenue': round(break_even_revenue, 2),
            'contribution_margin': price_per_unit - variable_cost_per_unit
        }
    
    def sensitivity_analysis(self, base_value, variable_name, change_range=[-20, -10, 0, 10, 20]):
        results = []
        
        for change_pct in change_range:
            new_value = base_value * (1 + change_pct / 100)
            results.append({
                'change_percent': change_pct,
                'new_value': round(new_value, 2)
            })
        
        return results
    
    def what_if_analysis(self, base_metrics, adjustments):
        scenario_results = {}
        
        for key, value in base_metrics.items():
            if key in adjustments:
                adjustment = adjustments[key]
                new_value = value * (1 + adjustment / 100)
                scenario_results[key] = {
                    'original': value,
                    'adjusted': new_value,
                    'change': new_value - value,
                    'change_percent': adjustment
                }
            else:
                scenario_results[key] = {
                    'original': value,
                    'adjusted': value,
                    'change': 0,
                    'change_percent': 0
                }
        
        return scenario_results
    
    def compound_growth_projection(self, initial_value, annual_growth_rate, years=5):
        values = [initial_value]
        
        for year in range(years):
            new_value = values[-1] * (1 + annual_growth_rate / 100)
            values.append(new_value)
        
        return {
            'projections': values[1:],
            'total_growth': values[-1] - initial_value,
            'total_growth_percent': ((values[-1] - initial_value) / initial_value * 100) if initial_value > 0 else 0
        }
    
    def runway_calculator(self, current_cash, monthly_burn_rate, monthly_revenue=0):
        if monthly_burn_rate <= monthly_revenue:
            return {
                'runway_months': float('inf'),
                'status': 'Profitable - Indefinite Runway',
                'cash_flow_positive': True
            }
        
        net_burn = monthly_burn_rate - monthly_revenue
        runway_months = current_cash / net_burn if net_burn > 0 else float('inf')
        
        return {
            'runway_months': round(runway_months, 1),
            'net_monthly_burn': net_burn,
            'status': 'Critical' if runway_months < 6 else 'Healthy' if runway_months > 12 else 'Warning',
            'cash_flow_positive': False
        }
    
    def ltv_cac_scenario(self, customer_lifetime_value, customer_acquisition_cost, target_ratio=3.0):
        current_ratio = customer_lifetime_value / customer_acquisition_cost if customer_acquisition_cost > 0 else 0
        
        required_ltv = customer_acquisition_cost * target_ratio
        required_cac = customer_lifetime_value / target_ratio
        
        return {
            'current_ratio': round(current_ratio, 2),
            'target_ratio': target_ratio,
            'health_status': 'Excellent' if current_ratio >= 3 else 'Good' if current_ratio >= 2 else 'Poor',
            'ltv_gap': round(required_ltv - customer_lifetime_value, 2),
            'cac_gap': round(customer_acquisition_cost - required_cac, 2)
        }
    
    def market_share_scenario(self, current_market_size, current_share, growth_scenarios):
        results = []
        
        for scenario in growth_scenarios:
            market_growth = scenario.get('market_growth', 0)
            share_growth = scenario.get('share_growth', 0)
            
            new_market_size = current_market_size * (1 + market_growth / 100)
            new_share = min(100, current_share * (1 + share_growth / 100))
            
            new_revenue = new_market_size * (new_share / 100)
            current_revenue = current_market_size * (current_share / 100)
            
            results.append({
                'scenario_name': scenario.get('name', 'Unnamed'),
                'new_market_size': round(new_market_size, 2),
                'new_market_share': round(new_share, 2),
                'projected_revenue': round(new_revenue, 2),
                'revenue_change': round(new_revenue - current_revenue, 2)
            })
        
        return results
