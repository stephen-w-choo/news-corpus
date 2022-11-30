import requests
import json
import markovify


def news_api_url(source, page):
    return f"https://newsapi.org/v2/everything?apiKey=dc0d853fff164a0b86216df081e1ee45&sources={source}&page={page}"

def news_api_request(url_request):
    # takes an API get request and returns a dictionary
    # the dict will have the shape {"data":{}, "meta"}
    return requests.request(
        "GET",
        url_request,
    ).json()


def paginate(source):
    # takes a list and uses the next token to extend the list 4 times
    # returns the extended list
    api_url = news_api_url(source, 1)

    first_api_response = news_api_request(api_url)

    pages = first_api_response["totalResults"] // 100
    print(pages)
    corpus = first_api_response["articles"]

    for i in range(2, pages):
        api_url = news_api_url(source, i)
        next_api_response = news_api_request(api_url)
        print(next_api_response)
        corpus.extend(next_api_response["articles"])

    return corpus


def twitter_json_to_string(list_of_tweet_objects):
    # Takes the data object from the API response and converts to a string
    text = []

    for object in list_of_tweet_objects:
        text.append(object["text"])

    return "\n".join(text)
