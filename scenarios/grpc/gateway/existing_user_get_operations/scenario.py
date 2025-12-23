from locust import task, events
from locust.env import Environment

from clients.grpc.gateway.locust import GatewayGRPCTaskSet
from seeds.scenarios.existing_user_get_operations import ExistingUserGetOperationsSeedsScenario
from seeds.schema.result import SeedUserResult
from tools.locust.user import LocustBaseUser


# Хук инициализации — вызывается перед началом запуска нагрузки
@events.init.add_listener
def init(environment: Environment, **kwargs):
    # Выполняем сидинг
    seeds_scenario = ExistingUserGetOperationsSeedsScenario()
    seeds_scenario.build()  # создаём пользователей, счета, карты и операции

    # Загружаем результат сидинга (из файла JSON)
    environment.seeds = seeds_scenario.load()


# TaskSet — сценарий пользователя. Каждый виртуальный пользователь выполняет эти задачи
class GetOperationsTaskSet(GatewayGRPCTaskSet):
    seed_user: SeedUserResult  # Типизированная ссылка на данные из сидинга

    def on_start(self) -> None:
        super().on_start()
        # Получаем случайного пользователя из подготовленного списка
        self.seed_user = self.user.environment.seeds.get_random_user()


    @task(3)
    def get_accounts(self):
        # Получение списка счетов
        self.accounts_gateway_client.get_accounts(user_id=self.seed_user.user_id)

    @task(5)
    def get_operations(self):
        # Получаем список операций по счёту
        self.operations_gateway_client.get_operations(
            account_id=self.seed_user.credit_card_accounts[0].account_id
        )

    @task(2)
    def get_operations_summary(self):
        # Получаем статистику по операциям пользователя
        self.operations_gateway_client.get_operations_summary(
            account_id=self.seed_user.credit_card_accounts[0].account_id
        )


# Пользовательский класс, который будет запускать наш TaskSet
class GetOperationsScenarioUser(LocustBaseUser):
    tasks = [GetOperationsTaskSet]