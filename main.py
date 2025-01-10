import requests
import os
from dotenv import load_dotenv
from twilio.rest import Client


load_dotenv()

# stock params
STOCK = "TVGN"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = os.getenv("STOCK_API_KEY")
PRICE_THRESHOLD = 5

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}

# news params
COMPANY_NAME = "Tevogen Bio Holdings Inc"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

news_params = {
    "q": COMPANY_NAME,
    "apiKey": NEWS_API_KEY
}

# twilio params
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
WHATSAPP_FROM = os.getenv("WHATSAPP_FROM")
WHATSAPP_TO = os.getenv("WHATSAPP_TO")

## STEP 1: Use https://www.alphavantage.co/query
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

print("Getting stock prices...")

stock_response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
stock_response.raise_for_status()
stock_data = stock_response.json()["Time Series (Daily)"]

date_yesterday = list(stock_data.keys())[0]
date_previous = list(stock_data.keys())[1]

price_yesterday = float(stock_data[date_yesterday]["4. close"])
price_previous = float(stock_data[date_previous]["4. close"])

price_diff = (price_yesterday - price_previous) / price_previous * 100

## STEP 2: Use https://newsapi.org/docs/endpoints/everything
# Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME. 

if abs(price_diff) > PRICE_THRESHOLD:
    print("Getting news...")
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"][:3]

## STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number. 

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_TOKEN)

if price_diff > 0:
    indicator = "🔺"
else:
    indicator = "🔻"

for article in news_data:
    headline = article["title"]
    description = article["description"]
    body = f"{STOCK}:{indicator}{price_diff:.2f}%\nHeadline: {headline}\nBrief: {description}"

    print("Sending message...")

    message = twilio_client.messages.create(
        from_=WHATSAPP_FROM,
        to=WHATSAPP_TO,
        body=body
    )

    print(f"Message Status: {message.status}")


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

