import requests

class TestExercise11:
    def test_check(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        request1 = requests.get(url)
        cookies_dict = dict(request1.cookies)
        print(cookies_dict)
        assert request1.status_code == 200, "Wrong response code"
        assert "HomeWork" in cookies_dict, "There is not 'HomeWork' in the cookies"
        assert cookies_dict['HomeWork'] == "hw_value", "There is not 'hw_value' value in the 'HomeWork' parameter"