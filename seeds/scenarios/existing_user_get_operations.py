from seeds.scenario import SeedsScenario
from seeds.schema.plan import SeedsPlan, SeedUsersPlan, SeedAccountsPlan, SeedOperationsPlan


class ExistingUserGetOperationsSeedsScenario(SeedsScenario):
    """
    Сценарий сидинга для существующего пользователя, который открывает для каждого пользователя
    кредитный счёт, а затем выполнять для каждого пользователя следующее:
    5 операций покупки.
    1 операция пополнения счёта.
    1 операция снятия наличных.
    """

    @property
    def plan(self) -> SeedsPlan:
        """
        План сидинга, который описывает, сколько пользователей нужно создать
        и какие именно данные для них генерировать.
        В данном случае создаём 300 пользователей, каждому даём кредитный счёт и операции по счету.
        """
        return SeedsPlan(
            users=SeedUsersPlan(
                count=300,  # Количество пользователей
                credit_card_accounts=SeedAccountsPlan(
                    count=1,  # Количество счётов на пользователя
                    purchase_operations=SeedOperationsPlan(count=5),  # Количество операций покупки
                    top_up_operations=SeedOperationsPlan(count=1),  # Количество операций пополнения
                    cash_withdrawal_operations=SeedOperationsPlan(count=1),  # Количество операций снятия
                )
            ),
        )

    @property
    def scenario(self) -> str:
        """
        Название сценария сидинга, которое будет использоваться для сохранения данных.
        """
        return "existing_user_get_operations"


if __name__ == '__main__':
    # Если файл запускается напрямую, создаём объект сценария и запускаем его.
    seeds_scenario = ExistingUserGetOperationsSeedsScenario()
    seeds_scenario.build()  # Стартуем процесс сидинга
