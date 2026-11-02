# Task Manager API

![Python](https://img.shields.io/badge/python-3.11-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?logo=sqlalchemy&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)
![Tests](https://img.shields.io/badge/tests-12%20passed-brightgreen)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

REST API для управления задачами: создание, чтение, обновление и удаление
(CRUD), автоматическая Swagger-документация, тесты и Docker-образ.

## Стек

- **Python 3.11**
- **FastAPI** — асинхронный веб-фреймворк + автогенерация OpenAPI
- **SQLAlchemy 2.0** — ORM, типизированные модели через `Mapped[...]`
- **SQLite** — лёгкая БД, не требующая отдельного сервера
- **Pydantic v2** — валидация входных данных и сериализация ответов
- **Pytest** — 12 тестов на все эндпоинты
- **Docker** — воспроизводимый запуск одной командой

## Эндпоинты

| Метод | Путь | Описание | Коды ответов |
|-------|------|----------|--------------|
| `GET` | `/health` | Проверка живости сервиса | 200 |
| `POST` | `/tasks` | Создать задачу | 201, 422 |
| `GET` | `/tasks?skip=0&limit=100` | Список задач с пагинацией | 200 |
| `GET` | `/tasks/{task_id}` | Получить задачу по id | 200, 404 |
| `PATCH` | `/tasks/{task_id}` | Частично обновить задачу | 200, 404, 422 |
| `DELETE` | `/tasks/{task_id}` | Удалить задачу | 204, 404 |

## Скриншоты

![Swagger UI](docs/swagger.png)

Swagger доступен по адресу `http://127.0.0.1:8000/docs` после запуска.

## Запуск локально

```powershell
# 1. Клонировать репозиторий
git clone https://github.com/<ваш-логин>/task-manager-api.git
cd task-manager-api

# 2. Создать виртуальное окружение
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Запустить сервер
uvicorn app.main:app --reload