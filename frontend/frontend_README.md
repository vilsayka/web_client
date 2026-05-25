# Технологии

HTML, CSS, JS

# Зависимости

- itsdangerous==2.2.0
- Jinja2==3.1.6
- MarkupSafe==3.0.3

# Дизайн

Стилизация под Windows XP. Используется фреймворк XP.css (https://botoxparty.github.io/XP.css/).

# Адаптивность

- Компьютеры
- Медиазапросы:
  - max-width: 768px
  - max-width: 480px

Режим администратора — строго для компьютеров.

# Обычный режим

- available_orders.html — список заказов на сборку ПК
- create-pc.html — сборка ПК из комплектующих
- dashboard.html — статистика в виде графиков
- login.html — авторизация
- main.html — главная страница для неавторизованного пользователя
- main-user.html — главная страница для авторизованного пользователя
- my_guarantees.html — обращения по гарантии
- order_detail.html — детали конкретного заказа
- orders.html — все заказы пользователя
- personal_account.html — личный кабинет
- registration.html — регистрация

# Режим администратора

- index.html — шаблон для админских страниц
- main_page.html — главная страница с выводом таблиц
- update_details.html — форма обновления записи
- add.html — кнопки для добавления записи в таблицы
- add_form.html — форма создания новой записи

# Структура проекта

```
frontend/
├── static/
│   ├── css/
│   │   ├── add.css
│   │   ├── create-pc.css
│   │   ├── guarantee.css
│   │   ├── index.css
│   │   ├── main-page-admin.css
│   │   ├── main-page.css
│   │   ├── modal.css
│   │   ├── order.css
│   │   ├── PA.css
│   │   ├── reg-and-login.css
│   │   ├── style.css
│   │   └── update_details.css
│   ├── image/
│   │   ├── component-icons/
│   │   │   ├── CPU-cooling.png
│   │   │   ├── Motherboard.png
│   │   │   ├── pc-case.png
│   │   │   ├── Power-unit.png
│   │   │   ├── Processor.png
│   │   │   ├── RAM-memory.png
│   │   │   ├── Storage-devices.png
│   │   │   └── Video-card.png
│   │   ├── banner.png
│   │   ├── blue-header-mini.png
│   │   ├── blue_header.png
│   │   ├── logo.png
│   │   ├── logo_mini.png
│   │   ├── main_image.jpg
│   │   ├── profile_picture.gif
│   │   └── windows_background.jpg
│   └── js/
│       ├── add_form.js
│       ├── available_orders.js
│       ├── dashboard.js
│       ├── login.js
│       ├── modal.js
│       ├── my_guarantees.js
│       ├── order_detail.js
│       ├── orders.js
│       ├── profile.js
│       ├── registration.js
│       └── utils.js
└── templates/
    ├── add_form.html
    ├── add.html
    ├── available_orders.html
    ├── create-pc.html
    ├── dashboard.html
    ├── index.html
    ├── login.html
    ├── main_page.html
    ├── main-user.html
    ├── main.html
    ├── my_guarantees.html
    ├── order_detail.html
    ├── orders.html
    ├── personal_account.html
    ├── registration.html
    └── update_details.html
```
