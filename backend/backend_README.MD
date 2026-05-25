# Backend: Vibecore PC Configurator

## Стек технологий
- **Язык:** Python 3.13
- **Фреймворки:** FastAPI (Core/Business), Flask (Supporting/Admin)
- **База данных:** PostgreSQL с репликацией Master-Slave
- **Работа с БД:** psycopg2 (чистый SQL, без ORM)
- **Аутентификация:** JWT (python-jose) + bcrypt
- **Статика и шаблоны:** общая папка `frontend/`
- **Документация API:** Swagger UI (`/docs`)

## Архитектура
Проект состоит из двух микросервисов, взаимодействующих с общей базой данных:

1. **Core/Business сервис (FastAPI, порт 8000)**  
   Вся клиентская бизнес-логика: регистрация, вход, конфигуратор ПК, заказы, совместимость, гарантии, дашборд.

2. **Supporting сервис (Flask, порт 5000)**  
   Административная панель для управления сущностями (CRUD) с поиском, сортировкой и фильтрацией.

Оба сервиса используют Master для записи и Slave для чтения.

## Структура проекта (Backend)
backend/
├── main.py # FastAPI приложение, маршруты статики
├── config.py # Конфигурация (SECRET_KEY, DATABASE_URL)
├── database.py # Подключения get_master_connection / get_slave_connection
├── dependencies.py # Зависимости: get_db_master, get_db_slave, get_current_user, require_role
├── requirements.txt # Прямые зависимости
├── core/
│ └── security.py # bcrypt, JWT, oauth2_scheme
├── app/
│ ├── api/v1/
│ │ ├── routers.py # Главный роутер API
│ │ └── endpoints/
│ │ ├── auth.py # /login, /register, /refresh
│ │ ├── users.py # /me (GET, PUT)
│ │ ├── orders.py # CRUD заказов, /available, /take, /status
│ │ ├── components.py # /components?category=...
│ │ ├── build.py # /build/check (совместимость)
│ │ ├── guarantees.py # POST /guarantees, GET /guarantees
│ │ ├── dashboard.py # /dashboard/stats
│ │ └── hash.py # /api/hash/{str}
│ ├── schemas/ # Pydantic модели
│ ├── services/ # Бизнес-логика
│ ├── repository/ # Слой доступа к данным (SQL)
| ├── pages.py # Роуты, которые выгружают страницы
| └──flask/ # Supporting сервис
|   ├─ main.py # Flask приложение (админ-панель)
└   └── models.py # CRUD функции для админки


## Основные API эндпоинты (FastAPI)

### Аутентификация
- `POST /api/v1/register` – регистрация (customer)
- `POST /api/v1/login` – вход, возвращает JWT access_token
- `POST /api/v1/refresh` – обновить токен (продлить сессию)
- `GET /api/hash/{str}` – получить bcrypt-хеш строки

### Пользователи и профиль
- `GET /api/v1/me` – профиль текущего пользователя (роль, username, для импортёра – телефон, email, ФИО)
- `PUT /api/v1/me` – изменить username (возвращает новый токен)

### Компоненты и сборка
- `GET /api/v1/components?category=Процессор` – список компонентов по русской категории
- `POST /api/v1/build/check` – проверить совместимость набора компонентов (массив id)

### Заказы
- `POST /api/v1/orders/` – создать заказ (customer)
- `GET /api/v1/orders/` – мои заказы (customer/importer)
- `GET /api/v1/orders/available` – доступные заказы (importer)
- `GET /api/v1/orders/{id}` – детали заказа
- `POST /api/v1/orders/{id}/take` – взять заказ в работу (importer)
- `PATCH /api/v1/orders/{id}/status` – изменить статус (importer)

### Гарантии
- `POST /api/v1/guarantees/` – создать обращение (customer)
- `GET /api/v1/guarantees/` – мои обращения (customer)

### Дашборд
- `GET /dashboard` – HTML страница с графиками (admin)
- `GET /api/v1/dashboard/stats` – JSON с данными (admin)

## Ролевая модель
- **customer** – заказчик: регистрируется сам, собирает ПК, создаёт заказы и обращения.
- **importer** – сборщик: создаётся админом, берёт заказы, меняет статус.
- **admin** – администратор: видит дашборд, управляет всеми сущностями через Flask-админку.

Защита роутов: `Depends(get_current_user)` + `Depends(require_role(...))`.

## Репликация Master-Slave
- `get_db_master()` – для INSERT, UPDATE, DELETE.
- `get_db_slave()` – для SELECT.
- Настройки подключения в `config.py` (переменные окружения).

## Запуск

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
Документация: http://127.0.0.1:8000/docs
cd backend
python flask/main.py
Админ-панель: http://127.0.0.1:5000


- Все пароли хэшируются bcrypt (как в FastAPI, так и в Flask).

- JWT токен содержит sub (username), user_role, user_id.

- Статика и шаблоны находятся в общей папке frontend/.

- Для учебного проекта используется один сервер БД с репликацией (Master-Slave), но код поддерживает разделение.

- В админ-панели реализованы поиск, сортировка и фильтрация по всем таблицам.