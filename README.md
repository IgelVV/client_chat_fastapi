# Service Chat

## Описание

Тестовое задание для компании 
"ООО Научно-Исследовательский Институт Цифровые Технологии".

### Требования
- Написать модуль переписки посетителя сайта и админа техподдержки
- По аналогии и взамен JivoChat
- Вся переписка хранится в базе в привязке к пользователю, если он авторизован.
- Оформить API эндпоинты с помощью fastapi
- Небольшой Frontend (буквально визуализировать данные)
- Оформить всё в Docker.
- Важно, стек ровно тот, что прописан в вакансии


С учетом требований стек проекта составил:
  - React
  - Python, 
  - FastApi, 
  - pymysql,
  - MariaDB

Не использовалась ORM, так как она не указана в стеке вакансии.
В базе данных 3 сущности `User`, `Chat`, `Message`.
Реализована аутентификация с помощью JWT.
Чат реализован через WebSocket.

## Deploy
Для разворачивания проекта, необходимо:
- клонировать с Git
- скопировать `.env.template` как `.env`
- выполнить `docker compose up --build`

Frontend запускается на порту `3000`, Backend на порту `8000`. 
При использовании нестандартоного хоста, необходимо прописать его в
переменную окружения `ALLOWED_ORIGINS` в файле `.env`.

## Использование
При первом запуске проекта в базе данных, есть 2 тестовых пользователя
`username=admin password=password`, `username=user password=password`.
После регистрации необходимо залогиниться. 
Далее в зависимости от роли `admin` или `customer`, доступны
разные разделы сайта.
Для клиентов доступен только чат.
Для админа доступна панель с выбором чатов клиентов.
Клиент не может получить доступ админ панели.

На порту 8000 развернут Backend, по эндпойнту `/docs` доступна интерактивная 
документация.

Клинты и админы видят историю своего чата, а так же в режиме реального
времени получают сообщения от оппонента.

Сообщения привязаны к отправителю и чату,
В чатах могут быть только 2 пользователя (`admin`, `customer`).

До того как клиент начнет чат, админ не может его создать, и вначале работы
во всех разделах меню будет пусто. 
Необходимо зайти от имени клиента `user` и написать хоть что-то.

Если создать других админа и клиента, то сообщения из их чата будут видны только им,
однако, если другой админ зайдет в этот чат, то чат перепривяжется на него.
