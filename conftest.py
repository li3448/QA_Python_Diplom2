import allure
import pytest

from helpers import HelpersOnCreateUser
from tests.old_test_create_order import TestCreateOrder
from helpers import HelpersOnCheck
from helpers import HelpersOnGetIngredients

@pytest.fixture
@allure.title('Генерация пейлоада')
def generate_payload():
    # генерируем данные нового пользователя: email, password, user_name
    user_data = HelpersOnCreateUser.generate_random_user_data()
    return user_data

@pytest.fixture
@allure.title('Создание пользователя')
def create_user(generate_payload):
    user_data = generate_payload
@allure.title('Создаем пользователя и инициализируем данные для удаления после завершения работы')
def setup_user():
    # генерируем данные нового пользователя: email, password, user_name
    user_data = HelpersOnCreateUser.generate_random_user_data()
 
    # отправляем запрос на создание пользователя
    auth_token, refresh_token = HelpersOnCreateUser.create_user(user_data)
    # сохраняем полученные данные пользователя
    yield user_data, auth_token


@pytest.fixture(autouse=True)
@allure.title('Удаление пользователя после завершения работы')
def delete_user(create_user):
    user_data, auth_token = create_user
    # Удаляем созданного пользователя
    HelpersOnCreateUser.try_to_delete_user(auth_token)


    # Удаляем созданного пользователя
    HelpersOnCreateUser.try_to_delete_user(auth_token)

@pytest.fixture
@allure.title('Инициализируем списки ингредиентов')
def setup_ingredients():
    ingredients = HelpersOnCheck.get_ingredients()
    TestCreateOrder.buns_list = HelpersOnCheck.get_buns_list(ingredients)
    TestCreateOrder.fillings_list = HelpersOnCheck.get_fillings_list(ingredients)
    TestCreateOrder.sauces_list = HelpersOnCheck.get_sauces_list(ingredients)
    HelpersOnCheck.check_ingredients(TestCreateOrder.buns_list, TestCreateOrder.fillings_list, TestCreateOrder.sauces_list)


