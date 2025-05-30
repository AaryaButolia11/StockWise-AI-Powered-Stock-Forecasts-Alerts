# 📈 Stock Forecast & SMS Alert Web App

This Flask-based web application allows users to select a US stock, enter their phone number, and receive daily SMS or WhatsApp alerts with price updates and news. It also provides interactive stock price forecasts for the next 6 months (monthly average) or next 5 years (yearly average) using Facebook's Prophet forecasting model.

## 🚀 Features

- 📊 **Forecast Visualization**:
  - Predicts stock prices using Prophet.
  - Provides 6-month (monthly average) and 5-year (yearly average) forecasts.
  
- 🔔 **SMS/WhatsApp Notifications**:
  - Sends real-time price and news updates to user-input phone numbers using Twilio.
  
- 🌐 **Data Source**:
  - Uses [Polygon.io](https://polygon.io/) for 5 years of historical stock data.

- 📥 **Clean, production-ready architecture**:
  - Uses environment variables for sensitive keys.
  - Modular code for forecasting and visualization.

## 🛠 Tech Stack

- **Backend**: Flask (Python)
- **Data & Forecasting**: Pandas, NumPy, Prophet
- **API Integration**: Polygon.io, Twilio
- **Plotting**: Matplotlib (rendered server-side)

## 📸 Demo Screenshot

### HomePage
![Screenshot 2025-05-30 134634](https://github.com/user-attachments/assets/054f9049-2f4a-473d-bff6-44e16ec8dfaf)

### Current Stock Price is displayed as you select stock
![Screenshot 2025-05-30 134646](https://github.com/user-attachments/assets/8fff6e2d-ff61-47a5-8f9f-4e6bfdccf656)

### Prediction of future value of stock using Prophet
![Screenshot 2025-05-30 134712](https://github.com/user-attachments/assets/6f95c2c4-0b72-4c5e-b8df-ef6c227c5cce)


### SMS service for stock price
![Screenshot 2025-05-30 134725](https://github.com/user-attachments/assets/885cd53b-7d25-4b3d-82ff-9a95946b56e2)

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
