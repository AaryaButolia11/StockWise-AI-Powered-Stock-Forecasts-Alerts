import requests
from twilio.rest import Client
import os

# Load credentials and API keys from environment variables
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_sms_number = os.getenv("TWILIO_SMS_NUMBER")
twilio_whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

STOCK_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Initialize Twilio client
client = Client(account_sid, auth_token)

def _get_current_stock_price_and_name(stock_symbol):
    """Fetches the current stock price and symbol (as name) from Alpha Vantage."""
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_symbol}&apikey={STOCK_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "Global Quote" in data and data["Global Quote"]:
            quote = data["Global Quote"]
            current_price = float(quote.get("05. price"))
            return current_price, stock_symbol
        else:
            print(f"No 'Global Quote' found for {stock_symbol}. Response: {data}")
            return None, None
    except (requests.exceptions.RequestException, ValueError, KeyError) as e:
        print(f"Error fetching stock price for {stock_symbol}: {e}")
        return None, None

def send_alert(stock_symbol, phone=None, fetch_only_price=False):
    """
    Sends an SMS/WhatsApp alert or just fetches the current price.
    """
    current_price, company_name = _get_current_stock_price_and_name(stock_symbol)

    if fetch_only_price:
        return current_price, company_name

    if not phone or not stock_symbol:
        return False, "Stock symbol and phone number are required."
    if not phone.startswith('+'):
        return False, "Phone number must include country code (e.g., +91...)."

    if current_price is None:
        return False, f"Could not fetch current stock price for {stock_symbol}."

    news_headlines = "No recent news found."
    try:
        news_url = f"https://newsapi.org/v2/everything?q={stock_symbol}&apiKey={NEWS_API_KEY}&language=en&pageSize=1"
        news_response = requests.get(news_url)
        news_response.raise_for_status()
        articles = news_response.json().get('articles', [])
        if articles:
            news_headlines = articles[0]['title']
            if articles[0].get('url'):
                news_headlines += f" Read more: {articles[0]['url']}"
    except Exception as news_e:
        print(f"News fetch error for {stock_symbol}: {news_e}")
        news_headlines = "Could not fetch recent news."

    message_body = (
        f"StockWise Alert for {stock_symbol}:\n"
        f"Current Price: ${current_price:.2f}\n"
        f"Recent News: {news_headlines}\n"
        "You will be notified of significant price changes."
    )

    try:
        message = client.messages.create(
            to=phone,
            from_=twilio_sms_number,
            body=message_body
        )
        print(f"SMS sent: {message.sid}")
        return True, f"SMS alert sent successfully to {phone}!"
    except Exception as sms_e:
        print(f"SMS failed: {sms_e}. Trying WhatsApp...")
        try:
            whatsapp_message = client.messages.create(
                to=f"whatsapp:{phone}",
                from_=twilio_whatsapp_number,
                body=message_body
            )
            print(f"WhatsApp sent: {whatsapp_message.sid}")
            return True, f"WhatsApp alert sent successfully to {phone}!"
        except Exception as whatsapp_e:
            print(f"WhatsApp failed: {whatsapp_e}")
            return False, f"Alert failed via SMS and WhatsApp. Error: {whatsapp_e}"
