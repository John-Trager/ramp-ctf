'''
Used to spoof a request with what browser is being used

"/browser" challenge
'''

import requests

if __name__ == '__main__':

    url = "https://0ijq1i6sp1.execute-api.us-east-1.amazonaws.com/dev/browser"
    custom_user_agent = "Mozilla/8.8 (Macintosh; Intel Mac OS X 8888_8888) AppleWebKit/888.8.88 (KHTML, like Gecko) Version/88.8.8 Safari/888.8.88"

    headers = {
        "User-Agent": custom_user_agent
    }

    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print("Request successful!")
        print(response.text)
    else:
        print(f"Request failed with status code: {response.status_code}")

