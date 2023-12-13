import requests

class TestExercise11:
    def test_check(self):
        url = " https://playground.learnqa.ru/api/homework_header"
        request1 = requests.get(url)
        expected_parameter = "x-secret-homework-header"
        expected_value = "Some secret value"
        headers_dict = request1.headers
        print(headers_dict) #'x-secret-homework-header': 'Some secret value'
        assert request1.status_code == 200, "Wrong response code"
        assert expected_parameter in headers_dict, f"There is not '{expected_parameter}' in the headers"
        assert headers_dict[expected_parameter] == expected_value, f"There is not '{expected_value}' value in the '{expected_parameter}' parameter"