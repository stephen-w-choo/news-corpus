import requests
import json
import os
from dotenv import load_dotenv
import twitter_api
import re
from amazon_boto3 import update_db
import pandas as pd
from datetime import datetime

load_dotenv()

payload={}
headers = {
    'Authorization': os.getenv("AUTHORIZATION")
}

f = open("abc-news-corpus.txt", "w")

twitter_id = twitter_api.lookup_username(headers, "abcnews")["data"]["id"]


dates = pd.date_range(start="2022-11-22",end="2022-11-30")

for i in range(0, len(dates) - 1):
    url = twitter_api.timeline_api_url(twitter_id, str(dates[i].date()), str(dates[i + 1].date()))
    api_response = twitter_api.api_request(payload, headers, url)
    api_response = twitter_api.paginate(api_response, headers, url)

    if not api_response:
        continue

    res = []

    for dictionary in api_response:
        headline = dictionary["text"]
        headline = re.sub("https\S*", "", headline)
        res.append(headline)
    # def update_db(news_site, day, month, year, headlines):
    update_db("abc-news", str(dates[i].day), str(dates[i].month), str(dates[i].year), res)
