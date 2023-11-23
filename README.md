# Service Chat

## Endpoints
- / - chat from customer side
- /register
- /login
- /admin - chat from admin side
- /api/chat/ - get all chats (с фильтрами inbox, all, my)
- /api/chat/ - post user message (or websocket) new or old
- /api/chat/<id> - get chat history (for admin)
- /api/chat/<id>/ - post admin message (ws), accept chat (link to admin)
- /api/login
- /api/register
- 


## Notes
"ws://" + location.host + "/whatever"

## Workflow
- Пользователь отправляет сообщение через webSocket 
- сообщение сохраняется в бд. 
  - если пользователь залогинен, то ищется чат по user
  - если нет, то создается новый чат
  - к чату привязывается сообщение
- в адиминке отображаются все чаты
  - Inbox: если у чата нет админа
  - My: чаты админа
  - all: все чаты
- Админ может открыть чат, и начать в нем писать, 
тогда чат будет перепривязан к нему.
- у пользователя отображаются ответы админа.

## Steps 
- создать сервисы для взаимодействия с бд
- создать систему регистрации и аутенификации
  - хэшировать пароль юзера
  - создавать jwt
- система сообщений
- создать фронтенд для регистрации и логина
- фронтенд для пользователя
- фронтенд для админа

## Dependencies

- `fastapi[all]`
- `datetime`
- `PyMySQL`
- `python-jose[cryptography]`
- `passlib[bcrypt]`