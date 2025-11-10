from locust import User, between, task

from clients.http.gateway.users.client import UsersGatewayHTTPClient, build_users_gateway_locust_http_client
from clients.http.gateway.users.schema import CreateUserResponseSchema
from clients.http.gateway.accounts.client import AccountsGatewayHTTPClient, build_accounts_gateway_locust_http_client


class OpenDebitCardAccountScenarioUser(User):
    # Обязательное поле, требуемое Locust. Будет проигнорировано, но его нужно указать, иначе будет ошибка запуска.
    host = "localhost"
    # Пауза между запросами для каждого виртуального пользователя (в секундах)
    wait_time = between(1, 3)

    def on_start(self) -> None:
        """
        Метод on_start вызывается один раз при запуске каждой сессии виртуального пользователя.
        Здесь мы создаем нового пользователя, отправляя POST-запрос к /api/v1/users.
        """
        # Инициализация клиентов
        users_gateway_client: UsersGatewayHTTPClient
        accounts_gateway_client: AccountsGatewayHTTPClient
        # Поле, куда мы сохраним ответ после создания пользователя
        create_user_response: CreateUserResponseSchema
        # создаем API клиент для пользователя
        self.users_gateway_client = build_users_gateway_locust_http_client(self.environment)
        # Создаём клиент для счётов
        self.accounts_gateway_client = build_accounts_gateway_locust_http_client(self.environment)
        # создаем пользователя через API, записываем в переменную
        self.create_user_response = self.users_gateway_client.create_user()

    @task
    def open_debit_card_account(self):
        """
        Основная нагрузочная задача: открытиe дебетового счёта.
        """
        # открываем дебетовую карту с id созданного пользователя
        self.accounts_gateway_client.open_debit_card_account(self.create_user_response.user.id)
