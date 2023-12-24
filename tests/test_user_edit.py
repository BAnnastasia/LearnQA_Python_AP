import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserEdit (BaseCase):

    def register(self):
        register_data = self.prepare_registrstion_data()
        response1 = MyRequests.post(
            "/user",
            data=register_data
        )
        Assertions.asser_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        register_data["id"] = self.get_json_value(response1, "id")
        print(f"register_data {register_data}")

        return register_data

    def login(self, email, password):
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        login_data["auth_sid"] = self.get_cookie(response2, "auth_sid")
        login_data["token"] = self.get_header(response2, "x-csrf-token")
        return login_data

    def edit(self, user_id, data, scode, x_csrf_token=None, auth_sid=None, expected_content=None):

        if (x_csrf_token is not None) & (auth_sid is not None):
            response3 = MyRequests.put(
                f"/user/{user_id}",
                headers={"x-csrf-token": x_csrf_token},
                cookies={"auth_sid": auth_sid},
                data=data
            )
            print(f"EDIT {response3.status_code}")
            print(f"EDIT {response3.content}")
            Assertions.asser_code_status(response3, scode)

        elif (x_csrf_token is None) & (auth_sid is None):
            response3 = MyRequests.put(
                f"/user/{user_id}",
                data=data
            )
            if expected_content is not None:
                Assertions.asser_content(response3, expected_content)

        return
    def get(self, user_id, name, scode, expected_value, x_csrf_token=None, auth_sid=None, expected_content=None):

            response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": x_csrf_token},
            cookies={"auth_sid": auth_sid}

            )
            print(f"GET {response4.status_code}")
            print(f"GET {response4.content}")

            Assertions.asser_code_status(response4,scode)
            Assertions.assert_json_value_by_name(response4,
                                                 name,
                                                 expected_value,
                                                 f"Expected parameter and value: '{name}':'{expected_value}' not found in json. Actual content: {response4.content} "
                                                 )

            if expected_content is not None:
                Assertions.asser_content(response4,expected_content)
            return


    def test_edit_just_created_user(self, password=None):
        #REGISTER
        register_data =self.register()
        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = register_data['id']

        #LOGIN
        login_value = self.login(email, password)
        auth_sid = login_value["auth_sid"]
        token = login_value["token"]

        #EDIT
        # def edit(self, user_id, data,scode, x_csrf_token=None, auth_sid=None, expected_content=None):
        new_name = "Changed Name"
        change_value = {"firstName": new_name }
        self.edit(user_id, change_value, 200, token, auth_sid)


        #GET
        #def get(self, user_id, name, scode, expected_value, x_csrf_token=None, auth_sid=None, expected_content=None):
        name = "firstName"
        self.get(user_id,name,200,new_name,token,auth_sid)


    def test_edit_user_not_auth(self, password=None):
        # 4Ex17-1 Попытаемся изменить данные пользователя, будучи неавторизованным
        # REGISTER
        register_data = self.register()
        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = register_data['id']

        # EDIT
        new_name = "Changed Name"
        change_value = {"firstName": new_name}
        self.edit(user_id, change_value, 400,None, None, "Auth token not supplied")


        # LOGIN
        login_value = self.login(email, password)
        auth_sid = login_value["auth_sid"]
        token = login_value["token"]

        # GET
        # def get(self, user_id, name, scode, expected_value, x_csrf_token=None, auth_sid=None, expected_content=None):
        name = "firstName"
        expected_value = "lernqa"
        self.get(user_id, name, 200, expected_value, token, auth_sid)


    def test_edit_user_auth_with_other_user(self, password=None):
        # 4Ex17-2 Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем

        # REGISTER
        register_data = self.register()
        email1 = register_data['email']
        first_name = register_data['firstName']
        password1 = register_data['password']
        user_id = register_data['id']

        # LOGIN
        email2 = "vinkotov@example.com"
        password2 = "1234"
        login_value = self.login(email2, password2)
        auth_sid2 = login_value["auth_sid"]
        token2 = login_value["token"]

        # EDIT
        new_name = "Changed Name"
        change_value = {"firstName": new_name}
        self.edit(user_id, change_value, 400,token2, auth_sid2, "Auth token not supplied")

        # LOGIN
        login_value = self.login(email1, password1)
        auth_sid1 = login_value["auth_sid"]
        token1 = login_value["token"]

        # GET
        # def get(self, user_id, name, scode, expected_value, x_csrf_token=None, auth_sid=None, expected_content=None):
        name = "firstName"
        expected_value = "lernqa"
        self.get(user_id, name, 200, expected_value, token1, auth_sid1)


    def test_edit_users_email_address_without_atsign(self):
        # 4Ex17-3 Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @ #
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

        # EDIT
        # def edit(self, user_id, data,scode, x_csrf_token=None, auth_sid=None, expected_content=None):
        new_email = "testemail.example.com"
        change_value = {"email": new_email}
        self.edit(user_id, change_value, 400, token, auth_sid,"Invalid email format")


        # GET
        expected_email =email
        self.get(user_id, "email", 200, expected_email, token, auth_sid)

    def test_edit_users_firstname(self):
        #4Ex17-4 Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ
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

        # EDIT
        # def edit(self, user_id, data,scode, x_csrf_token=None, auth_sid=None, expected_content=None):
        new_name = "C"
        change_value = {"firstName": new_name}
        self.edit(user_id, change_value, 400, token, auth_sid,"Too short value for field firstName")

        # GET
        # def get(self, user_id, name, scode, expected_value, x_csrf_token=None, auth_sid=None, expected_content=None):
        name = "firstName"
        expected_name = first_name
        expected_content = "Wrong name of the user after edit"
        self.get(user_id, name, 200, expected_name, token, auth_sid)