# from json.decoder import JSONDecodeError
import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True,
                        headers={"User-Agent": "PostmanRuntime/7.33.0"})

test_l = len(response.history)

for var in range(0, test_l):
    print(response.history[var].url)

print(response.status_code)
