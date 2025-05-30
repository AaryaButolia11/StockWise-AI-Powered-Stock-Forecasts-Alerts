# app.py
from flask import Flask, render_template, request, jsonify
import os
import csv
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import your specific modules
from msg import send_alert
from ml_model import generate_stock_plot, get_aggregated_forecast

# MySQL connector
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'replace_this_in_production!')

# --- Database Configuration from Environment Variables ---
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

def create_db_connection():
    """Establishes a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            database=DB_NAME
        )
        if connection.is_connected():
            print("Successfully connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
    return None

def save_user_alert_to_db(stock_symbol, phone_number):
    """Saves the stock symbol and phone number to the database."""
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO user_alerts (stock_symbol, phone_number) VALUES (%s, %s)"
            cursor.execute(query, (stock_symbol, phone_number))
            connection.commit()
            print(f"Alert for {stock_symbol} ({phone_number}) saved to DB.")
            return True
        except Error as e:
            print(f"Error saving alert to database: {e}")
            return False
        finally:
            cursor.close()
            connection.close()
    return False

def load_companies():
    """Loads company symbols and names from companies.csv."""
    companies = []
    try:
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'companies.csv')
        if not os.path.exists(file_path):
            print(f"Error: companies.csv not found at {file_path}.")
            return []

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if 'Symbol' in row and 'Company' in row:
                    companies.append((row['Symbol'], row['Company']))
    except Exception as e:
        print(f"An error occurred while loading companies.csv: {e}")
    return companies

companies = load_companies()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stock_symbol = request.form.get('stock')
        phone_number = request.form.get('phone')

        if not stock_symbol or not phone_number:
            return jsonify({'error': 'Stock symbol and phone number are required.'}), 400

        try:
            print(f"Simulating SMS sent for {stock_symbol} to {phone_number}")

            if save_user_alert_to_db(stock_symbol, phone_number):
                return jsonify({'message': 'Alert set successfully!', 'status': 'success'}), 200
            else:
                return jsonify({'error': 'Alert sent, but failed to record in database.'}), 500
        except Exception as e:
            print(f"Error processing alert: {e}")
            return jsonify({'error': f'Failed to set alert: {str(e)}'}), 500

    return render_template('index.html', companies=companies)

@app.route("/get_current_stock_info", methods=["GET"])
def get_current_stock_info():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"error": "Stock symbol is required."}), 400
    try:
        current_price, _ = send_alert(symbol, phone=None, fetch_only_price=True)
        
        if current_price is not None:
            found_company_name = next((comp_name for sym, comp_name in companies if sym == symbol), symbol)
            return jsonify({"symbol": symbol, "company_name": found_company_name, "current_price": f"{current_price:.2f}"})
        else:
            return jsonify({"error": "Could not retrieve current price."}), 404
    except Exception as e:
        print(f"Error fetching current stock info for {symbol}: {e}")
        return jsonify({"error": "Internal server error while fetching price."}), 500

@app.route("/get_forecast", methods=["GET"])
def get_forecast():
    symbol = request.args.get('symbol')
    forecast_type = request.args.get('forecast_type')

    if not symbol:
        return jsonify({"error": "Stock symbol is required."}), 400
    if forecast_type not in ['6m', '5y']:
        return jsonify({"error": "Invalid forecast type. Must be '6m' or '5y'."}), 400

    try:
        forecast_df = get_aggregated_forecast(symbol, forecast_type)

        if forecast_df is None or forecast_df.empty:
            return jsonify({"error": "Could not generate forecast."}), 500

        if not pd.api.types.is_datetime64_any_dtype(forecast_df['ds']):
            forecast_df['ds'] = pd.to_datetime(forecast_df['ds'])

        plot_img_base64 = generate_stock_plot(symbol, forecast_type=forecast_type)

        response_data = {
            "dates": forecast_df['ds'].dt.strftime('%Y-%m-%d').tolist(),
            "yhat": forecast_df['yhat'].round(2).tolist(),
            "yhat_lower": forecast_df['yhat_lower'].round(2).tolist(),
            "yhat_upper": forecast_df['yhat_upper'].round(2).tolist(),
            "plot_img": plot_img_base64
        }

        if plot_img_base64 is None:
            response_data["warning"] = "Could not generate plot."

        return jsonify(response_data)

    except Exception as e:
        print(f"Error in /get_forecast for {symbol}, type {forecast_type}: {e}")
        return jsonify({"error": "Internal server error during forecast."}), 500

if __name__ == '__main__':
    app.run(debug=True)
