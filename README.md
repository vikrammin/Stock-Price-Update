# STOCK PRICE UPDATE PROGRAM:

## Overview:
I created this Python script to monitor the prices of a certain stock I chose. The script looks at the closing price of the stock from two days ago and the closing price from yesterday. It will find the percentage difference between them and if it is more than 3% or less than -3%, you will get an email of articles relating to the company you chose. 

## Features:
- Fetches real-time data using the Alpha Vantage API.
- Retrieves the top articles of the specified company using NewsAPI.
- Sends customizable email alerts containing information about stock price changes and top news articles.
- Ability to customize email recipients and threshold for price change alerts.
- Error handling for API requests and email-sending processes.

## Here is a screenshot of an email for the company NVIDIA:
<img width="718" alt="Screenshot 2024-03-06 at 9 41 45 PM" src="https://github.com/vikrammin/Stock-Price-Update/assets/157865720/039408fb-80d2-4722-a455-e5eaf7440e73">
