import requests
import time


def check_status(status_code, status, text):
    if (status_code == 200) & (status == text):
        return "Успешно"
    else:
        return "Неуспешно"


requests1 = requests.get(" https://playground.learnqa.ru/ajax/api/longtime_job")
body_response1 = requests1.json()
print(f" Выполнили запрос на получение токена вот ответ: {body_response1} ")

requests2 = requests.get(" https://playground.learnqa.ru/ajax/api/longtime_job",
                         params={"token": body_response1["token"]})
status2 = "Job is NOT ready"
body_response2 = requests2.json()
result = check_status(requests2.status_code, body_response2["status"], status2)

print(
    f"Тест 1. Выполнен запрос с токеном: {body_response1["token"]}, получен ответ: {requests2.text}, сравнили статус со строкой {status2}. \nРезультат: {result}")
print(f"Следующий тест будет выполнен через {body_response1["seconds"]} секунд")

time.sleep(body_response1["seconds"])  # задежрка N секунд

requests3 = requests.get(" https://playground.learnqa.ru/ajax/api/longtime_job",
                         params={"token": body_response1["token"]})
body_response3 = requests3.json()
status3 = "Job is ready"
# result = check_status(requests3.status_code, body_response3["status"], status3)
if body_response3.get("result") is None:
    result = "Неуспешно"
else:
    result = check_status(requests3.status_code, body_response3["status"], status3)

print(
    f"Тест 2. Выполнен запрос с токеном: {body_response1["token"]}, получен ответ: {requests3.text} сравнили статус со строкой {status3} и проверили наличие поля result. \nРезультат: {result}  ")
