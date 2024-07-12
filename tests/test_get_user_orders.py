import pytest
import allure

from data import StatusCodes as CODE
from data import ResponseKeys as KEYS
from data import ResponseMessages as message

from helpers import HelpersOnCheck
from helpers import HelpersOnCreateUser
from helpers import HelpersOnGetIngredients


@pytest.fixture(scope='class')
@allure.title('Получаем данные об ингредиентах от API и инициализируем списки ингредиентов')
def setup_ingredients():
    ingredients = HelpersOnGetIngredients.get_ingredients()
    TestGetUserOrders.buns_list = HelpersOnGetIngredients.get_buns_list(ingredients)
    TestGetUserOrders.fillings_list = HelpersOnGetIngredients.get_fillings_list(ingredients)
    TestGetUserOrders.sauces_list = HelpersOnGetIngredients.get_sauces_list(ingredients)
    HelpersOnCheck.check_ingredients(TestGetUserOrders.buns_list, TestGetUserOrders.fillings_list, TestGetUserOrders.sauces_list)


@pytest.mark.usefixtures('setup_ingredients', scope='class')
class TestGetUserOrders:

    buns_list = None
    fillings_list = None
    sauces_list = None


    @allure.step('Собираем бургер для заказа')
    def __create_burger(self):
        ingredients_list = [
            (self.buns_list[0])[KEYS.ID_KEY],
            (self.fillings_list[0])[KEYS.ID_KEY],
            (self.sauces_list[0])[KEYS.ID_KEY],
        ]
        return ingredients_list

    @allure.title('Проверка получения списка заказов для авторизованного пользователя - 1 заказ')
    def test_get_user_orders_list_authorized_user(self, setup_user):
        user_data, auth_token = setup_user
        ingredients_list = self.__create_burger()
        HelpersOnCreateUser.create_order(ingredients_list, auth_token)
        response =HelpersOnCreateUser.try_to_get_user_orders(auth_token)

        received_body = HelpersOnCheck.check_success_ok(response)
        HelpersOnCheck.check_received_orders_list(received_body, 1)


    # 2
    @allure.title('Проверка получения количества заказов "total" для авторизованного пользователя - 1 заказ')
    def test_get_user_orders_total_authorized_user(self, setup_user):
        user_data, auth_token = setup_user
        ingredients_list = self.__create_burger()
        HelpersOnCreateUser.create_order(ingredients_list, auth_token)
        response = HelpersOnCreateUser.try_to_get_user_orders(auth_token)
        received_body = HelpersOnCheck.check_success_ok(response)
        HelpersOnCheck.check_received_orders_total(received_body, 1)


    # 3
    @allure.title('Проверка получения количества заказов "total_today" для авторизованного пользователя - 1 заказ')
    def test_get_user_orders_total_today_authorized_user(self, setup_user):
        user_data, auth_token = setup_user
        ingredients_list = self.__create_burger()
        HelpersOnCreateUser.create_order(ingredients_list, auth_token)
        response = HelpersOnCreateUser.try_to_get_user_orders(auth_token)

        received_body = HelpersOnCheck.check_success_ok(response)
        HelpersOnCheck.check_received_orders_total_today(received_body, 1)


    @allure.title('Проверка получения списка заказов для авторизованного пользователя - нет заказов')
    def test_get_user_orders_list_authorized_user_no_orders(self, setup_user):
        user_data, auth_token = setup_user
        response = HelpersOnCreateUser.try_to_get_user_orders(auth_token)


        received_body = HelpersOnCheck.check_success_ok(response)
        HelpersOnCheck.check_received_orders_list(received_body, 0)


    # 2
    @allure.title('Проверка получения количества заказов "total" для авторизованного пользователя - нет заказов')
    def test_get_user_orders_total_authorized_user_no_orders(self, setup_user):
        response = HelpersOnCreateUser.try_to_get_user_orders(auth_token)
        received_body = HelpersOnCheck.check_success_ok(response)
        HelpersOnCheck.check_received_orders_total(received_body, 0)


    # 3
    @allure.title('Проверка получения количества заказов "total_today" для авторизованного пользователя - нет заказов')
    def test_get_user_orders_total_today_authorized_user_no_orders(self, setup_user):
        user_data, auth_token = setup_user
        response = HelpersOnCreateUser.try_to_get_user_orders(auth_token)


        received_body = HelpersOnCheck.check_success_ok(response)
        HelpersOnCheck.check_received_orders_total_today(received_body, 0)


    @allure.title('Проверка получения заказов для неавторизованного пользователя - сообщение об ошибке')
    def test_get_user_orders_unauthorized_user_error(self):
        response = HelpersOnCreateUser.try_to_get_user_orders()

        HelpersOnCheck.check_not_success_error_message(response, CODE.UNAUTHORIZED, message.UNAUTHORIZED)
