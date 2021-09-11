# Бекенд дл агрегатора вакансий г. Хабаровска khabjob.ru.


## Переменные окружения

Установить следующие переменные окружения:

```
# Путь для доступа к API, с указанием протокола, 
# например https:://khabjob.ru/api
API_ROOT=

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

