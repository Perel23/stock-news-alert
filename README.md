# Stock News SMS Alert

Monitors a stock's daily price change and sends SMS alerts with relevant news when the price moves significantly.

## What it does

1. Fetches the last two days of closing prices for a stock (default: TSLA) from Alpha Vantage
2. If the price changed by 1% or more, fetches the top 3 relevant news articles from NewsAPI
3. Sends each article as a formatted SMS via Twilio

**Example message:**
```
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?
Brief: We at Insider Monkey have gone over 821 13F filings...
```

## Setup

1. Install dependencies:
   ```bash
   pip install requests twilio python-dotenv
   ```

2. Create a `.env` file with the following keys:
   ```
   STOCK_API_KEY=your_alphavantage_api_key
   NEWS_API_KEY=your_newsapi_key
   TWILIO_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_NUMBER=your_twilio_phone_number
   YOUR_NUMBER=your_personal_phone_number
   ```

3. Run:
   ```bash
   python main.py
   ```

## APIs Used

- [Alpha Vantage](https://www.alphavantage.co) — stock price data
- [NewsAPI](https://newsapi.org) — news articles
- [Twilio](https://www.twilio.com) — SMS delivery