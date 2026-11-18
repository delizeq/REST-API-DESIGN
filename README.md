
# Esports Watch API

Django REST API для перегляду та керування кіберспортивними іграми, командами, турнірами та матчами CS2 і Dota 2.

## Технології

- Python
- Django
- Django REST Framework
- SQLite
- JWT (Simple JWT)
- drf-spectacular (Swagger / OpenAPI)
- coverage.py
- python-decouple
- Python logging
- Postman Collection v2.1

## Основні можливості

- CRUD-операції для ігор, команд, турнірів і матчів.
- Перегляд пов'язаних турнірів і матчів.
- Фільтрація, пошук і сортування даних.
- Реєстрація та авторизація користувачів через JWT.
- Розмежування доступу для авторизованих і неавторизованих користувачів.
- JSON-відповіді та обробка помилок.
- Валідація даних.
- Автоматичне тестування API.
- Генерація документації Swagger / OpenAPI.
- Логування операцій та помилок.
- Зберігання секретних налаштувань у `.env`.
- CORS для взаємодії з окремим frontend.

## Встановлення та запуск

Клонуйте репозиторій і перейдіть у папку проєкту.

Створіть віртуальне середовище:

```bash
python -m venv venv
```

Активуйте його у Windows Git Bash:

```bash
source venv/Scripts/activate
```

Встановіть залежності:

```bash
python -m pip install -r requirements.txt
```

### Налаштування .env

Створіть у кореневій папці проєкту файл `.env` за зразком `.env.example`.

Приклад:

```env
SECRET_KEY=your-generated-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

Для генерації власного секретного ключа виконайте:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Вставте згенерований ключ у локальний `.env`.

Файл `.env` не додається до Git, оскільки містить секретні налаштування.

### Запуск Django

Застосуйте міграції:

```bash
python manage.py migrate
```

Запустіть сервер:

```bash
python manage.py runserver
```

API буде доступне за адресою:

http://127.0.0.1:8000/

## API endpoints

Усі дані передаються у форматі JSON.

### Games

- `GET /games/` — список ігор.
- `POST /games/` — створення гри.
- `GET /games/{id}/` — отримання гри.
- `PUT /games/{id}/` — повне оновлення гри.
- `PATCH /games/{id}/` — часткове оновлення гри.
- `DELETE /games/{id}/` — видалення гри.
- `GET /games/{id}/tournaments/` — турніри гри.

### Teams

- `GET /teams/` — список команд.
- `POST /teams/` — створення команди.
- `GET /teams/{id}/` — отримання команди.
- `PUT /teams/{id}/` — повне оновлення команди.
- `PATCH /teams/{id}/` — часткове оновлення команди.
- `DELETE /teams/{id}/` — видалення команди.
- `GET /teams/{id}/matches/` — матчі команди.

### Tournaments

- `GET /tournaments/` — список турнірів.
- `POST /tournaments/` — створення турніру.
- `GET /tournaments/{id}/` — отримання турніру.
- `PUT /tournaments/{id}/` — повне оновлення турніру.
- `PATCH /tournaments/{id}/` — часткове оновлення турніру.
- `DELETE /tournaments/{id}/` — видалення турніру.
- `GET /tournaments/{id}/matches/` — матчі турніру.

### Matches

- `GET /matches/` — список матчів.
- `POST /matches/` — створення матчу.
- `GET /matches/{id}/` — отримання матчу.
- `PUT /matches/{id}/` — повне оновлення матчу.
- `PATCH /matches/{id}/` — часткове оновлення матчу.
- `DELETE /matches/{id}/` — видалення матчу.

Списки підтримують доступні в реалізації фільтри, пошук і сортування.

## Реєстрація та авторизація (JWT)

Для авторизації використовується `djangorestframework-simplejwt`.

### Реєстрація

`POST /auth/register/`

Приклад JSON:

```json
{
  "username": "exampleuser",
  "email": "example@example.com",
  "password": "StrongPass123!",
  "password_confirmation": "StrongPass123!"
}
```

- `201 Created` — користувача створено.
- `400 Bad Request` — помилка валідації.

Паролі зберігаються у вигляді хешу.

### Вхід

`POST /auth/login/`

```json
{
  "username": "exampleuser",
  "password": "StrongPass123!"
}
```

- `200 OK` — повертає access і refresh токени.
- `401 Unauthorized` — неправильні дані входу.

### Оновлення токена

`POST /auth/token/refresh/`

```json
{
  "refresh": "YOUR_REFRESH_TOKEN"
}
```

- `200 OK` — повертає новий access токен.
- `401 Unauthorized` — недійсний refresh токен.

### Профіль користувача

`GET /auth/me/`

Заголовок:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

- `200 OK` — інформація про користувача.
- `401 Unauthorized` — немає авторизації.

### Права доступу

GET-запити до ігор, команд, турнірів і матчів доступні всім користувачам.

POST, PUT, PATCH та DELETE для цих ресурсів доступні тільки авторизованим користувачам.

Для захищених запитів використовується заголовок:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Вихід із системи

Вихід реалізовано на frontend шляхом видалення збережених access і refresh токенів.

Окремого backend endpoint для виходу немає.

## Swagger / OpenAPI

Документація API генерується автоматично за допомогою `drf-spectacular`.

Після запуску Django-сервера доступні:

**Swagger UI:**

http://127.0.0.1:8000/api/docs/

**OpenAPI schema:**

http://127.0.0.1:8000/api/schema/

Swagger UI дозволяє переглядати:

- Доступні API endpoints.
- HTTP-методи.
- Параметри запитів.
- Структуру JSON-запитів і відповідей.
- Коди відповідей.
- Налаштування авторизації.

Для перевірки захищених запитів необхідно отримати JWT access token через `/auth/login/` та використати кнопку Authorize у Swagger UI.

Для збереження OpenAPI-схеми у файл можна виконати:

```bash
python manage.py spectacular --file schema.yml
```

## Автоматичне тестування

Для тестування використовується Django REST Framework `APITestCase`.

Запуск тестів:

```bash
python manage.py test
```

Реалізовано 17 автоматичних тестів.

Тести перевіряють:

- GET, POST, PUT, PATCH і DELETE.
- Авторизовані та неавторизовані запити.
- Успішне створення, оновлення та видалення ресурсів.
- Валідацію некоректних даних.
- Пошук і фільтрацію.
- Обробку помилок 400, 401, 404 та 409.
- Заборону видалення об'єктів із пов'язаними записами.

Для підготовки тестових даних використовується метод `setUp()`.

## Покриття тестами (Coverage)

Для вимірювання покриття використовується бібліотека `coverage`.

Запуск тестів із вимірюванням покриття:

```bash
coverage run --source=accounts,esports manage.py test
```

Перегляд звіту:

```bash
coverage report -m
```

Створення HTML-звіту:

```bash
coverage html
```

HTML-звіт створюється в папці `htmlcov/`.

Папка `htmlcov/` та файл `.coverage` не додаються до Git.

Актуальний відсоток покриття вказується в описі Pull Request після фінального запуску тестів.

## Логування API

Для логування використовується стандартний модуль Python `logging`.

Налаштування знаходяться в `config/settings.py`, а логування операцій з ресурсами реалізоване в `esports/views.py`.

Використовуються такі рівні:

- `DEBUG` — діагностичні повідомлення.
- `INFO` — успішне створення, оновлення та видалення об'єктів.
- `WARNING` — помилки валідації та заблоковані операції.
- `ERROR` — серверні помилки, для яких налаштовано логер Django.

Приклад повідомлень:

```text
[INFO] esports.views: Created Game with id=2
[INFO] esports.views: Updated Game id=1 using PATCH
[WARNING] esports.views: Invalid create request for Match
[WARNING] esports.views: Deletion blocked for Game id=1
```

Логи виводяться в консоль із зазначенням часу, рівня та назви модуля.

Паролі, JWT-токени та секретні ключі не записуються в додані повідомлення логування.

## Коди відповідей

- `200 OK` — успішне отримання або оновлення.
- `201 Created` — ресурс створено.
- `204 No Content` — ресурс видалено.
- `400 Bad Request` — некоректні дані.
- `401 Unauthorized` — необхідна авторизація.
- `404 Not Found` — ресурс не знайдено.
- `409 Conflict` — конфлікт даних, визначений логікою API.

## Postman

Колекція Postman Collection v2.1 знаходиться у файлі:

`postman/esports_watch_api.postman_collection.json`

Імпортуйте цей файл у Postman.

Базова адреса API:

http://127.0.0.1:8000/

## Frontend

Frontend знаходиться в окремому репозиторії:

https://github.com/delizeq/esports-watch-frontend

Frontend запускається на порту `5500`, а Django API — на порту `8000`.
