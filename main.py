import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True,
                        headers={"User-Agent": "PostmanRuntime/7.33.0"})

redirect_cnt = len(response.history)

for var in range(0, redirect_cnt):
    print(response.history[var].url)

print(f"Количество редиректов: {redirect_cnt}")
print(f"Конечный урл: {response.url}")
