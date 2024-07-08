import pytest
import allure
from data import StatusCodes as CODE
from data import ResponseKeys as KEYS
from data import ResponseMessages as message
from helpers import HelpersOnCheck
from helpers import HelpersOnCreateUser



@pytest.mark.usefixtures('setup_ingredients', scope='class')
class TestCreateOrder:

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


    @allure.title('Проверка создания заказа для авторизованного пользователя')
    def test_create_order_authorized_user(self, setup_user):

        user_data, auth_token = setup_user
        ingredients_id_list = self.__create_burger()
        response = HelpersOnCreateUser.try_to_create_order(ingredients_id_list, auth_token)
        HelpersOnCheck.check_order_data(response)


    @allure.title('Проверка создания заказа для авторизованного пользователя')
    def test_create_order_two_orders_for_authorized_user(self, setup_user):
        user_data, auth_token = setup_user
        ingredients_id_list = self.__create_burger()
        response = HelpersOnCreateUser.try_to_create_order(ingredients_id_list, auth_token)
        HelpersOnCheck.check_order_data(response)
        response = HelpersOnCreateUser.try_to_create_order(ingredients_id_list, auth_token)
        HelpersOnCheck.check_order_data(response)


    @allure.title('Проверка создания заказа без авторизации')
    def test_create_order_unauthorized(self):
        ingredients_id_list = self.__create_burger()
        response = HelpersOnCreateUser.try_to_create_order(ingredients_id_list)
        HelpersOnCheck.check_order_data(response)


    @allure.title('Проверка создания заказа без ингредиентов')
    def test_create_order_no_ingredients(self):
        ingredients_id_list = []
        response = HelpersOnCreateUser.try_to_create_order(ingredients_id_list)
        HelpersOnCheck.check_not_success_error_message(response, CODE.BAD_REQUEST, message.NO_INGREDIENTS)


    @allure.title('Проверка создания заказа с неверным хешем ингредиента')
    def test_create_order_invalid_ingredient_hash(self):
        ingredients_id_list = ['0000000000']
        response = HelpersOnCreateUser.try_to_create_order(ingredients_id_list)
        HelpersOnCheck.check_status_code(response, CODE.ERROR_500)


