from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure
import os
import subprocess
import platform
import atexit
import datetime

def pytest_write_env():
    f = open("./test_results/environment.properties", "w")
    f.write(f"Python:{subprocess.getoutput('python --version')}\n")
    f.write(f"Platform:{platform.system()}-{platform.release()}\n")
    f.write(f"Date:{str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))}\n")
    f.write(f"ENV:{os.environ.get('ENV')}\n")
    f.close()
atexit.register(pytest_write_env)

@allure.epic("User delete cases")
class TestUserDelete (BaseCase):

    def login(self, email, password):
        with allure.step("login: checking status_code 200"):
                login_data = {
                    'email': email,
                    'password': password
                }
                response2 = MyRequests.post("/user/login", data=login_data)
                Assertions.asser_code_status(response2,200)
                print(f"Login {response2.status_code} : {response2.content}")
                login_data["auth_sid"] = self.get_cookie(response2, "auth_sid")
                login_data["token"] = self.get_header(response2, "x-csrf-token")
                login_data["user_id"] = self.get_json_value(response2, "user_id")

        return login_data
    def register(self):
        register_data = self.prepare_registrstion_data()
        with allure.step("Register: check status_code 200"):
            response1 = MyRequests.post(
                "/user",
                data=register_data
            )
            Assertions.asser_code_status(response1, 200)
        with allure.step(f"Register: searching 'id' in response"):
            Assertions.assert_json_has_key(response1, "id")
            register_data["id"] = self.get_json_value(response1, "id")
            print(f"register_data {register_data}")
            return register_data

    def delete(self,user_id, status_code, token, auth_sid,expected_content = None):
        with allure.step(f"Delete: checking status_code{status_code}"):
            response5 = MyRequests.delete(f"/user/{user_id}",
                                          headers={"x-csrf-token": token},
                                          cookies={"auth_sid": auth_sid})
            print(f"DELETE {response5.status_code}")
            print(f"DELETE {response5.content}")
            print(f"DELETE url {response5.url}")
            Assertions.asser_code_status(response5, status_code)
            if expected_content is not None:
                with allure.step(f"Delete: checking message in content {expected_content}"):
                    Assertions.asser_content(response5, expected_content)
            return
    @allure.description("This test checks that it is impossible to delete a user with ID 2")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_user_id2(self, password=None):
        # 4Ex18-1 попытка удалить пользователя по ID 2.
        # LOGIN
        email = "vinkotov@example.com"
        password = "1234"
        login_value = self.login(email, password)
        auth_sid = login_value["auth_sid"]
        token = login_value["token"]

        #DELETE
        user_id = 2
        self.delete(user_id, 400, token, auth_sid, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")

        #LOGIN2
        login_value =self.login(email, password)
        user_id = login_value["user_id"]
        with allure.step("checking user_id == 2 is not deleted"):
            assert user_id == 2, f"User id:'{user_id}' != expected value user_id=2"

    @allure.description("This test successfully deletes user")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_delete_user(self, password=None):
    # 4Ex18-2 Создать пользователя, авторизоваться из-под него, удалить, затем попробовать получить его данные по
    # ID и убедиться, что пользователь действительно удален.

        # REGISTER
        register_data = self.register()
        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = register_data['id']

        # LOGIN
        login_value = self.login(email, password)
        auth_sid = login_value["auth_sid"]
        token = login_value["token"]

        # DELETE
        self.delete(user_id, 200, token, auth_sid)

        #GET
        response_test = MyRequests.get(
        f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        with allure.step("GET: checking status_code 404"):
            Assertions.asser_code_status(response_test,404)
        with allure.step("GET: checking in response contend "):
            Assertions.asser_content(response_test,"User not found")

    @allure.description("This test checks that it will not be possible to delete a user authorized under another user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_user_auth_with_other_user(self, password=None):
        # 4Ex18-3 попробовать удалить пользователя, будучи авторизованными другим пользователем.

        # REGISTER 1
        register_data1 = self.register()
        email1 = register_data1['email']
        password1 = register_data1['password']
        user_id = register_data1["id"]
        print(f"user1 {user_id}")

        # REGISTER 2
        register_data2 = self.register()
        email2 = register_data2['email']
        password2 = register_data2['password']
        user_id2 = register_data2['id']
        print(f"user2 {user_id2}")

        # LOGIN2
        login_value2 = self.login(email2, password2)
        auth_sid2 = login_value2["auth_sid"]
        token2 = login_value2["token"]

        # DELETE
        self.delete(user_id, 200, token2, auth_sid2)

        #LOGIN1
        login_value1 = self.login(email1, password1)
        auth_sid1 = login_value1["auth_sid"]
        token1 = login_value1["token"]
        user_id1 = login_value1["user_id"]
        with allure.step(f"Login: compare users id '{str(user_id1)}' and '{user_id}'"):
            assert str(user_id1) == user_id, f"User id:{user_id1} != expected value {user_id}"
