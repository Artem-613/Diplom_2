import pytest
import allure

from data import StatusCodes as CODE
from data import ResponseKeys as KEYS
from data import ResponseMessages as message
from data import create_burger  # ← НОВЫЙ ИМПОРТ

from helpers.helpers_check_response import HelpersOnCheck as c
from helpers.helpers_create_user import HelpersOnCreateUser as u
from helpers.helpers_get_ingredients import HelpersOnGetIngredients as g


@pytest.mark.usefixtures('setup_ingredients')
class TestCreateOrder:

    @allure.step('Собираем бургер для заказа')
    def get_burger_ingredients(self, setup_ingredients):
        # Получаем ингредиенты из фикстуры
        buns_list = setup_ingredients['buns_list']
        fillings_list = setup_ingredients['fillings_list']
        sauces_list = setup_ingredients['sauces_list']
        
        # Используем функцию из data.py
        return create_burger(buns_list, fillings_list, sauces_list)


    @allure.title('Проверка создания заказа для авторизованного пользователя')
    def test_create_order_authorized_user(self, setup_user, setup_ingredients):
        # сохраняем авторизационный токен пользователя, полученный при регистрации
        user_data, auth_token = setup_user
        # составляем список ингредиентов для бургера
        ingredients_id_list = self.get_burger_ingredients(setup_ingredients)
        # отправляем запрос на создание заказа
        response = u.try_to_create_order(ingredients_id_list, auth_token)

        # проверяем полученный ответ и данные заказа
        c.check_order_data(response)


    @allure.title('Проверка создания заказа для авторизованного пользователя')
    def test_create_order_two_orders_for_authorized_user(self, setup_user, setup_ingredients):
        # сохраняем авторизационный токен пользователя, полученный при регистрации
        user_data, auth_token = setup_user
        # составляем список ингредиентов для бургера
        ingredients_id_list = self.get_burger_ingredients(setup_ingredients)
        # отправляем запрос на создание заказа
        response = u.try_to_create_order(ingredients_id_list, auth_token)
        # проверяем полученный ответ и данные заказа
        c.check_order_data(response)
        # отправляем запрос на создание еще одного заказа
        response = u.try_to_create_order(ingredients_id_list, auth_token)

        # проверяем полученный ответ и данные заказа
        c.check_order_data(response)


    @allure.title('Проверка создания заказа без авторизации')
    def test_create_order_unauthorized(self, setup_ingredients):
        # составляем список ингредиентов для бургера
        ingredients_id_list = self.get_burger_ingredients(setup_ingredients)
        # отправляем запрос на создание заказа
        response = u.try_to_create_order(ingredients_id_list)

        # проверяем полученный ответ и данные заказа
        c.check_order_data(response)


    @allure.title('Проверка создания заказа без ингредиентов')
    def test_create_order_no_ingredients(self):
        # составляем список ингредиентов для бургера
        ingredients_id_list = []
        # отправляем запрос на создание заказа
        response = u.try_to_create_order(ingredients_id_list)

        # проверяем что получен код ответа 400
        # проверяем в теле ответа: { "success" = False }
        # проверяем сообщение в теле ответа: { "message" = "You should be authorised" }
        c.check_not_success_error_message(response, CODE.BAD_REQUEST, message.NO_INGREDIENTS)


    @allure.title('Проверка создания заказа с неверным хешем ингредиента')
    def test_create_order_invalid_ingredient_hash(self):
        # составляем список ингредиентов для бургера
        ingredients_id_list = ['0000000000']
        # отправляем запрос на создание заказа
        response = u.try_to_create_order(ingredients_id_list)

        # проверяем что получен код ответа 500
        c.check_status_code(response, CODE.ERROR_500)