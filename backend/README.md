# Бекенд для агрегатора вакансий г. Хабаровска khabjob.ru.

Написан на:
- `python 3.8` - язык программирования
- `aiohttp` - веб-фреймворк
- `postgresql` - база данных
- `sqlalchemy core` - запросы к базе данных
- `alembic` - управление миграциями базы данных
- `pydantic` - валидация данных
- `pytest` - тесты


## Деплой

Установить следующие переменные окружения:

```
# Режим дебага, off для production
DEBUG=

# Секретный ключ
SECRET_KEY=

# Путь для логов сервера
SERVER_LOGFILE=
# Путь для логов остального приложения
ROOT_LOGFILE=

# Список источников, с которых разрешено делать межсайтовые запросы к API
# https://developer.mozilla.org/ru/docs/Web/HTTP/CORS
CORS_ALLOWED_ORIGINS=

# Секретный ключ для API superjob.ru
SJ_SECRET_KEY=

# Параметры для доступа к API Вконтакте
VK_CLIENT_ID=
VK_ACCESS_TOKEN=

# Настройки Postgresql
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
```




## Команды:

Запускает парсинг вакансий и сохраняет их в базу данных.

- `python main.py update_vacancies`


Запускает парсинг вакансий и выводит их в консоль.

- `python main.py run_parsers`


Запускает сервер API.

- `python main.py run_app`


Инициализирует базу данных.

- `python main.py init_db`


Создать пользователя для доступа к закрытому API (админскому.)

- `python main.py create_user`


## Настройка парсеров.

Настройка парсеров производится в файле `config.py` с помощью словаря `PARSERS_CONFIG`:

```
"<parser name>": {
    ... # параметры парсера
    "is_active": True # обязательное поле, определяет запускать ли этот парсер.
    }
```


## Разработка

- Запуск миграций: `alembic upgrade head`

- Запуск тестов: `pytest`

