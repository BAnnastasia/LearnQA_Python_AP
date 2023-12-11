import requests
def  find_password ():

    f = open('/Volumes/MacOS/nastia/Desktop/password.txt', 'r')
    for line in f:
        line = line.rstrip('\n')
        payload = {"login": "super_admin", "password": line}
        requests1 = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data=payload)
        cookies_value = dict(requests1.cookies)

        requests2 = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies=cookies_value)
        if requests2.text == "You are authorized":
            print(f"Логин:'super_admin' и правильный пароль: '{line}'")
            return "Найден!"
    return "Пароль не найден"

print(find_password())







