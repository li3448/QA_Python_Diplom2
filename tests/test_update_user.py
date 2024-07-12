import pytest
import allure

from data import StatusCodes as CODE
from data import ResponseKeys as KEYS
from data import ResponseMessages as message

from helpers import HelpersOnCheck
from helpers import HelpersOnCreateUser


class TestUpdateUser:

    @allure.title('Проверка обновления данных пользователя для авторизованного пользователя')
    @pytest.mark.parametrize('field', [         # обновляемое поле
        KEYS.EMAIL_KEY,
        KEYS.NAME_KEY,
        KEYS.PASSWORD_KEY,
    ])
    def test_update_user_success(self, setup_user, field):
        user_data, auth_token = setup_user
        new_user_data = HelpersOnCreateUser.generate_random_user_data()
        update_data = user_data.copy()
        update_data[field] = new_user_data[field]
        payload = {
            field: update_data[field]
        }
        response = HelpersOnCreateUser.try_to_update_user(payload, auth_token)

        received_body = HelpersOnCheck.check_success_ok(response)
        HelpersOnCheck.check_user_data(received_body, update_data)


    @allure.title('Проверка обновления данных пользователя для неавторизованного пользователя')
    @pytest.mark.parametrize('field', [         # обновляемое поле
        KEYS.EMAIL_KEY,
        KEYS.NAME_KEY,
        KEYS.PASSWORD_KEY,
    ])
    def test_update_user_not_authorized_error(self, setup_user, field):
        user_data, auth_token = setup_user
        new_user_data = HelpersOnCreateUser.generate_random_user_data()
        update_data = user_data.copy()
        update_data[field] = new_user_data[field]
        payload = {
            field: update_data[field]
        }
        response = HelpersOnCreateUser.try_to_update_user(payload)

        HelpersOnCheck.check_not_success_error_message(response, CODE.UNAUTHORIZED, message.UNAUTHORIZED)

