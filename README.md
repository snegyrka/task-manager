\# Task Manager API



REST-сервис для управления проектами и задачами на FastAPI.



\## Функциональность

\- JWT-аутентификация (регистрация, вход)

\- CRUD операции для проектов и задач

\- Анализ загрузки исполнителей

\- Алгоритм подбора оптимального исполнителя

\- Email-уведомления и отслеживание дедлайнов

\- 10 автоматических тестов



\## Технологии

\- FastAPI, SQLAlchemy, SQLite

\- JWT (python-jose), Pydantic, Pytest



\## Запуск



1\. Клонировать репозиторий:

git clone https://github.com/snegyrka/task-manager.git

cd task-manager



2\. Создать виртуальное окружение:

python -m venv venv

venv\\Scripts\\activate



3\. Установить зависимости:

pip install -r requirements.txt



4\. Запустить сервер:

uvicorn app.main:app --reload



5\. Открыть http://localhost:8000/docs



\## Запуск тестов

pytest tests/test\_main.py -v



\## Оценка pylint

7.60/10



\## Автор

snegyrka

