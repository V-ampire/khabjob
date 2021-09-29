#!/bin/bash

project_path=`pwd`

# Подставляем путь до проекта в конфиги и скрипты
echo Configure project path and domain...
sed -i "s~template_path~$project_path~g" nginx/khabjob.conf systemd/khabjob.server.service

# Подключаем сервера
echo Enable servers...
sudo ln -fns $project_path/nginx/khabjob.conf /etc/nginx/sites-enabled/
sudo ln -fns $project_path/systemd/khabjob.server.service /etc/systemd/system/

# Crontab
sed -i "s~template_path~$project_path~g" scripts/crontab