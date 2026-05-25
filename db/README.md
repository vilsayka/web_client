# VibeCore DB — Data Engineering проект

## Роль
**Data Engineer** — проектирование схемы БД, миграции, ETL, репликация PostgreSQL.

## Стек
- PostgreSQL 18
- Python (psycopg2, json)
- Docker
- Streaming replication

## Структура
```bash
db/
├── migrations/
│ ├── 1_create_table_users.sql
│ └── 2_create_all_tables.sql
├── scripts/
│ ├── models.py
│ ├── test_run.py 
│ └── tests_data.json
└── rules_migrations.txt
```

## Что я сделал

### 1. Спроектировал схему базы данных
Разработал структуру из 6 таблиц с нормализацией до 3НФ:
- **users** — ядро системы с ролями (customer, importer, admin)
- **importers** — расширение для импортеров (связь 1:1 с users)
- **orders** — факты заказов с внешними ключами на customer и importer
- **components** — каталог комплектующих с JSONB полем для гибких спецификаций
- **pc_composition** — bridge-таблица для связи many-to-many (orders ↔ components)
- **service_guarantees** — гарантийные обращения по дефектным компонентам

### 2. Написал миграции
Создал два SQL-файла для последовательного развертывания схемы:
- `1_create_table_users.sql` — таблица users + индекс по user_name
- `2_create_all_tables.sql` — все остальные таблицы, индексы (B-Tree, GIN), триггер для auto-update

**Ключевые решения:**
- Использовал `SERIAL PRIMARY KEY` для автоинкремента
- Добавил `CHECK` constraints для ролей и статусов
- Создал GIN индекс на JSONB поле для быстрого поиска по спецификациям
- Написал триггерную функцию `update_modified_column()` для автоматического обновления `updated_at`

### 3. Разработал ETL процесс для загрузки данных
Написал скрипт `test_run.py`, который:
- Читает JSON-файл с тестовыми данными
- Парсит категории комплектующих (processors, gpus, ram, storage и т.д.)
- Вставляет данные в таблицу `components` с конвертацией specifications в JSONB

### 4. Реализовал CRUD-операции на Python
В `models.py` написал функции для работы с каждой таблицей (основные sql-запросы находятся на backend):
- **Users**: `add_user()`, `update_password_user()`, `update_data_user()`, `read_data_user()`
- **Importers**: `add_importer()` (с транзакцией в две таблицы), `update_importer()`, `read_data_importer()`
- **Orders**: `add_order()`, `update_data_order()`, `read_data_order()`
- **Components**: `add_components()`, `update_components()`, `read_data_components()`
- **Service_guarantees**: `add_service_guarantees()`, `update_data_service_guarantees()`, `read_data_service_guarantees()`

### 5. Настроил отказоустойчивую инфраструктуру в Docker
Развернул кластер PostgreSQL с мастер-слейв репликацией:
- Создал Docker-контейнер мастера с пробросом порта 5438
- Настроил параметры репликации: `wal_level = replica`, `max_wal_senders = 10`
- Создал пользователя `replicator` с правами на репликацию
- Сделал `pg_basebackup` для клонирования данных на реплику
- Запустил контейнер реплики на порту 5439
- Проверил работу репликации через `pg_stat_replication`

### 6. Написал документацию по деплою
Создал `rules_migrations.txt` с инструкциями:
- Установка PostgreSQL 18 с конкретным паролем
- Команды для применения миграций через psql
- Полный гайд по развертыванию в Docker с репликацией
