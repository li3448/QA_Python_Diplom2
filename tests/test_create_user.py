import pytest
import allure

from data import StatusCodes as CODE
from data import ResponseKeys as KEYS
from data import ResponseMessages as message
from helpers import HelpersOnCheck
from helpers import HelpersOnCreateUser



@pytest.fixture
@allure.title('Инициализируем данные пользователя для удаления после завершения работы')
def setup_user():
    # Инициализируем данные пользователя для удаления после завершения работы
    TestCreateUser.to_teardown = False
    TestCreateUser.auth_token = None

    yield
    # Удаляем созданного пользователя
    if TestCreateUser.to_teardown:
        HelpersOnCreateUser.try_to_delete_user(TestCreateUser.auth_token)



class TestCreateUser:
  
    to_teardown = False  # Выполнять удаление созданного пользователя
    auth_token = None

    @allure.title('Сохраняем полученные данные пользователя для удаления после завершения работы')
    def __init_teardown(self, auth_token):
        TestCreateUser.to_teardown = True
        TestCreateUser.auth_token = auth_token


    @allure.title('Проверка создания пользователя - регистрация уникального пользователя')

    def test_create_user_new_user(self, create_user, generate_payload):
        user_data = HelpersOnCreateUser.generate_random_user_data()
        created_user = User.create_user(user_data)
        assert created_user.json()['success'] == True
        assert created_user.status_code == HTTPStatus.OK



    @allure.title('Можно создать уникального пользователя')
    def test_create_user_code_200(self, generating_the_user_and_delete_the_user):
        data_user = _payload(generating_the_user_and_delete_the_user)
        req_cr_user = User.create_user(data_user)
        assert req_cr_user.json()['success'] == True
        assert req_cr_user.status_code == HTTPStatus.OK

    def test_create_user_new_user(self, setup_user):
        user_data = HelpersOnCreateUser.generate_random_user_data()
        auth_token, refresh_token = HelpersOnCreateUser.create_and_check_user(user_data)
        self.__init_teardown(auth_token)


    @allure.title('Проверка создания пользователя - повторная регистрация пользователя')
    def test_create_user_double_user_error(self, setup_user):
        user_data = HelpersOnCreateUser.generate_random_user_data()
        auth_token, refresh_token = HelpersOnCreateUser.create_user(user_data)
        self.__init_teardown(auth_token)
        response = HelpersOnCreateUser.try_to_create_user(user_data)
        HelpersOnCheck.check_not_success_error_message(response, CODE.FORBIDDEN, message.USER_ALREADY_EXISTS)


    @allure.title('Проверка создания пользователя - не заполнено одно из полей')
    @pytest.mark.parametrize('field', [         # незаполненное поле
        KEYS.EMAIL_KEY,
        KEYS.PASSWORD_KEY,
        KEYS.NAME_KEY
    ])
    def test_create_user_empty_field_error(self, field):
        user_data = HelpersOnCreateUser.generate_random_user_data()
        user_data.pop(field)
        response = HelpersOnCreateUser.try_to_create_user(user_data)

        HelpersOnCheck.check_not_success_error_message(response, CODE.FORBIDDEN, message.MISSING_REQUIRED_FIELD)

