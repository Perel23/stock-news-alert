import os
import requests
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = os.environ["STOCK_API_KEY"]
NEWS_API_KEY = os.environ["NEWS_API_KEY"]
TWILIO_SID = os.environ["TWILIO_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_NUMBER = os.environ["TWILIO_NUMBER"]
YOUR_NUMBER = os.environ["YOUR_NUMBER"]

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}

response = requests.get("https://www.alphavantage.co/query", params=stock_params)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]

data_list = [value for (key, value) in data.items()]
yesterday_close = float(data_list[0]["4. close"])
day_before_yesterday_close = float(data_list[1]["4. close"])

difference = yesterday_close - day_before_yesterday_close
up_down = "🔺" if difference > 0 else "🔻"
diff_percent = round((difference / day_before_yesterday_close) * 100)

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

if abs(diff_percent) >= 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get("https://newsapi.org/v2/everything", params=news_params)
    news_response.raise_for_status()
    articles = news_response.json()["articles"]
    three_articles = [a for a in articles if a["description"]][:3]

    ## STEP 3: Use https://www.twilio.com
    # Send a separate message with the percentage change and each article's title and description to your phone number.

    formatted_articles = [
        f"{STOCK}: {up_down}{abs(diff_percent)}%\nHeadline: {article['title']}\nBrief: {article['description']}"
        for article in three_articles
    ]

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        client.messages.create(
            body=article,
            from_=TWILIO_NUMBER,
            to=YOUR_NUMBER,
        )


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

