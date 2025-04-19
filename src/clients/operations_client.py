"""
Created on 2025-04-19

 * OperationsClient — класс, который наследует от BaseClient и предоставляет методы для работы с операциями (получение списка операций, создание, обновление, удаление операции).
 * Каждый метод аннотирован с помощью @allure.step, что позволяет добавлять шаги в отчет Allure. Это помогает отслеживать выполнение шагов и параметров запросов в тестах.
 * Для сериализации объектов в JSON используется метод model_dump, который поддерживает алиасы и может исключать поля с None значениями.
 * get_operations_client — функция для создания экземпляра OperationsClient. Она принимает настройки и использует их для создания HTTP-клиента с нужными параметрами.
 * get_http_client — этот метод создает экземпляр httpx.Client с настройками из конфигурации.

 Важно! Обратите внимание, что шаги для Allure были добавлены на двух уровнях: для BaseClient и OperationsClient.
 1. Шаги для BaseClient: На уровне BaseClient шаги содержат подробную техническую информацию о том, какой HTTP-метод использовался (например, GET, POST, PATCH, DELETE), куда был отправлен запрос, с каким телом и параметрами. Это позволяет нам точно видеть все детали запроса, которые были отправлены на сервер. Например, мы можем узнать:
    * Используемый HTTP-метод.
    * URL, по которому был отправлен запрос.
    * Тело запроса (если оно было).
2. Шаги для OperationsClient: На уровне OperationsClient шаги отражают описание выполняемых действий с точки зрения бизнес-логики. Здесь не отображаются технические детали (например, сам HTTP-запрос), а скорее бизнесовые действия, такие как "Получение списка операций", "Создание новой операции" и т.д. Это делает отчет Allure более понятным и ориентированным на бизнес-логику, не перегружая его техническими деталями.
В случае, если нужно получить более детальную информацию (например, какие параметры были переданы в запросе или какие методы использовались), можно раскрыть шаги с детальным описанием, где будут представлены все технические детали.
3. Декоратор @allure.step: Важно отметить, что мы используем декоратор @allure.step специально, чтобы в отчет автоматически прикреплялись все параметры, передаваемые в методы и функции. Это позволяет нам в отчете видеть не только, какие шаги были выполнены, но и какие данные были переданы в каждом запросе, обеспечивая полную прозрачность всех действий.
"""

import allure
from httpx import Response

from src.clients.base_client import BaseClient, get_http_client
from config import Settings
from src.schema.operations import CreateOperationSchema, UpdateOperationSchema, OperationSchema
from src.tools.routes import APIRoutes


class OperationsClient(BaseClient):
    """
    Получить список всех операций.

    :return: Ответ от сервера с информацией о всех операциях.
    """

    @allure.step("Get list of operations")
    def get_operations_api(self) -> Response:
        """
        Получить список всех операций.

        :return: Ответ от сервера с информацией о всех операциях.
        """
        return self.get(APIRoutes.OPERATIONS)

    @allure.step("Get operation by id {operation_id}")
    def get_operation_api(self, operation_id: int) -> Response:
        """
        Получить операцию по идентификатору.

        :param operation_id: Идентификатор операции.
        :return: Ответ от сервера с информацией об операции.
        """
        return self.get(f"{APIRoutes.OPERATIONS}/{operation_id}")

    @allure.step("Create operation")
    def create_operation_api(self, operation: CreateOperationSchema) -> Response:
        """
        Получить операцию по идентификатору.

        :param operation: Идентификатор операции.
        :return: Ответ от сервера с информацией об операции.
        """
        return self.post(
            APIRoutes.OPERATIONS,
            json=operation.model_dump(mode="json", by_alias=True)  # Сериализуем объект в JSON перед отправкой
        )

    @allure.step("Update operation by id {operation_id}")
    def update_operation_api(
            self,
            operation_id: int,
            operation: UpdateOperationSchema) -> Response:
        """
        Обновить операцию по идентификатору.

        :param operation_id: Идентификатор операции, которую нужно обновить.
        :param operation: Данные для обновления операции.
        :return: Ответ от сервера с обновленными данными операции.
        """
        return self.patch(
            f"{APIRoutes.OPERATIONS}/{operation_id}",
            json=operation.model_dump(mode='json', by_alias=True, exclude_none=True)
        )

    @allure.step("Delete operation by id {operation_id}")
    def delete_operation_api(self, operation_id: int) -> Response:
        """
        Удалить операцию по идентификатору.

        :param operation_id: Идентификатор операции, которую нужно удалить.
        :return: Ответ от сервера с результатом удаления операции.
        """
        return self.delete(f"{APIRoutes.OPERATIONS}/{operation_id}")

    def create_operation(self) -> OperationSchema:
        """
        Упрощенный метод для создания новой операции.

        Этот метод создает операцию с помощью схемы `CreateOperationSchema`, отправляет запрос
        на создание, а затем преобразует ответ в объект `OperationSchema`.

        :return: Объект `OperationSchema`, представляющий созданную операцию.
        """
        # Создаем запрос с фейковыми данными (по умолчанию для теста)
        request = CreateOperationSchema()
        # Отправляем запрос на создание
        response = self.create_operation_api(request)
        # Возвращаем созданную операцию как объект схемы
        return OperationSchema.model_validate_json(response.text)


def get_operations_client(settings: Settings) -> OperationsClient:
    """
    Функция для создания экземпляра OperationsClient с нужными настройками.

    :param settings: Конфигурация с настройками для работы с API.
    :return: Экземпляр клиента для работы с операциями.
    """
    return OperationsClient(client=get_http_client(settings.fake_bank_http_client))
