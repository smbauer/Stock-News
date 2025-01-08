import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# stock params
STOCK = "TSLA"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = os.getenv("STOCK_API_KEY")

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}

# news params
COMPANY_NAME = "Tesla Inc"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

news_params = {
    "q": COMPANY_NAME,
    "apiKey": NEWS_API_KEY
}

## STEP 1: Use https://www.alphavantage.co/query
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

try:
    # read data if file exists
    with open("data.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    # otherwise create new file and add data
    print("calling api")
    response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
    response.raise_for_status()
    data = response.json()["Time Series (Daily)"]

    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

date_yesterday = list(data.keys())[0]
date_previous = list(data.keys())[1]

price_yesterday = float(data[date_yesterday]["4. close"])
price_previous = float(data[date_previous]["4. close"])

price_diff = (price_yesterday - price_previous) / price_previous * 100

## STEP 2: Use https://newsapi.org/docs/endpoints/everything
# Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME. 

if price_diff < -4 or price_diff > 4:
    print("Get news")
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"][:3]

    print(price_diff)
    print(news_data[0]["title"])
    print(news_data[0]["description"])

    print(price_diff)
    print(news_data[1]["title"])
    print(news_data[1]["description"])

    print(price_diff)
    print(news_data[2]["title"])
    print(news_data[2]["description"])

## STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number. 
#HINT 1: Consider using a List Comprehension.



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

