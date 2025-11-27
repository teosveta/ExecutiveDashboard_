import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

class DashboardVisualizations:

    def __init__(self):
        self.color_scheme = {
            'primary': '#1a2a6c',
            'secondary': '#0f2027',
            'success': '#28a745',
            'warning': '#d4af37',
            'danger': '#dc3545',
            'info': '#2c5364',
            'accent': '#d4af37',
            'navy': '#1a2a6c',
            'teal': '#2c5364',
            'gold': '#d4af37'
        }
        self.gradient_colors = [
            '#1a2a6c',
            '#2c5364',
            '#d4af37',
            '#28a745',
            '#5a9bd4'
        ]
    
    def create_line_chart(self, df, x_col, y_col, title='', color=None):
        fig = px.line(df, x=x_col, y=y_col, title=title)

        fig.update_traces(
            line_color=color or self.color_scheme['primary'],
            line_width=3,
            line_shape='spline'
        )

        fig.update_layout(
            template='plotly_white',
            hovermode='x unified',
            showlegend=True,
            height=400,
            margin=dict(l=20, r=20, t=60, b=20),
            title_font=dict(size=18, color='#1a2a6c', family='Arial Black'),
            plot_bgcolor='rgba(245, 247, 250, 0.5)',
            paper_bgcolor='white',
            font=dict(family='Arial', size=12, color='#2c3e50'),
            xaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(200, 200, 200, 0.3)',
                showline=True,
                linewidth=2,
                linecolor='#d4af37'
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(200, 200, 200, 0.3)',
                showline=True,
                linewidth=2,
                linecolor='#d4af37'
            )
        )

        return fig
    
    def create_area_chart(self, df, x_col, y_col, title='', fill_color=None):
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[y_col],
            fill='tozeroy',
            fillcolor=fill_color or 'rgba(26, 42, 108, 0.2)',
            line=dict(color=self.color_scheme['primary'], width=3, shape='spline'),
            name=y_col,
            hovertemplate='<b>%{y:,.0f}</b><extra></extra>'
        ))

        fig.update_layout(
            title=title,
            template='plotly_white',
            hovermode='x unified',
            height=400,
            margin=dict(l=20, r=20, t=60, b=20),
            title_font=dict(size=18, color='#1a2a6c', family='Arial Black'),
            plot_bgcolor='rgba(245, 247, 250, 0.5)',
            paper_bgcolor='white',
            font=dict(family='Arial', size=12, color='#2c3e50'),
            xaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(200, 200, 200, 0.3)',
                showline=True,
                linewidth=2,
                linecolor='#d4af37'
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(200, 200, 200, 0.3)',
                showline=True,
                linewidth=2,
                linecolor='#d4af37'
            )
        )

        return fig
    
    def create_bar_chart(self, df, x_col, y_col, title='', color=None, orientation='v'):
        if orientation == 'v':
            fig = px.bar(df, x=x_col, y=y_col, title=title)
        else:
            fig = px.bar(df, x=y_col, y=x_col, title=title, orientation='h')

        fig.update_traces(
            marker_color=color or self.color_scheme['navy'],
            marker_line_color='#d4af37',
            marker_line_width=1.5,
            hovertemplate='<b>%{y:,.0f}</b><extra></extra>'
        )

        fig.update_layout(
            template='plotly_white',
            height=400,
            margin=dict(l=20, r=20, t=60, b=20),
            title_font=dict(size=18, color='#1a2a6c', family='Arial Black'),
            plot_bgcolor='rgba(245, 247, 250, 0.5)',
            paper_bgcolor='white',
            font=dict(family='Arial', size=12, color='#2c3e50'),
            xaxis=dict(
                showgrid=False,
                showline=True,
                linewidth=2,
                linecolor='#d4af37'
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(200, 200, 200, 0.3)',
                showline=True,
                linewidth=2,
                linecolor='#d4af37'
            )
        )

        return fig
    
    def create_pie_chart(self, df, names_col, values_col, title=''):
        fig = px.pie(df, names=names_col, values=values_col, title=title,
                     color_discrete_sequence=self.gradient_colors)

        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont_size=13,
            marker=dict(line=dict(color='white', width=3)),
            hovertemplate='<b>%{label}</b><br>Value: %{value:,.0f}<br>Percent: %{percent}<extra></extra>',
            pull=[0.05 if i == 0 else 0 for i in range(len(df))]
        )

        fig.update_layout(
            template='plotly_white',
            height=400,
            margin=dict(l=20, r=20, t=60, b=20),
            title_font=dict(size=18, color='#1a2a6c', family='Arial Black'),
            paper_bgcolor='white',
            font=dict(family='Arial', size=12, color='#2c3e50')
        )

        return fig
    
    def create_multi_line_chart(self, df, x_col, y_cols, title=''):
        fig = go.Figure()

        for i, col in enumerate(y_cols):
            if col in df.columns:
                fig.add_trace(go.Scatter(
                    x=df[x_col],
                    y=df[col],
                    name=col,
                    line=dict(color=self.gradient_colors[i % len(self.gradient_colors)], width=3, shape='spline'),
                    mode='lines',
                    hovertemplate='<b>%{y:,.0f}</b><extra></extra>'
                ))

        fig.update_layout(
            title=title,
            template='plotly_white',
            hovermode='x unified',
            height=400,
            margin=dict(l=20, r=20, t=60, b=20),
            title_font=dict(size=18, color='#1a2a6c', family='Arial Black'),
            plot_bgcolor='rgba(245, 247, 250, 0.5)',
            paper_bgcolor='white',
            font=dict(family='Arial', size=12, color='#2c3e50'),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1,
                bgcolor='rgba(255, 255, 255, 0.9)',
                bordercolor='#d4af37',
                borderwidth=2
            ),
            xaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(200, 200, 200, 0.3)',
                showline=True,
                linewidth=2,
                linecolor='#d4af37'
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(200, 200, 200, 0.3)',
                showline=True,
                linewidth=2,
                linecolor='#d4af37'
            )
        )

        return fig
    
    def create_grouped_bar_chart(self, df, x_col, y_cols, title=''):
        fig = go.Figure()
        
        colors = [self.color_scheme['primary'], self.color_scheme['success'], 
                 self.color_scheme['warning'], self.color_scheme['info']]
        
        for i, col in enumerate(y_cols):
            if col in df.columns:
                fig.add_trace(go.Bar(
                    x=df[x_col],
                    y=df[col],
                    name=col,
                    marker_color=colors[i % len(colors)]
                ))
        
        fig.update_layout(
            title=title,
            template='plotly_white',
            barmode='group',
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
        )
        
        return fig
    
    def create_stacked_bar_chart(self, df, x_col, y_cols, title=''):
        fig = go.Figure()
        
        colors = [self.color_scheme['primary'], self.color_scheme['success'], 
                 self.color_scheme['warning'], self.color_scheme['info']]
        
        for i, col in enumerate(y_cols):
            if col in df.columns:
                fig.add_trace(go.Bar(
                    x=df[x_col],
                    y=df[col],
                    name=col,
                    marker_color=colors[i % len(colors)]
                ))
        
        fig.update_layout(
            title=title,
            template='plotly_white',
            barmode='stack',
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
        )
        
        return fig
    
    def create_scatter_plot(self, df, x_col, y_col, title='', color_col=None, size_col=None):
        fig = px.scatter(
            df, 
            x=x_col, 
            y=y_col, 
            title=title,
            color=color_col,
            size=size_col
        )
        
        fig.update_layout(
            template='plotly_white',
            height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        return fig
    
    def create_heatmap(self, df, x_col, y_col, z_col, title=''):
        pivot_df = df.pivot_table(values=z_col, index=y_col, columns=x_col, aggfunc='mean')
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_df.values,
            x=pivot_df.columns,
            y=pivot_df.index,
            colorscale='Blues',
            hoverongaps=False
        ))
        
        fig.update_layout(
            title=title,
            template='plotly_white',
            height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        return fig
    
    def create_gauge_chart(self, value, title='', max_value=100, threshold_low=30, threshold_high=70):
        fig = go.Figure(go.Indicator(
            mode='gauge+number+delta',
            value=value,
            title={'text': title},
            delta={'reference': max_value * 0.8},
            gauge={
                'axis': {'range': [None, max_value]},
                'bar': {'color': self.color_scheme['primary']},
                'steps': [
                    {'range': [0, threshold_low], 'color': 'rgba(239, 68, 68, 0.2)'},
                    {'range': [threshold_low, threshold_high], 'color': 'rgba(245, 158, 11, 0.2)'},
                    {'range': [threshold_high, max_value], 'color': 'rgba(16, 185, 129, 0.2)'}
                ],
                'threshold': {
                    'line': {'color': 'red', 'width': 4},
                    'thickness': 0.75,
                    'value': max_value * 0.9
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        return fig
    
    def create_forecast_chart(self, historical_data, forecast_data, historical_dates, forecast_dates, title='', 
                              lower_bound=None, upper_bound=None):
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=historical_dates,
            y=historical_data,
            name='Historical',
            line=dict(color=self.color_scheme['primary'], width=2),
            mode='lines'
        ))
        
        if lower_bound and upper_bound:
            fig.add_trace(go.Scatter(
                x=forecast_dates,
                y=upper_bound,
                mode='lines',
                line=dict(width=0),
                showlegend=False,
                hoverinfo='skip'
            ))
            
            fig.add_trace(go.Scatter(
                x=forecast_dates,
                y=lower_bound,
                mode='lines',
                line=dict(width=0),
                fillcolor='rgba(245, 158, 11, 0.2)',
                fill='tonexty',
                name='Confidence Interval',
                hoverinfo='skip'
            ))
        
        fig.add_trace(go.Scatter(
            x=forecast_dates,
            y=forecast_data,
            name='Forecast',
            line=dict(color=self.color_scheme['warning'], width=2, dash='dash'),
            mode='lines'
        ))
        
        fig.update_layout(
            title=title,
            template='plotly_white',
            hovermode='x unified',
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
        )
        
        return fig
