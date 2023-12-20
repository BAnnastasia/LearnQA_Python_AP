import requests
import string
import random
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime



class TestUserRegister(BaseCase):
    def setup(self):
        base_part ="lernqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"

    def call(self, password, username, firstName, lastName, email):
        body = {
            'password': password,
            'username': username,
            'firstName': firstName,
            'lastName': lastName,
            'email': email
        }
        # print(body)
        return requests.post("https://playground.learnqa.ru/api/user", data=body)

    def test_create_user_successfully(self):

        response = self.call('123', 'lernqa', 'lernqa', 'learnqa', self.email)
        Assertions.asser_code_status(response,200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        response = self.call('123','lernqa','lernqa','lernqa', email)
        Assertions.asser_code_status(response,400)
        Assertions.asser_content(response, f"Users with email '{email}' already exists")


    def test_create_user_with_email_address_without_atsign(self): # 4Ex15 1-Создание пользователя с некорректным email - без символа @
        email = '"vinkotovexample.com"'
        response = self.call('123', 'lernqa', 'lernqa', 'lernqa', email)
        Assertions.asser_code_status(response, 400)
        Assertions.asser_content(response, "Invalid email format")

    parameters = [
            ('password'),
            ('username'),
            ('firstName'),
            ('lastName'),
            ('email' )
        ]

    @pytest.mark.parametrize('parameter', parameters)
    def test_create_user_without_parameter(  # 4Ex15 2 Создание пользователя без указания одного из полей - с помощью @parametrize необходимо проверить
            self, parameter):  #, что отсутствие любого параметра не дает зарегистрировать пользователя

        body = {
            'password': '123',
            'username': 'lernqa',
            'firstName': 'lernqa',
            'lastName': 'lernqa',
            'email': self.email
        }
        del body[parameter]
        response = requests.post("https://playground.learnqa.ru/api/user", data=body)
        Assertions.asser_code_status(response,400)
        Assertions.asser_content(response,f"The following required params are missed: {parameter}")


    def test_create_user_with_short_username(self): #4Ex15 3 Создание пользователя с очень коротким именем в один символ

        res = ''.join(random.choices(string.ascii_lowercase, k=1))
        response = self.call('123', res, 'lernqa', 'lernqa', self.email)
        Assertions.asser_code_status(response, 400)
        Assertions.asser_content(response,"The value of 'username' field is too short")

    def test_create_user_with_long_username(self): #4Ex15 4 Создание пользователя с очень длинным именем - длиннее 250 символов

        res = ''.join(random.choices(string.ascii_lowercase, k=251))
        response = self.call('123', res, 'lernqa', 'learnqa', self.email)
        Assertions.asser_code_status(response, 400)
        Assertions.asser_content(response, "The value of 'username' field is too long")
