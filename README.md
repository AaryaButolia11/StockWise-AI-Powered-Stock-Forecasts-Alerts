# 📈 Stock Forecast & SMS Alert Web App

This Flask-based web application allows users to select a US stock out of S&P 500 stocks, enter their phone number, and receive daily SMS or WhatsApp alerts with price updates and news. It also provides interactive stock price forecasts for the next 6 months (monthly average) or next 5 years (yearly average) using Facebook's Prophet forecasting model.

## 🚀 Features

- 📊 **Forecast Visualization**:
  - Predicts stock prices using Prophet.
  - Provides 6-month (monthly average) and 5-year (yearly average) forecasts.
  
- 🔔 **SMS/WhatsApp Notifications**:
  - Sends real-time price and news updates to user-input phone numbers using Twilio.
  
- 🌐 **Data Source**:
  - Uses [Polygon.io](https://polygon.io/) for 5 years of historical stock data.
  - Uses Vantage News API to take real-time data of current stock value.

- 📥 **Clean, production-ready architecture**:
  - Uses environment variables for sensitive keys.
  - Modular code for forecasting and visualization.

## 🛠 Tech Stack
👨‍💻 **Backend**
<br>
Python 3.x

Flask – Lightweight Python web framework for routing, templates, and API handling.

🧠 **Forecasting & Data Processing**
<br>
Pandas – For structured data manipulation and analysis.

Prophet – Facebook’s time-series forecasting model (for 6-month and 5-year predictions).

NumPy – Numerical operations used internally within forecasting.

📊 **Plotting**
<br>
Matplotlib – Server-side graph generation for forecast visualization (sent to frontend as base64 images).

🗃 **Database**
<br>
MySQL – Stores user alerts (stock symbol + phone number).

mysql-connector-python – Used to connect Flask with the MySQL database.

📦 **API Integrations**
<br>
Polygon.io API – For real-time stock data (prices, ticker info).

Twilio API – To send SMS/WhatsApp stock alerts to users.

(Optional/Extendable: NewsAPI) – For related stock market news integration.

📁 **Data Source**
<br>
companies.csv – Static CSV file containing company names and stock symbols.

🌐 **Frontend**
<br>
HTML5 + CSS3 – Rendered using Flask’s Jinja2 template engine.

JavaScript + AJAX – For dynamic UI interactions (e.g., fetching stock info or forecast without reloading).

🔐 **Security & Configuration**
<br>
Environment Variables – For storing secrets (e.g., DB credentials, API keys).

Flask Secret Key – For session and CSRF protection.

## Working Video



https://github.com/user-attachments/assets/59d82a63-b9d5-46f2-91a2-110610fb9ee0



## 📸 Demo Screenshot

### HomePage
![Screenshot 2025-05-30 134634](https://github.com/user-attachments/assets/054f9049-2f4a-473d-bff6-44e16ec8dfaf)

### Current Stock Price is displayed as you select stock
![Screenshot 2025-05-30 134646](https://github.com/user-attachments/assets/8fff6e2d-ff61-47a5-8f9f-4e6bfdccf656)

### Prediction of future value of stock using Prophet
![Screenshot 2025-05-30 134712](https://github.com/user-attachments/assets/6f95c2c4-0b72-4c5e-b8df-ef6c227c5cce)


### SMS service for stock price
![Screenshot 2025-05-30 134725](https://github.com/user-attachments/assets/885cd53b-7d25-4b3d-82ff-9a95946b56e2)


### Message received for updates

![WhatsApp Image 2025-06-01 at 17 44 47_bc00cb7e](https://github.com/user-attachments/assets/91d2135f-f4b4-4ac0-9dda-374eb5c2f18e)


##@ Database Creation in MySQL

![WhatsApp Image 2025-05-30 at 13 46 00_41aba738](https://github.com/user-attachments/assets/a03de476-1ea7-4487-81e2-08745e54afe4)

### Data added to DB on sending SMS

![image](https://github.com/user-attachments/assets/197d322b-a182-4fb5-b51b-f20b3cb3f323)



<!-- Replace with actual image if hosted -->

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/stock-forecast-app.git
cd stock-forecast-app
```

### 2. Create a .env File
Create a .env file in the project root and add your API keys:

```bash
POLYGON_API_KEY=your_polygon_api_key
TWILIO_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_number
DB_HOST=your_host_name
DB_USER=your_db_user_name
DB_PASSWORD=your_password
DB_NAME=your_name
```

### 3. Install Dependencies
Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run the App
```bash
flask run
```
Visit http://127.0.0.1:5000 in your browser.



## 📁 File Structure

├── app.py                 # Flask entry point<br>
├── ml_model.py            # Forecast logic using Prophet<br>
├── templates/<br>
│   └── index.html         # Web UI<br>
├── static/<br>
│   └── style.css          # CSS styles<br>
├── companies.csv          # Stock symbols and names<br>
├── requirements.txt       # Python dependencies<br>
├── .env                   # API keys (not pushed to GitHub)<br>
└── README.md              # Project documentation<br>


## 🔍 How the Forecasting Model Works
The core forecasting functionality in this project leverages historical stock data from Polygon.io, which provides daily price data for the selected stock over the last 5 years.

Workflow:
Data Fetching:
The app fetches daily historical closing prices for the chosen stock symbol using the Polygon.io API.

Data Preparation:
The raw API data is processed into a DataFrame with two columns:

ds: The date (timestamp) of the price

y: The closing stock price on that date

Model Training:
Using the cleaned data, the Prophet forecasting model is trained. Prophet is designed to handle time series data with strong seasonal effects and several seasons of historical data.

Forecast Generation:
The trained model predicts future prices for either:

The next 6 months (daily predictions aggregated to monthly averages) or

The next 5 years (daily predictions aggregated to yearly averages)

Aggregation:
Since Prophet forecasts daily data (including weekends), the predictions are filtered to exclude weekends and then averaged to smooth out the data into monthly or yearly values, which are easier to interpret.

Visualization:
The aggregated forecast data is plotted using Matplotlib, showing the predicted stock prices along with confidence intervals (uncertainty bounds) to give a sense of prediction reliability.


## 🧠 About Prophet Model Used
Prophet is a powerful open-source forecasting tool developed by Facebook for time series prediction.

Why Prophet?
It is specifically designed for business time series data with multiple seasonalities (e.g., daily, weekly, yearly).

Handles missing data and shifts in the trend gracefully.

Easy to tune and requires minimal data preprocessing.

Provides uncertainty intervals on predictions, useful for assessing risk.

How Prophet Works in This Project:
Seasonality Mode: The model uses multiplicative seasonality, which means the seasonal effects scale with the level of the time series (stock price) — appropriate for financial data.

Seasonalities Enabled: Weekly and yearly seasonality are included to capture market cycles and annual trends.

No Daily Seasonality: Disabled, since stock prices don’t typically have meaningful intraday seasonal effects at this daily aggregation level.

Future Forecasting: Prophet generates daily forecasts for the specified future period.

Confidence Intervals: Prophet computes lower and upper bounds of the forecast, representing the uncertainty in predictions.

## 📌 To-Do
 Add user authentication

 Enable email alerts

 Improve mobile responsiveness

## 🤝 Contributing
Pull requests are welcome! Please fork the repository and open a PR with enhancements or bug fixes.

## 📜 License
This project is open-source under the MIT License.
