# Агрегатор вакансий города Хабаровск.

Проект создан **исключительно в учебных целях** и не предусматривает коммерческого использования.

Сайт доступен по адресу: [khabjob.ru](https://khabjob.ru)


[Вход](https://khabjob.ru/login) в админку:

(*Вы можете посмотреть админ-панель для управления вакансиями*)

- Логин: `demouser`
- Пароль `demoPass%11`


## Использованные технологии

Проект состоит из двух частей:

- Серверная часть, в виде REST API использует:
    - Python 3.8
    - Aiohttp
    - SQLAlchemy CORE
    - PostgresQL

- Клиентская часть в виде SPA написана на:
    - Vue JS 2
    - Axios
    - BootstrapVue


## В проекте реализовано

- Сбор вакансий из открытых источников
- Возможность добавления новых вакансий через форму обратной связи
- Сортировка вакансий по дате добавления, полнотекстовый поиск по вакансиям
- Закрытая часть сайта для администраторов
- JWT аутентификация


## Деплой

Настроить конфиги `nginx` и `systemd`:

`$ source scripts/setup_configs.sh`


### Фронтенд

Установить переменные окружения см. [описание фронтенда](/frontend/README.md)

```
$ cd frontend
$ npm install
$ npm run build
$ sudo service nginx restart
```


### Бэкенд

Установить переменные окружения см. [описание бэкенда](/backend/README.md)

```
$ source scripts/init_backend.sh
$ sudo systemctl daemon-reload
$ sudo systemctl start khabjob.server
$ sudo systemctl enable khabjob.server
$ sudo chmod 666 /tmp/khabjob.sock
$ sudo service nginx restart
```


Настройка автоматического обновления и очистки старых вакансий:

`$ crontab scripts/crontab`

