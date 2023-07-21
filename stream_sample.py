'''
data collection script for "/stream" challenge
'''
import requests

if __name__ == "__main__":
    url = "https://0ijq1i6sp1.execute-api.us-east-1.amazonaws.com/dev/stream"


    d = {}
    for i in range(100):
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            char = response.text[1]
            if char in d:
                d[char] += 1
            else:
                d[char] = 1
        else:
            print(f"Request failed with status code: {response.status_code}")


    print(d)

    # output: 
    # {'i': 18, 'u': 24, 'b': 4, 'd': 12, 'l': 7, 'a': 34, 'y': 1}
    # {'a': 35, 'i': 10, 'b': 10, 'u': 21, 'y': 1, 'd': 17, 'l': 6}