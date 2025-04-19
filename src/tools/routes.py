"""
Created on 2025-04-17

 * APIRoutes — перечисление всех возможных эндпоинтов, с которыми будет работать приложение.
 Это позволяет централизовать и стандартизировать использование адресов.
 * В реальных проектах вам возможно придется добавлять новые маршруты, и это будет намного удобнее,
 если они будут прописаны в одном месте.
"""

from enum import Enum


class APIRoutes(str, Enum):
    """
    Перечисление всех URI-адресов API для проекта.

    Это перечисление позволяет централизованно управлять всеми маршрутами API,
    что помогает избежать ошибок при их использовании и упрощает масштабирование.
    """
    CARDS = "/fakebank/cards"
    CLIENTS = "/fakebank/clients"
    OPERATIONS = "/fakebank/accounts"  # Основной URI для работы с операциями
    STATEMENTS = "/fakebank/statements"
    NOTIFICATIONS = "/fakebank/notifications"

    def __str__(self):
        return self.value
