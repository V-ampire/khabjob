from datetime import timedelta
from environs import Env
import pathlib


env = Env()
env.read_env()  # read .env file, if it exists


BASE_DIR = pathlib.Path(__file__).parent


DEBUG = env.bool('DEBUG', default=False)


PARSERS_CONFIG = {
    "superjob": {
        "parse_url": "https://api.superjob.ru",
        "secret_key": env.str('SJ_SECRET_KEY'),
        "id": 1091,
        "v": "2.33",
        "is_active": True
    },
    "farpost": {
        "parse_url": "https://www.farpost.ru/khabarovsk/job/vacancy",
        "is_active": False
    },
    "hh": {
        "parse_url": "https://api.hh.ru/vacancies/",
        "is_active": True
    },
    "vk": {
        "parse_url": "https://api.vk.com/method/newsfeed.search",
        "client_id": env.str('VK_CLIENT_ID'),
        "access_token": env.str('VK_ACCESS_TOKEN'),
        "v": 5.95,
        "is_active": True
    }
}

VACANCY_EXPIRED = timedelta(weeks=4*2) # Clean vacancies every 2 mounth


SELF_SOURCE_NAME = 'khabjob' # Name of source for vacancies added on site


POSTGRES_CONFIG = {
    'POSTGRES_DB': env.str('POSTGRES_DB'),
    'POSTGRES_USER': env.str('POSTGRES_USER'),
    'POSTGRES_PASSWORD': env.str('POSTGRES_PASSWORD'),
    'POSTGRES_HOST': env.str('POSTGRES_HOST'),
    'POSTGRES_PORT': env.str('POSTGRES_PORT'),
}


TIMEZONE = 'Asia/Vladivostok'


AUTH_CONFIG = {
    'SECRET_KEY': env.str('SECRET_KEY', default='No-no, its a secret!'),
    'ALGORITHM': "HS256",
    'JWT_AUTH_SCHEME': 'Bearer',
    'JWT_HEADER_NAME': 'Authorization',
    'JWT_LIFETIME': timedelta(days=30),
    'PASSWORD_PATTERN': r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
}


CORS_CONFIG = {
    'CORS_ALLOWED_ORIGINS': env.list('CORS_ALLOWED_ORIGINS')
}
