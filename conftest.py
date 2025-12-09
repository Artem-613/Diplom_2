import allure
import pytest

from helpers.helpers_check_response import HelpersOnCheck as c
from helpers.helpers_create_user import HelpersOnCreateUser as u
from helpers.helpers_get_ingredients import HelpersOnGetIngredients as g 


@pytest.fixture
@allure.title('Создаём пользователя и инициализируем данные для удаления после завершения работы')
def setup_user():
    # генерируем данные нового пользователя: email, password, user_name
    user_data = u.generate_random_user_data()
    # отправляем запрос на создание пользователя
    auth_token, refresh_token = u.create_user(user_data)
    # сохраняем полученные данные пользователя
    yield user_data, auth_token

    # Удаляем созданного пользователя
    u.try_to_delete_user(auth_token)


@pytest.fixture(scope='class')
@allure.title('Инициализируем списки ингредиентов')
def setup_ingredients():
    ingredients = g.get_ingredients()
    buns_list = g.get_buns_list(ingredients)
    fillings_list = g.get_fillings_list(ingredients)
    sauces_list = g.get_sauces_list(ingredients)
    c.check_ingredients(buns_list, fillings_list, sauces_list)
    
    # Возвращаем как словарь
    return {
        'buns_list': buns_list,
        'fillings_list': fillings_list,
        'sauces_list': sauces_list
    }


@pytest.fixture
@allure.title('Инициализируем данные пользователя для удаления после завершения работы')
def setup_user_teardown():
    # Инициализируем данные пользователя для удаления после завершения работы
    to_teardown = False
    auth_token = None

    yield to_teardown, auth_token
    
    # Удаляем созданного пользователя
    if to_teardown:
        u.try_to_delete_user(auth_token)