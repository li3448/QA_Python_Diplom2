import pytest
import allure

from data import StatusCodes as CODE
from data import ResponseKeys as KEYS
from data import ResponseMessages as message
from helpers import HelpersOnCheck
from helpers import HelpersOnCreateUser


class TestLoginUser:

    @allure.title('Проверка авторизации пользователя под существующим пользователем')
    def test_login_user_success(self, setup_user):
        user_data, auth_token = setup_user
        response = HelpersOnCreateUser.try_to_login_user(user_data[KEYS.EMAIL_KEY], user_data[KEYS.PASSWORD_KEY])
        HelpersOnCheck.check_status_code(response, CODE.OK)
        received_body = HelpersOnCheck.check_success(response, True)
        HelpersOnCheck.check_new_user_data(received_body, user_data)


    @allure.title('Проверка авторизации пользователя с неверным логином или паролем')
    @pytest.mark.parametrize('field', [         # неверное поле
        KEYS.PASSWORD_KEY,
        KEYS.EMAIL_KEY,
    ])
    def test_login_user_invalid_login_or_password_error(self, setup_user, field):
        user_data, auth_token = setup_user
        new_user_data = user_data.copy()
        new_user_data[field] = ""

        response = HelpersOnCreateUser.try_to_login_user(new_user_data[KEYS.EMAIL_KEY], new_user_data[KEYS.PASSWORD_KEY])
        HelpersOnCheck.check_not_success_error_message(response, CODE.UNAUTHORIZED, message.INVALID_LOGIN)


