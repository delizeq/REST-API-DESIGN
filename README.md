# Esports Watch API

Django REST API для перегляду та керування кіберспортивними іграми, командами, турнірами та матчами CS2 і Dota 2.

## Технології

- Python
- Django
- Django REST Framework
- SQLite
- Postman Collection v2.1

## Основні можливості

- CRUD-операції для ігор, команд, турнірів і матчів.
- Перегляд пов'язаних турнірів і матчів.
- Фільтрація, пошук і сортування даних.
- JSON-відповіді та обробка помилок.
- Валідація даних.
- CORS для взаємодії з окремим frontend.

## Встановлення та запуск

Перейдіть у папку бекенду.

Створіть і активуйте віртуальне середовище, якщо воно ще не створене:

```bash
python -m venv venv
```

Windows Git Bash:

```bash
source venv/Scripts/activate
```

Встановіть залежності:

```bash
pip install -r requirements.txt
```

Застосуйте міграції:

```bash
python manage.py migrate
```

Запустіть сервер:

```bash
python manage.py runserver
```

API буде доступне за адресою `http://127.0.0.1:8000/`.

## API endpoints

Усі дані передаються у форматі JSON.

### Games

- `GET /games/` — список ігор.
- `POST /games/` — створення гри.
- `GET /games/<id>/` — отримання гри.
- `PUT /games/<id>/` — повне оновлення гри.
- `PATCH /games/<id>/` — часткове оновлення гри.
- `DELETE /games/<id>/` — видалення гри.
- `GET /games/<id>/tournaments/` — турніри гри.

### Teams

- `GET /teams/` — список команд.
- `POST /teams/` — створення команди.
- `GET /teams/<id>/` — отримання команди.
- `PUT /teams/<id>/` — повне оновлення команди.
- `PATCH /teams/<id>/` — часткове оновлення команди.
- `DELETE /teams/<id>/` — видалення команди.
- `GET /teams/<id>/matches/` — матчі команди.

### Tournaments

- `GET /tournaments/` — список турнірів.
- `POST /tournaments/` — створення турніру.
- `GET /tournaments/<id>/` — отримання турніру.
- `PUT /tournaments/<id>/` — повне оновлення турніру.
- `PATCH /tournaments/<id>/` — часткове оновлення турніру.
- `DELETE /tournaments/<id>/` — видалення турніру.
- `GET /tournaments/<id>/matches/` — матчі турніру.

### Matches

- `GET /matches/` — список матчів.
- `POST /matches/` — створення матчу.
- `GET /matches/<id>/` — отримання матчу.
- `PUT /matches/<id>/` — повне оновлення матчу.
- `PATCH /matches/<id>/` — часткове оновлення матчу.
- `DELETE /matches/<id>/` — видалення матчу.

Списки підтримують доступні у реалізації фільтри, пошук і сортування.

## Коди відповідей

- `200 OK` — успішне отримання або оновлення.
- `201 Created` — ресурс створено.
- `204 No Content` — ресурс видалено.
- `400 Bad Request` — некоректні дані.
- `404 Not Found` — ресурс не знайдено.
- `409 Conflict` — конфлікт даних, якщо він визначений логікою API.

## Тестування

Запустіть автоматичні тести:

```bash
python manage.py test
```

## Postman

Колекція Postman Collection v2.1 знаходиться у файлі:

`postman/esports_watch_api.postman_collection.json`

Імпортуйте цей файл у Postman. Базова адреса API: `http://127.0.0.1:8000`.

## Frontend

Frontend знаходиться в окремому репозиторії:

https://github.com/delizeq/esports-watch-frontend

Frontend запускається на порту `5500`, а Django API — на порту `8000`.

## Ліцензія

Навчальний проєкт.