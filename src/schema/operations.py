"""
Created on 2025-04-17

Определим:
 * CreateOperationSchema – используется при создании новой операции.
 Включает поля для суммы списания (debit), суммы зачисления (credit), категории (category),
 описания (description) и даты (transaction_date).
 * UpdateOperationSchema – предназначена для PATCH-запросов, где можно передавать только изменяемые поля.
 Все параметры здесь опциональны, так как частичное обновление не требует передачи всех данных.
 * OperationSchema – расширенная версия CreateOperationSchema, добавляет поле id, которое присваивается сервером.
 Используется для представления операции в ответах API.
 * OperationsSchema – список операций. Наследуется от RootModel, что позволяет работать с массивами объектов в Pydantic.

Добавим фейковую генерацию прямо в модели Pydantic, используя параметр default_factory.
Это позволит автоматически заполнять поля случайными значениями при создании модели.
"""

from datetime import date

from pydantic import BaseModel, Field, RootModel, ConfigDict

from src.tools.fakers import fake


# Модель для создания новой операции
class CreateOperationSchema(BaseModel):
    """
    Модель для создания новой банковской операции.

    Поля:
    - debit (float | None): Сумма списания со счёта
    - credit (float | None): Сумма зачисления на счёт
    - category (str): Категория операции
    - description (str): Описание операции
    - transaction_date (date): Дата транзакции (передаётся в формате "transactionDate")
    """
    model_config = ConfigDict(populate_by_name=True)  # Позволяет использовать alias при сериализации/десериализации

    debit: float | None = Field(default_factory=fake.money)  # Генерация случайной суммы списания со счёта
    credit: float | None = Field(default_factory=fake.money)  # Генерация случайной суммы зачисления на счёт
    category: str = Field(default_factory=fake.category)  # Генерация случайной категории
    description: str = Field(default_factory=fake.sentence)  # Генерация случайного описания
    transaction_date: date = Field(alias="transactionDate", default_factory=fake.date)  # Генерация случайной даты


# Модель для обновления данных (используется для PATCH запросов)
class UpdateOperationSchema(BaseModel):
    """Модель для обновления банковской операции (используется в PATCH запросах).

    Все поля являются необязательными, так как можно обновлять только часть данных.

    Поля:
    - debit (float | None): Новая сумма списания
    - credit (float | None): Новая сумма зачисления
    - category (str | None): Новая категория
    - description (str | None): Новое описание
    - transaction_date (date | None): Новая дата транзакции (alias "transactionDate")
    """
    model_config = ConfigDict(populate_by_name=True)

    debit: float | None = Field(default_factory=fake.money)
    credit: float | None = Field(default_factory=fake.money)
    category: str | None = Field(default_factory=fake.category)
    description: str | None = Field(default_factory=fake.sentence)
    transaction_date: date | None = Field(alias="transactionDate", default_factory=fake.date)


# Расширенная модель с id, представляющая конечную структуру операции
class OperationSchema(CreateOperationSchema):
    """
    Модель банковской операции, содержащая ID.

    Наследуется от CreateOperationSchema и добавляет поле:
    - id (int): Уникальный идентификатор операции
    """
    id: int


# Контейнер для списка операций
class OperationsSchema(RootModel):
    """
    Контейнер для списка операций.

    Поле:
    - root (list[OperationSchema]): Список операций
    """
    root: list[OperationSchema]
