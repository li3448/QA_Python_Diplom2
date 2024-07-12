
import random
import string
import requests
import allure
from data import StatusCodes as CODE, ResponseKeys as KEYS, Endpoints as e
#
# Вспомогательные методы проверки ответа на запрос к API
class HelpersOnCheck:

    @staticmethod
    @allure.step('Проверяем наличие ключа в ответе')
    def check_key_in_body(response_body, key):
        # проверяем что в ответе есть ключ key
        assert key in response_body, f'В ответе отсутствует ключ "{key}", получен ответ: "{response_body}"'
        return response_body[key]
    @staticmethod
    @allure.step('Проверяем значение ключа в ответе')
    def check_key_and_value_in_body(response_body, key, value):
        # проверяем наличие ключа в ответе
        assert key in response_body, f'В ответе отсутствует ключ "{key}", получен ответ: "{response_body}"'
        # проверяем значение ключа в ответе
        received_value = response_body[key]
        assert received_value == value, f'Получено неверное значение ключа "{key}": ожидалось "{value}", получено "{received_value}"'
        return received_value
    @staticmethod
    @allure.step('Проверяем код ответа')
    def check_status_code(response, expected_code):
        # проверяем что получен код ответа expected_code
        received_code = response.status_code
        assert received_code == expected_code, f'Неверный код в ответе: ожидался {expected_code}, получен "{received_code}", ответ: "{response.text}"'
    @staticmethod
    @allure.step('Проверяем значение поля "success" в ответе')
    def check_success(response, expected_value):
        received_text = response.text
        # проверяем что в ответе есть "success"
        assert KEYS.SUCCESS_KEY in response.json(), f'В ответе отсутствует ключ "{KEYS.SUCCESS_KEY}", получено: "{received_text}"'
        # проверяем тело ответа
        received_body = response.json()
        # проверяем сообщение об ошибке
        received_value = received_body[KEYS.SUCCESS_KEY]
        assert received_value == expected_value, f'Получено неверное значение поля "{KEYS.SUCCESS_KEY}": ожидалось "{expected_value}", получено "{received_value}"'
        return received_body
    @staticmethod
    @allure.step('Проверяем, что запрос выполнен успешно')
    def check_success_ok(response):
        # проверяем что получен код ответа 200
        HelpersOnCheck.check_status_code(response, CODE.OK)
        # проверяем в теле ответа: { "success" = True }
        return HelpersOnCheck.check_success(response, True)
    @staticmethod
    @allure.step('Проверяем код ошибки и сообщение об ошибке')
    def check_not_success_error_message(response, code, message):
        # проверяем что получен код ответа = code
        HelpersOnCheck.check_status_code(response, code)
        # проверяем в теле ответа: { "success" = False }
        received_body = HelpersOnCheck.check_success(response, False)
        # проверяем сообщение в теле ответа: { "message" = message }
        HelpersOnCheck.check_message(received_body, message)
        return received_body
    @staticmethod
    @allure.step('Проверяем сообщение в ответе')
    def check_message(received_body, expected_message):
        # проверяем что в ответе есть "message"
        assert KEYS.MESSAGE_KEY in received_body, f'В ответе отсутствует ключ "{KEYS.MESSAGE_KEY}", получено: "{received_body}"'
        # проверяем сообщение об ошибке
        received_message = received_body[KEYS.MESSAGE_KEY]
        assert received_message == expected_message, f'Получено неверное значение поля "{KEYS.MESSAGE_KEY}":\nожидалось "{expected_message}"\nполучено "{received_message}"'
        return received_message
    #
    # Проверка полученных данных пользователя после создания/авторизации пользователя
    @staticmethod
    @allure.step('Проверяем полученные данные пользователя - поле "user"')
    def check_user_data(received_body, user_data):
        # проверяем наличие в ответе ключа "user" и получаем его значение - словарь
        received_user_data = HelpersOnCheck.check_key_in_body(received_body, KEYS.USER_KEY)
        assert type(received_user_data) is dict
        # проверяем в словаре "user" наличие и значения полей "email" и "name"
        email = user_data[KEYS.EMAIL_KEY]
        name = user_data[KEYS.NAME_KEY]
        HelpersOnCheck.check_key_and_value_in_body(received_user_data, KEYS.EMAIL_KEY, email)
        HelpersOnCheck.check_key_and_value_in_body(received_user_data, KEYS.NAME_KEY, name)
    @staticmethod
    @allure.step('Проверяем полученные данные пользователя после регистрации/авторизации')
    def check_new_user_data(received_body, user_data):
        # проверяем наличие в ответе ключа "user" и значения полей "email" и "name"
        HelpersOnCheck.check_user_data(received_body, user_data)

        # проверяем наличие в ответе ключа "accessToken" и получаем его значение - строку "Bearer ..."
        auth_token = HelpersOnCheck.check_key_in_body(received_body, KEYS.ACCESS_TOKEN)
        # проверяем формат токена: "Bearer ..."
        assert (type(auth_token) is str and
                e.ACCESS_TOKEN_PREFIX in auth_token and
                len(auth_token) > len(
                    e.ACCESS_TOKEN_PREFIX)), f'Получено неверное значение ключа "{KEYS.ACCESS_TOKEN}": неправильный формат "{KEYS.ACCESS_TOKEN}"={auth_token}'
        # проверяем наличие в ответе ключа "refreshToken" и получаем его значение - строку `"..."
        refresh_token = HelpersOnCheck.check_key_in_body(received_body, KEYS.REFRESH_TOKEN)
        # проверяем токен
        assert (type(refresh_token) is str and
                len(refresh_token) > 0), f'Получено неверное значение ключа "{KEYS.REFRESH_TOKEN}": неправильный формат "{KEYS.REFRESH_TOKEN}"={refresh_token}'
        # возвращаем полученные токены
        return auth_token, refresh_token
    #
    # Проверка полученных данных после создания заказа
    @staticmethod
    @allure.step('Проверяем полученный ответ после запроса создания заказа')
    # def check_order_data(received_body):
    def check_order_data(response):
        # проверяем что получен код ответа 200
        HelpersOnCheck.check_status_code(response, CODE.OK)
        # проверяем в теле ответа: { "success" = True }
        received_body = HelpersOnCheck.check_success(response, True)
        # проверяем полученные данные заказа в теле ответа
        # проверяем наличие в ответе ключа "name" и получаем его значение - строка
        order_name = HelpersOnCheck.check_key_in_body(received_body, KEYS.NAME_KEY)
        assert type(order_name) is str, f'Получено неверное значение ключа "{KEYS.NAME_KEY}": ожидалось - строка, получено значение {order_name} тип {type(order_name)}'
        # проверяем наличие в ответе ключа "order" и получаем его значение - словарь
        received_order_data = HelpersOnCheck.check_key_in_body(received_body, KEYS.ORDER_KEY)
        assert type(received_order_data) is dict
        # проверяем в словаре "order" наличие и значения поля "number"
        order_number = HelpersOnCheck.check_key_in_body(received_order_data, KEYS.NUMBER_KEY)
        assert str(
            order_number).isdigit(), f'Получено неверное значение ключа "{KEYS.NUMBER_KEY}": ожидалось - число, получено значение {order_number} тип {type(order_number)}'
        return order_number, order_name
    @staticmethod
    @allure.step('Проверяем списки ингредиентов по типам - булки, начинки, соусы')
    def check_ingredients(buns_list, fillings_list, sauces_list):
        assert type(buns_list) is list and len(buns_list) != 0, f'TestCreateOrder ошибка - в списке ингредиентов нет булок'
        assert type(fillings_list) is list and len(fillings_list) != 0, f'TestCreateOrder ошибка - в списке ингредиентов нет начинок'
        assert type(sauces_list) is list and len(sauces_list) != 0, f'TestCreateOrder ошибка - в списке ингредиентов нет соусов'
    @staticmethod
    @allure.step('Проверяем полученный ответ на запрос списка ингредиентов')
    def check_ingredients_list(response):
        # проверяем что получен код ответа 200
        HelpersOnCheck.check_status_code(response, CODE.OK)
        # проверяем в теле ответа: { "success" = True }
        received_body = HelpersOnCheck.check_success(response, True)
        # проверяем наличие в ответе ключа "data" и получаем его значение - список ингредиентов (словарь)
        ingredients = HelpersOnCheck.check_key_in_body(received_body, KEYS.DATA)
        # проверяем что поле data содержит список и возвращаем его
        assert type(ingredients) is list and len(ingredients) > 0
        return ingredients
    #
    # Проверка полученного ответа на запрос получения заказов пользователя
    @staticmethod
    @allure.step('Проверяем в полученном ответе информацию о заказе')
    def check_received_order_data(received_order_data, order_number, order_name, ingredients_list):
        # проверяем полученные данные заказа
        assert type(received_order_data) is dict
        # проверяем что поле "_id" строка
        received_order_id = HelpersOnCheck.check_key_in_body(received_order_data, KEYS.ID_KEY)
        assert type(received_order_id) is str
        # проверяем что поле "number" = order_number
        HelpersOnCheck.check_key_and_value_in_body(received_order_data, KEYS.NUMBER_KEY, order_number)
        # проверяем что поле "name" = order_name
        HelpersOnCheck.check_key_and_value_in_body(received_order_data, KEYS.NAME_KEY, order_name)
        # проверяем поле "ingredients"
        received_ingredients_list = HelpersOnCheck.check_key_in_body(received_order_data, KEYS.INGREDIENTS)
        assert type(received_ingredients_list) is list
        # проверяем что количество ингредиентов совпадает с заданным
        assert len(received_ingredients_list) == len(ingredients_list)
    @staticmethod
    @allure.step('Проверяем в полученном ответе поле "orders" - список заказов')
    def check_received_orders_list(received_body, amount):
        # проверяем наличие в ответе ключа "orders" и получаем его значение - список
        received_orders_list = HelpersOnCheck.check_key_in_body(received_body, KEYS.ORDERS_KEY)
        assert type(received_orders_list) is list
        # проверяем что количество заказов в списке = amount
        assert len(received_orders_list) == amount
        return received_orders_list

    @staticmethod
    @allure.step('Проверяем в полученном ответе поля "total" и "totalToday"')
    def check_received_orders_info(received_body, amount):
        # проверяем поля "total" и "totalToday" в списке заказов "orders" (в теле ответа)
        HelpersOnCheck.check_key_and_value_in_body(received_body, KEYS.TOTAL_KEY, amount)
        HelpersOnCheck.check_key_and_value_in_body(received_body, KEYS.TOTAL_TODAY_KEY, amount)


    @staticmethod
    @allure.step('Проверяем в полученном ответе поле "total"')
    def check_received_orders_total(received_body, amount):
        # проверяем поле "total" в списке заказов "orders" (в теле ответа)
        HelpersOnCheck.check_key_and_value_in_body(received_body, KEYS.TOTAL_KEY, amount)


    @staticmethod
    @allure.step('Проверяем в полученном ответе поле "totalToday"')
    def check_received_orders_total_today(received_body, amount):
        # проверяем поле "totalToday" в списке заказов "orders" (в теле ответа)
        HelpersOnCheck.check_key_and_value_in_body(received_body, KEYS.TOTAL_TODAY_KEY, amount)

class HelpersOnCreateUser:
    # Вспомогательные функции

    @staticmethod
    def generate_random_string(length):
        """
        Метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки.
        :param length: (int) длина строки
        :return: (str) строка
        """
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string


    @staticmethod
    @allure.step('Отправляем запрос на создание нового пользователя')
    def try_to_create_user(user_data):
        return Requests.request_on_create_user(user_data)


    @staticmethod
    @allure.step('Авторизация пользователя')
    def try_to_login_user(email, password):
        payload = {KEYS.EMAIL_KEY: email, KEYS.PASSWORD_KEY: password}
        return Requests.request_on_login_user(payload)


    @staticmethod
    @allure.step('Удаляем пользователя')
    def try_to_delete_user(auth_token):
        headers = {KEYS.AUTH_TOKEN_KEY: auth_token}
        return Requests.request_on_delete_user(headers)


    @staticmethod
    @allure.step('Обновляем данные пользователя')
    def try_to_update_user(user_data, auth_token=None):
        if auth_token is not None:
            headers = {KEYS.AUTH_TOKEN_KEY: auth_token}
        else:
            headers = None
        return Requests.request_on_update_user(user_data, headers)


    @staticmethod
    @allure.step('Выход пользователя из системы')
    def try_to_logout_user(token):
        payload = {KEYS.TOKEN_KEY: token}
        return Requests.request_on_logout_user(payload)


    # Вспомогательные методы для работы с заказами
    @staticmethod
    @allure.step('Отправляем запрос на создание заказа')
    def try_to_create_order(ingredient_list, auth_token=None):  # ingredient_list - список _id ингредиентов
        if auth_token is not None:
            headers = {
                KEYS.AUTH_TOKEN_KEY: auth_token,  # "Autorization": auth_token
            }
        else:
            headers = None

        payload = {
            KEYS.INGREDIENTS: ingredient_list,  # "ingredients": ingredient_list,
        }
        return Requests.request_on_create_order(payload, headers)


    @staticmethod
    @allure.step('Отправляем запрос на получение заказов пользователя')
    def try_to_get_user_orders(auth_token=None):
        if auth_token is not None:
            headers = {
                KEYS.AUTH_TOKEN_KEY: auth_token,  # "Autorization": auth_token
            }
        else:
            headers = None
        return Requests.request_on_get_user_orders(headers)


    # генерируем логин, пароль и имя пользователя
    @staticmethod
    @allure.step('Генерируем данные нового пользователя: email, password, name')
    def generate_random_user_data():
        email = HelpersOnCreateUser.generate_random_string(10) + '@mail.ru'
        password = HelpersOnCreateUser.generate_random_string(10)
        name = HelpersOnCreateUser.generate_random_string(10)
        # собираем тело запроса
        user_data = {
            KEYS.EMAIL_KEY: email,  # "email"
            KEYS.PASSWORD_KEY: password,  # "password"
            KEYS.NAME_KEY: name  # "name"
        }
        # возвращаем словарь
        return user_data


    @staticmethod
    @allure.step('Генерируем новое имя пользователя: поле "name"')
    def generate_random_user_name():
        return HelpersOnCreateUser.generate_random_string(10)


    @staticmethod
    @allure.step('Генерируем email пользователя: поле "email"')
    def generate_random_user_login():
        return HelpersOnCreateUser.generate_random_string(10) + '@mail.ru'


    @staticmethod
    @allure.step('Генерируем пароль пользователя: поле "password"')
    def generate_random_user_password():
        return HelpersOnCreateUser.generate_random_string(10)


    # метод создания нового пользователя и проверки полученного ответа
    @staticmethod
    @allure.step('Создаем нового пользователя')
    def create_and_check_user(user_data=None):
        # генерируем уникальные данные нового пользователя
        if user_data is None:
            user_data = HelpersOnCreateUser.generate_random_user_data()
        # отправляем запрос на создание пользователя
        response = HelpersOnCreateUser.try_to_create_user(user_data)
        # проверяем что получен код ответа 200
        # проверяем в теле ответа: { "success" = True }
        received_body = HelpersOnCreateUser.check_success(response, True)
        # проверяем полученные данные пользователя и возвращаем 2 токена
        auth_token, refresh_token = HelpersOnCheck.check_new_user_data(received_body, user_data)
        return auth_token, refresh_token


    # вспомогательный метод создания нового пользователя для других тестов
    @staticmethod
    @allure.step('Создаем нового пользователя')
    def create_user(user_data=None):
        # генерируем уникальные данные нового пользователя
        if user_data is None:
            user_data = HelpersOnCreateUser.generate_random_user_data()
        # отправляем запрос на создание пользователя
        response = HelpersOnCreateUser.try_to_create_user(user_data)
        # проверяем что получен код ответа 200
        HelpersOnCheck.check_status_code(response, CODE.OK)
        # получаем токены пользователя
        received_body = response.json()
        auth_token = received_body[KEYS.ACCESS_TOKEN]
        refresh_token = received_body[KEYS.REFRESH_TOKEN]
        return auth_token, refresh_token


    # Вспомогательные методы для работы с заказами
    @staticmethod
    @allure.step('Создаем заказ и проверяем полученные в ответе данные')
    def create_order(ingredient_list, auth_token=None):
        # создаем заказ
        response = HelpersOnCreateUser.try_to_create_order(ingredient_list, auth_token)
        # проверяем что получен код ответа 200
        HelpersOnCheck.check_status_code(response, CODE.OK)
        # проверяем в теле ответа: { "success" = True }
        received_body = HelpersOnCheck.check_success(response, True)
        # Получаем данные заказа - name, number
        order_name = HelpersOnCheck.check_key_in_body(received_body, KEYS.NAME_KEY)
        received_order_data = HelpersOnCheck.check_key_in_body(received_body, KEYS.ORDER_KEY)
        order_number = HelpersOnCheck.check_key_in_body(received_order_data, KEYS.NUMBER_KEY)

        return order_number, order_name
#
# Вспомогательные методы для работы с ингредиентами
class HelpersOnGetIngredients:

    @staticmethod
    @allure.step('Отправляем запрос на получение списка ингредиентов от API')
    def try_to_get_ingredients():
        # Отправляем запрос на получение списка ингредиентов
        return Requests.request_on_get_ingredients()


    @staticmethod
    @allure.step('Получаем списки булок из общего списка ингредиентов')
    def get_buns_list(ingredients):
        buns_list = []
        for item in ingredients:
            if item['type'] == 'bun':
                buns_list.append(item)
        return buns_list


    @staticmethod
    @allure.step('Получаем списки начинок из общего списка ингредиентов')
    def get_fillings_list(ingredients):
        fillings_list = []
        for item in ingredients:
            if item['type'] == 'main':
                fillings_list.append(item)
        return fillings_list


    @staticmethod
    @allure.step('Получаем списки соусов из общего списка ингредиентов')
    def get_sauces_list(ingredients):
        sauces_list = []
        for item in ingredients:
            if item['type'] == 'sauce':
                sauces_list.append(item)
        return sauces_list


    # Получаем данные об ингредиентах от API
    @staticmethod
    @allure.step('Получаем данные об ингредиентах')
    def get_ingredients():
        response = HelpersOnGetIngredients.try_to_get_ingredients()
        # проверяем что получен код ответа 200
        return HelpersOnCheck.check_ingredients_list(response)


class Requests:

    @staticmethod
    @allure.step('Отправляем API-запрос на создание пользователя')
    def request_on_create_user(payload):
        request_url = f'{e.SERVER_URL}{e.CREATE_USER}'
        return requests.post(f'{request_url}', json=payload)

    @staticmethod
    @allure.step('Отправляем API-запрос на авторизацию пользователя')
    def request_on_login_user(payload):
        request_url = f'{e.SERVER_URL}{e.LOGIN_USER}'
        return requests.post(f'{request_url}', json=payload)

    @staticmethod
    @allure.step('Отправляем API-запрос на выход пользователя из системы')
    def request_on_logout_user(payload):
        request_url = f'{e.SERVER_URL}{e.LOGOUT_USER}'
        return requests.post(f'{request_url}', json=payload)

    @staticmethod
    @allure.step('Отправляем API-запрос на удаление пользователя')
    def request_on_delete_user(headers):
        request_url = f'{e.SERVER_URL}{e.DELETE_USER}'
        return requests.delete(f'{request_url}', headers=headers)

    @staticmethod
    @allure.step('Отправляем API-запрос на обновление данных пользователя')
    def request_on_update_user(payload, headers=None):
        request_url = f'{e.SERVER_URL}{e.UPDATE_USER}'
        return requests.patch(f'{request_url}', headers=headers, json=payload)

    @staticmethod
    @allure.step('Отправляем API-запрос на изменение пароля пользователя')
    def request_on_reset_password(payload):
        request_url = f'{e.SERVER_URL}{e.RESET_PASSWORD}'
        return requests.post(f'{request_url}', json=payload)

    @staticmethod
    @allure.step('Отправляем API-запрос на получение ингредиентов')
    def request_on_get_ingredients():
        request_url = f'{e.SERVER_URL}{e.GET_INGREDIENTS}'
        return requests.get(f'{request_url}')

    @staticmethod
    @allure.step('Отправляем API-запрос на создание заказа')
    def request_on_create_order(payload, headers=None):
        request_url = f'{e.SERVER_URL}{e.CREATE_ORDER}'
        return requests.post(f'{request_url}', headers=headers, json=payload)

    @staticmethod
    @allure.step('Отправляем API-запрос на получение заказов пользователя')
    def request_on_get_user_orders(headers=None):
        request_url = f'{e.SERVER_URL}{e.GET_USER_ORDERS}'
        return requests.get(f'{request_url}', headers=headers)

