"""
Created on 2025-04-17

Базовый API клиент, который будет использоваться для выполнения стандартных HTTP-запросов.
В качестве HTTP-клиента будем использовать httpx.Client.

 * BaseClient — класс, который инкапсулирует базовые HTTP-методы (GET, POST, PATCH, DELETE) для взаимодействия с API.
 Для каждого метода добавлен декоратор allure.step, который позволяет отслеживать шаги выполнения тестов в отчете.

 * get_http_client — функция для создания экземпляра httpx.Client с необходимыми настройками (например, URL и таймаут),
 переданными через конфигурацию.

Важно! Чтобы избежать ошибок и дублирования адресов эндпоинтов в проекте,
рекомендуется вынести все URI в отдельный Enum.
Это позволит централизованно управлять URL-адресами и избежать опечаток.
"""

from typing import Any

import allure
from httpx import Client, URL, Response, QueryParams
from httpx._types import RequestData, RequestFiles

from config import HTTPClientConfig


class BaseClient:
    """
    Базовый клиент для выполнения HTTP-запросов.

    Этот класс предоставляет основные методы для выполнения HTTP-запросов
    (GET, POST, PATCH, DELETE) и использует httpx.Client для выполнения
    запросов. Каждый метод добавлен с использованием allure для генерации
    отчетов о тестах.
    """

    def __init__(self, client: Client):
        """
        Инициализация клиента.
        :param client: Экземпляр httpx.Client
        """
        self.client = client

    @allure.step("Make GET request to {url}")
    def get(
            self,
            url: URL | str,
            params: QueryParams | None = None) -> Response:
        """
        Выполняет GET-запрос.

        :param url: URL эндпоинта
        :param params: Query параметры запроса
        :return: HTTP-ответ
        """
        return self.client.get(url, params=params)

    @allure.step("Make POST request to {url}")
    def post(
            self,
            url: URL | str,
            json: Any | None = None,
            data: RequestData | None = None,
            files: RequestFiles | None = None) -> Response:
        """
        Выполняет POST-запрос.

        :param url: URL эндпоинта
        :param json: JSON тело запроса
        :param data: Данные формы
        :param files: Файлы для загрузки
        :return: HTTP-ответ
        """
        return self.client.post(url, json=json, data=data, files=files)

    @allure.step("Make PATCH request to {url}")
    def patch(
            self,
            url: URL | str,
            json: Any | None = None) -> Response:
        """
        Выполняет PATCH-запрос.

        :param url: URL эндпоинта
        :param json: JSON тело запроса
        :return: HTTP-ответ
        """
        return self.client.patch(url, json=json)

    @allure.step("Make DELETE request to {url}")
    def delete(
            self,
            url: URL | str) -> Response:
        """
        Выполняет DELETE-запрос.

        :param url: URL эндпоинта
        :return: HTTP-ответ
        """
        return self.client.delete(url)


def get_http_client(config: HTTPClientConfig) -> Client:
    """
    Функция для инициализации HTTP-клиента.

    :param config: Конфигурация HTTP-клиента
    :return: Экземпляр httpx.Client
    """
    return Client(
        timeout=config.timeout,  # Устанавливаем таймаут для всех запросов
        base_url=config.client_url,  # Базовый URL для API
    )
