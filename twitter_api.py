import requests
import json
import markovify

def lookup_username(headers, user_handle):
    # takes a user handle and returns the user id
    url = f"https://api.twitter.com/2/users/by/username/{user_handle}?user.fields=profile_image_url"
    response = requests.request("GET", url, headers=headers).json()
    return response

def timeline_api_url(user_id, start_date, end_date):
    return (f"https://api.twitter.com/2/users/{user_id}/tweets?max_results=100" +
    f"&start_time={start_date}T06:31:00.000Z&end_time={end_date}T06:31:00.000Z")

def api_request(payload, headers, url_request):
    # takes an API get request and returns a dictionary
    # the dict will have the shape {"data":{}, "meta"}
    print(url_request)
    return requests.request(
        "GET",
        url_request,
        headers=headers,
        data=payload
    ).json()

def paginate(api_response, headers, url_request):
    # takes an api response and uses the next token to extend the list 4 times
    # returns the extended list
    try:
        current_list = api_response["data"]
    except:
        return None
    current_response = api_response

    for i in range(4):
        if "next_token" not in current_response["meta"]:
            break
        next_token = current_response["meta"]["next_token"]

        next_response = requests.request(
            "GET",
            f"{url_request}&pagination_token={next_token}",
            headers=headers,
        ).json()
        try:
            current_list.extend(next_response["data"])
            current_response = next_response
        except:
            break

    return current_list
