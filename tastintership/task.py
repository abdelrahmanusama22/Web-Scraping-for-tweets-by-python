import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json

def scrape_twitter_account(account_url, ticker, time_interval):
   
    try:
        response = requests.get(account_url)
        response.raise_for_status()  # Ensure the request was successful
        soup = BeautifulSoup(response.text, 'lxml')
        tweets = soup.find_all("span", {'class': 'r-18u37iz'})
        count = 0
        tweets_text = []

        for tweet in tweets:
            tweet_content = tweet.find("a", {'class': 'css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3 r-1ny4l3l r-1ddef8g r-tjvw6i r-1loqt21'})
            if tweet_content and ticker in tweet_content.text:
                tweet_time_element = tweet.find('time')
                if tweet_time_element:
                    tweet_time = tweet_time_element['datetime']
                    tweet_datetime = datetime.strptime(tweet_time, '%Y-%m-%dT%H:%M:%S.%fZ')
                    time_difference = datetime.now() - tweet_datetime
                    if time_difference.total_seconds() / 60 <= time_interval:
                        count += 1
                        tweets_text.append(tweet_content.text)
                        print(tweet_content.text)

        return count, tweets_text
    except Exception as e:
        print("Error scraping account:", account_url)
        print(e)
        return 0, []

def main():
    twitter_accounts = [
        "https://twitter.com/Mr_Derivatives",
        "https://twitter.com/warrior_0719",
        "https://twitter.com/ChartingProdigy",
        "https://twitter.com/allstarcharts",
        "https://twitter.com/yuriymatso",
        "https://twitter.com/TriggerTrades",
        "https://twitter.com/AdamMancini4",
        "https://twitter.com/CordovaTrades",
        "https://twitter.com/Barchart",
        "https://twitter.com/RoyLMattox"
    ]

    ticker = input("Enter the stock symbol to look for (e.g., TSLA): ")
    interval = int(input("Enter the time interval for scraping sessions (in minutes): "))

    while True:
        total_mentions = 0
        for account_url in twitter_accounts:
            mentions, tweets_text = scrape_twitter_account(account_url, ticker, interval)
            total_mentions += mentions
            print(f"{ticker} was mentioned {mentions} times on {account_url} in the last {interval} minutes.")

        print(f"'{ticker}' was mentioned '{total_mentions}' times in the last '{interval}' minutes.")

        with open("output.json", "w") as outfile:
            json.dump({
                "ticker": ticker,
                "mentions": total_mentions,
                "interval": interval,
                "timestamp": datetime.now().isoformat()
            }, outfile, indent=4)

        time.sleep(interval * 60) 

if __name__ == "__main__":
    main()
