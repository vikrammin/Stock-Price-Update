import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_api_key = "YOUR STOCK API KEY"
news_api_key = "YOUR NEWS API KEY"
stock_symbol = "NVDA"
stock_company = "NVIDIA"

my_email = "YOUR EMAIL"
password = "YOUR EMAIL APP PASSWORD"
recipient = "RECIPIENT EMAIL"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": stock_symbol,
    "apikey": stock_api_key,
}


#Getting request for NVIDIA stock
stock_response = requests.get(STOCK_ENDPOINT, params=stock_params)
stock_data = stock_response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in stock_data.items()]

#Getting price of stock yesterday
yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])
print(yesterday_closing_price)

#Getting price of stock two days ago
twoDaysAgo_data = data_list[1]
twoDaysAgo_closing_price = float(twoDaysAgo_data["4. close"])
print(twoDaysAgo_closing_price)

#Finding the difference in the closing prices between the two days
price_difference = yesterday_closing_price - twoDaysAgo_closing_price
print(price_difference)

#Finding the percentage difference
percentage_difference = (price_difference / twoDaysAgo_closing_price) * 100
print(percentage_difference)


news_param = {
    'qInTitle': stock_company,
    'apiKey': news_api_key,
}

#Getting request for NewsAPI
news_response = requests.get(NEWS_ENDPOINT, params=news_param)
news_data = news_response.json()["articles"]

#If statement to get the top 3 articles relating to the stock if percentage difference is above 5%
msg = MIMEMultipart()
msg['From'] = my_email
msg['To'] = recipient

# Subject of the email
if percentage_difference > 0:
    subject = f"{stock_company} 🔺 {abs(round(percentage_difference))}%"
elif percentage_difference < 0:
    subject = f"{stock_company} 🔻 {abs(round(percentage_difference))}%"
else:
    subject = f"{stock_company} Stock Price Change Alert"
msg['Subject'] = subject

# Message body containing the articles and stock price change information
message = ""
if percentage_difference > 3 or percentage_difference < -3:
    if percentage_difference > 3:
        message += "The stock price has increased by {:.2f}%.\n\n".format(percentage_difference)
    elif percentage_difference < -3:
        message += "The stock price has decreased by {:.2f}%.\n\n".format(abs(percentage_difference))

    if news_response.status_code == 200:
        articles = news_data[:3]  # Use news_data directly since it's already a list of articles
        for article in articles:
            title = article['title']
            description = article['description']
            url = article['url']
            message += f"Title: {title}\nDescription: {description}\nURL: {url}\n\n"
    else:
        message = "Error: " + news_data.get('message', 'Unknown error')

    # Attach the message body
    msg.attach(MIMEText(message, 'plain'))

    # Send the email using the 'with' statement
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(my_email, password=password)
            text = msg.as_string()
            server.sendmail(my_email, recipient, text)
        print("Email sent successfully!")
    except Exception as e:
        print("Error:", e)

