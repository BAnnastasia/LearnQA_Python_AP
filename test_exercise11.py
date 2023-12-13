import requests

class TestExercise11:
    def test_check(self):
        expected_parameter = "HomeWork"
        expected_value = "hw_value"
        url = "https://playground.learnqa.ru/api/homework_cookie"
        request1 = requests.get(url)
        cookies_dict = dict(request1.cookies)
        print(cookies_dict)
        assert request1.status_code == 200, "Wrong response code"
        assert expected_parameter in cookies_dict, f"There is not '{expected_parameter}' in the cookies"
        assert cookies_dict[expected_parameter] == expected_value, f"There is not '{expected_value}' value in the '{expected_parameter}' parameter"