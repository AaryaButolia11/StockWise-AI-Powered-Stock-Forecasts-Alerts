import os
import requests
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend before importing pyplot
import matplotlib.pyplot as plt

import io
import base64
from datetime import datetime, timedelta
import warnings

# Suppress harmless warnings
warnings.filterwarnings("ignore")

from prophet import Prophet

# --- Read API key from environment variable ---
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
# ------------------------------------------------

def fetch_polygon_data(symbol):
    """
    Fetches historical stock data using Polygon.io API.
    """
    end = datetime.now()
    start = end - timedelta(days=365 * 5)  # 5 years of data
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start:%Y-%m-%d}/{end:%Y-%m-%d}"
    params = {
        "adjusted": "true",
        "sort": "asc",
        "limit": 5000,
        "apiKey": POLYGON_API_KEY
    }
    res = requests.get(url, params=params)
    if res.status_code != 200:
        print(f"Error fetching data from Polygon: {res.text}")
        return None
    data = res.json().get("results", [])
    if not data:
        return None
    df = pd.DataFrame(data)
    df['t'] = pd.to_datetime(df['t'], unit='ms')
    df.rename(columns={'t': 'ds', 'c': 'y'}, inplace=True)  # ds for date, y for close price
    return df[['ds', 'y']]

def get_aggregated_forecast(symbol, forecast_type='6m'):
    """
    Fetches historical data, trains a Prophet model, and generates a forecast.
    Aggregates daily predictions to monthly or yearly averages.
    """
    df = fetch_polygon_data(symbol)
    if df is None or df.empty:
        print(f"No data to train model for {symbol}.")
        return None

    df = df.sort_values('ds').reset_index(drop=True)

    model = Prophet(
        seasonality_mode='multiplicative',
        daily_seasonality=False,
        weekly_seasonality=True,
        yearly_seasonality=True
    )
    model.fit(df)

    if forecast_type == '6m':
        future = model.make_future_dataframe(periods=180, freq='D')
        forecast = model.predict(future)

        last_historical_date = df['ds'].max()
        forecast_df = forecast[forecast['ds'] > last_historical_date]
        forecast_df = forecast_df[forecast_df['ds'].dt.weekday < 5]

        agg = forecast_df.groupby(forecast_df['ds'].dt.to_period('M')).mean(numeric_only=True).reset_index()
        agg['ds'] = agg['ds'].dt.to_timestamp()

        if len(agg) < 6 and not agg.empty:
            print(f"DEBUG: Only {len(agg)} months generated for 6m forecast. Extending if possible.")

        return agg[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

    elif forecast_type == '5y':
        future = model.make_future_dataframe(periods=30 * 365, freq='D')
        forecast = model.predict(future)

        last_historical_date = df['ds'].max()
        forecast_df = forecast[forecast['ds'] > last_historical_date]
        forecast_df = forecast_df[forecast_df['ds'].dt.weekday < 5]

        forecast_df['year'] = forecast_df['ds'].dt.year
        agg = forecast_df.groupby('year').mean(numeric_only=True).reset_index()

        start_year = datetime.now().year + 1
        years_to_keep = [start_year + i for i in range(0, 5)]

        agg = agg[agg['year'].isin(years_to_keep)]
        agg['ds'] = pd.to_datetime(agg['year'].astype(str) + "-01-01")

        return agg[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    else:
        return None

def generate_stock_plot(symbol, forecast_type='6m'):
    """
    Generates a plot for the stock forecast.
    """
    forecast_df = get_aggregated_forecast(symbol, forecast_type)
    if forecast_df is None or forecast_df.empty:
        return None

    plt.figure(figsize=(12, 6))
    plot_title = f"{symbol} Stock Price Forecast"
    plot_label = "Predicted Price"

    if forecast_type == '6m':
        plot_title += " (Next 6 Months, Monthly Avg) - Prophet"
        plot_label += " (Monthly Avg)"
    elif forecast_type == '5y':
        plot_title += " (Next 5 Years, Yearly Avg) - Prophet"
        plot_label += " (Yearly Avg)"

    plt.plot(forecast_df['ds'], forecast_df['yhat'], label=plot_label, marker='o', color='#6c5ce7')
    plt.fill_between(forecast_df['ds'], forecast_df['yhat_lower'], forecast_df['yhat_upper'],
                     color='#a29bfe', alpha=0.3, label='Confidence Interval')

    plt.title(plot_title, fontsize=16, fontweight='bold')
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Price", fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')
