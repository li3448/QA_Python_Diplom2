class Endpoints:                        # as e
    # URL-адрес сервера
    SERVER_URL = 'https://stellarburgers.nomoreparties.site'
    # Эндпойнты (ручки) запросов к API
    CREATE_USER = '/api/auth/register'
    LOGIN_USER = '/api/auth/login'
    LOGOUT_USER = '/api/auth/logout'
    DELETE_USER = '/api/auth/user'

    GET_USER_DATA = '/api/auth/user'
    UPDATE_USER = '/api/auth/user'
    GET_INGREDIENTS = '/api/ingredients'

    CREATE_ORDER = '/api/orders'

    GET_USER_ORDERS = '/api/orders'

    RESET_PASSWORD = '/api/password-reset/reset'

    UPDATE_TOKEN = '/api/auth/token'

    ACCESS_TOKEN_PREFIX = 'Bearer '


class StatusCodes:
    OK              = 200
    CREATED         = 201
    ACCEPTED        = 202
    BAD_REQUEST     = 400
    UNAUTHORIZED    = 401
    FORBIDDEN       = 403
    NOT_FOUND       = 404
    CONFLICT        = 409
    ERROR_500       = 500


class ResponseKeys:
    SUCCESS_KEY     = 'success'
    USER_KEY        = 'user'
    EMAIL_KEY       = 'email'
    NAME_KEY        = 'name'
    ACCESS_TOKEN    = 'accessToken'
    REFRESH_TOKEN   = 'refreshToken'
    MESSAGE_KEY     = 'message'
    DATA            = 'data'
    INGREDIENTS     = 'ingredients'
    ID_KEY          = '_id'
    TYPE_KEY        = 'type'
    TYPE_BUN        = 'bun'
    TYPE_MAIN       = 'main'
    TYPE_SAUCE      = 'sauce'

    ORDER_KEY       = 'order'
    NUMBER_KEY      = 'number'
    ORDERS_KEY      = 'orders'
    TOTAL_KEY       = 'total'
    TOTAL_TODAY_KEY = 'totalToday'

    # поля для отправки запроса
    AUTH_TOKEN_KEY  = 'Authorization'
    PASSWORD_KEY    = 'password'
    TOKEN_KEY       = 'token'


class ResponseMessages:

    LOGOUT                  = 'Successful logout'
    USER_DELETED            = 'User successfully removed'
    PASSWORD_IS_RESET       = 'Password successfully reset'

    USER_ALREADY_EXISTS     = 'User already exists'
    MISSING_REQUIRED_FIELD  = 'Email, password and name are required fields'
    INVALID_LOGIN           = 'email or password are incorrect'
    UNAUTHORIZED            = 'You should be authorised'
    EMAIL_ALREADY_EXISTS    = 'User with such email already exists'
    NO_INGREDIENTS          = 'Ingredient ids must be provided'

