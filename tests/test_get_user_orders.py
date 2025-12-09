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
class TestGetUserOrders:

    @allure.step('Собираем бургер для заказа')
    def get_burger_ingredients(self, setup_ingredients):
        # Получаем ингредиенты из фикстуры
        buns_list = setup_ingredients['buns_list']
        fillings_list = setup_ingredients['fillings_list']
        sauces_list = setup_ingredients['sauces_list']
        
        # Используем функцию из data.py
        return create_burger(buns_list, fillings_list, sauces_list)


    # тесты получения списка заказов и полей "total" и "total_today" для авторизованного пользователя - 1 заказ
    # 1
    @allure.title('Проверка получения списка заказов для авторизованного пользователя - 1 заказ')
    def test_get_user_orders_list_authorized_user(self, setup_user, setup_ingredients):
        # сохраняем авторизационный токен пользователя, полученный при регистрации
        user_data, auth_token = setup_user
        # получаем список ингредиентов и составляем заказ
        ingredients_list = self.get_burger_ingredients(setup_ingredients)
        # отправляем запрос на создание заказа для пользователя
        u.create_order(ingredients_list, auth_token)
        # отправляем запрос на получение заказов пользователя
        response = u.try_to_get_user_orders(auth_token)

        # Проверяем, что получен статус-код 200 OK и в теле ответа "success" = True
        # и получаем тело ответа
        received_body = c.check_success_ok(response)
        # проверяем поле "orders" и количество заказов, получаем список заказов
        c.check_received_orders_list(received_body, 1)


    # 2
    @allure.title('Проверка получения количества заказов "total" для авторизованного пользователя - 1 заказ')
    def test_get_user_orders_total_authorized_user(self, setup_user, setup_ingredients):
        # сохраняем авторизационный токен пользователя, полученный при регистрации
        user_data, auth_token = setup_user
        # получаем список ингредиентов и составляем заказ
        ingredients_list = self.get_burger_ingredients(setup_ingredients)
        # отправляем запрос на создание заказа для пользователя
        u.create_order(ingredients_list, auth_token)
        # отправляем запрос на получение заказов пользователя
        response = u.try_to_get_user_orders(auth_token)

        # Проверяем, что получен статус-код 200 OK и в теле ответа "success" = True
        # и получаем тело ответа
        received_body = c.check_success_ok(response)
        # проверяем поля "total" и "totalToday" в теле ответа
        c.check_received_orders_total(received_body, 1)


    # 3
    @allure.title('Проверка получения количества заказов "total_today" для авторизованного пользователя - 1 заказ')
    def test_get_user_orders_total_today_authorized_user(self, setup_user, setup_ingredients):
        # сохраняем авторизационный токен пользователя, полученный при регистрации
        user_data, auth_token = setup_user
        # получаем список ингредиентов и составляем заказ
        ingredients_list = self.get_burger_ingredients(setup_ingredients)
        # отправляем запрос на создание заказа для пользователя
        u.create_order(ingredients_list, auth_token)
        # отправляем запрос на получение заказов пользователя
        response = u.try_to_get_user_orders(auth_token)

        # Проверяем, что получен статус-код 200 OK и в теле ответа "success" = True
        # и получаем тело ответа
        received_body = c.check_success_ok(response)
        # проверяем поля "total" и "totalToday" в теле ответа
        c.check_received_orders_total_today(received_body, 1)


    # тесты получения списка заказов для авторизованного пользователя - 0 заказов
    # 1
    @allure.title('Проверка получения списка заказов для авторизованного пользователя - нет заказов')
    def test_get_user_orders_list_authorized_user_no_orders(self, setup_user):
        # сохраняем авторизационный токен пользователя, полученный при регистрации
        user_data, auth_token = setup_user
        # получаем заказы пользователя
        response = u.try_to_get_user_orders(auth_token)

        # Проверяем, что получен статус-код 200 OK и в теле ответа "success" = True
        # и получаем тело ответа
        received_body = c.check_success_ok(response)
        # проверяем поле "orders" и количество заказов
        c.check_received_orders_list(received_body, 0)


    # 2
    @allure.title('Проверка получения количества заказов "total" для авторизованного пользователя - нет заказов')
    def test_get_user_orders_total_authorized_user_no_orders(self, setup_user):
        # сохраняем авторизационный токен пользователя, полученный при регистрации
        user_data, auth_token = setup_user
        # получаем заказы пользователя
        response = u.try_to_get_user_orders(auth_token)

        # Проверяем, что получен статус-код 200 OK и в теле ответа "success" = True
        # и получаем тело ответа
        received_body = c.check_success_ok(response)
        # проверяем поля "total" и "totalToday" в теле ответа
        c.check_received_orders_total(received_body, 0)


    # 3
    @allure.title('Проверка получения количества заказов "total_today" для авторизованного пользователя - нет заказов')
    def test_get_user_orders_total_today_authorized_user_no_orders(self, setup_user):
        # сохраняем авторизационный токен пользователя, полученный при регистрации
        user_data, auth_token = setup_user
        # получаем заказы пользователя
        response = u.try_to_get_user_orders(auth_token)

        # Проверяем, что получен статус-код 200 OK и в теле ответа "success" = True
        # и получаем тело ответа
        received_body = c.check_success_ok(response)
        # проверяем поля "total" и "totalToday" в теле ответа
        c.check_received_orders_total_today(received_body, 0)


    # тесты получения списка заказов и полей "total" и "total_today" для неавторизованного пользователя - сообщение об ошибке
    @allure.title('Проверка получения заказов для неавторизованного пользователя - сообщение об ошибке')
    def test_get_user_orders_unauthorized_user_error(self):
        # получаем заказы пользователя
        response = u.try_to_get_user_orders()

        # проверяем что получен код ответа 401
        # проверяем в теле ответа: { "success" = False }
        # проверяем сообщение в теле ответа: { "message" = "You should be authorised" }
        c.check_not_success_error_message(response, CODE.UNAUTHORIZED, message.UNAUTHORIZED)