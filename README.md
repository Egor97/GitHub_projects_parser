# GitHub_projects_parser

<u>Запуск приложения</u>\
Команда для сборки контейнера
1. docker build -t <имя контейнера> \

В compose файле заменить имя контейнера и прокинуть .env файл. Запуск парсера через docker-compose
2. docker compose up -d

Переменные окружения используемые в проекте:
POSTGRES_USER, POSTGRES_PASS, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB