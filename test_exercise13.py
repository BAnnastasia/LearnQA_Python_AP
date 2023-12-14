import pytest
import requests

class TestExercise13:
    data_test = [
        ("Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
         "Mobile", "No","Android"),
        ("Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
         "Mobile", "Chrome", "iOS"),
        ("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "Googlebot", "Unknown", "Unknown"),
        ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
         "Web", "Chrome", "No"),
        ("Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        "Mobile", "No", "iPhone")
    ]

    @pytest.mark.parametrize('user_agent,platform,browser,device', data_test)
    def test_check_user_agent(self, user_agent, platform, browser, device):
        requests1 = requests.get(
            "https://playground.learnqa.ru/ajax/api/user_agent_check",
            headers={"User-Agent": user_agent}
        )
        assert requests1.status_code == 200, "Wrong response code"

        assert "platform" in requests1.json(),f"There is no 'platform' parameter in the response, User-Agent: '{user_agent}"
        assert platform == requests1.json()['platform'], (f"Platform: '{platform}' from data_test is not equal to platform from response: '{requests1.json()['platform']}'  "
                                                          f"User-Agent: '{user_agent}'")

        assert "browser" in requests1.json(), f"There is  no 'browser' parameter in the response, User-Agent: '{user_agent}'"
        assert browser == requests1.json()['browser'],  (f"Browser: '{browser}' from data_test is not equal to browser from response: '{requests1.json()['browser']}'  "
                                                         f"User-Agent: '{user_agent}'")

        assert "device" in requests1.json(), f"There is  no 'device' parameter in the response, User-Agent: '{user_agent}"
        assert device == requests1.json()['device'], (f"Device: '{device}' from data_test is not equal to device from response: '{requests1.json()['device']}'  "
                                                      f"User-Agent: '{user_agent}")