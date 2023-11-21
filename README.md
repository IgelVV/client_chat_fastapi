# Service Chat

## DB structure 

### Table User
- id
- username
- password
- is_admin

### Table Message
- chat
- datetime
- text

### Table Chat
- id
- customer(user, Null)
- admin(user, Null)

## Endpoints
- / - chat from customer side
- /login
- /admin - chat from admin side
- /api/chat/<id> - get chat history


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