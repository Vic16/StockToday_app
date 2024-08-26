import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import random



class Crypto:
    def __init__(self, crypto_name, cryptoTicker, period='5y'):
        self.crypto_name = crypto_name
        self.period = period
        self.crytoTicker = cryptoTicker
        self.data = self._fetch_data()
        self.current_price = self._get_current_price()
        self.previous_close = self._get_previous_close()
        self.variation = self._calculate_variation()
    
    def _fetch_data(self):
        """
        Fetch historical data for the cryptocurrency.
        """
        try:
            data = yf.download(self.crytoTicker, period=self.period)
            return data
        except Exception as e:
            print(f"Error fetching data for {self.crypto_name}: {e}")
            return pd.DataFrame()

    def _get_current_price(self):
        """
        Get the current price of the cryptocurrency.
        """
        if not self.data.empty:
            return self.data['Close'].iloc[-1]
        return None

    def _get_previous_close(self):
        """
        Get the closing price of the previous day.
        """
        if len(self.data) > 1:
            return self.data['Close'].iloc[-2]
        return None

    def _calculate_variation(self):
        """
        Calculate the percentage variation with respect to the previous close.
        """
        if self.current_price and self.previous_close:
            variation = ((self.current_price - self.previous_close) / self.previous_close) * 100
            return round(variation, 2)
        return None

    def _get_variation_emoji(self):
        """
        Return an emoji based on the variation.
        """
        if self.variation is not None:
            if self.variation > 0:
                return "\\U0001F4C8".encode().decode('unicode_escape')  # Upward trend
            elif self.variation < 0:
                return "\\U0001F4C9".encode().decode('unicode_escape')  # Downward trend
            else:
                return "\\U000027A1".encode().decode('unicode_escape')  # No change
        return "\\U00002753".encode().decode('unicode_escape')  # Unknown

    def get_current_status(self):
        """
        Get the current price, variation, and emoji.
        """
        return {
            "Current Price": self.current_price,
            "Variation": self.variation,
            "Emoji": self._get_variation_emoji()
        }
    
    def plot_price(self):
        """
        Plot a minimalistic line chart with Plotly.
        """
        if self.data.empty:
            print("No data available to plot.")
            return None
        
        # Randomly choose a color from the provided list
        colors = ['#00BFFF', '#FFD700', '#FF6347']
        line_color = random.choice(colors)
        
        fig = go.Figure()

        # Add line trace with smoothed line, without legend
        fig.add_trace(go.Scatter(
            x=self.data.index,
            y=self.data['Close'],
            mode='lines',
            name='Price',
            line=dict(color=line_color, shape='spline'),  # Use 'spline' for a smooth curve
            marker=dict(size=6),
            showlegend=False  # Hide the legend for the price line
        ))

        # Highlight the last price point
        fig.add_trace(go.Scatter(
            x=[self.data.index[-1]],
            y=[self.current_price],
            mode='markers+text',
            name='Current Price',
            text=[f'${self.current_price:.2f}'],
            textposition='top center',
            textfont=dict(size=16, color='white'),
            marker=dict(size=12, color='red')
        ))

        # Layout settings
        fig.update_layout(
            title=f'{self.crypto_name} Price Trend',
            xaxis_title=None,  # No label on x-axis
            yaxis_title='Price (USD)',
            plot_bgcolor='black',
            paper_bgcolor='black',
            font_color='white',
            xaxis=dict(
                showgrid=True,
                gridcolor='white'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='white'
            )
        )

        return fig
        #fig.show()