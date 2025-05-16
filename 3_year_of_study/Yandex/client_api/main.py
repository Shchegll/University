# /client_api/main.py

from pyrogram import Client

api_id = 23932726
api_hash = '431ebce4e163ae6935beb4ea82f60a0d'

# Создаём программный клиент, передаём в него
# имя сессии и данные для аутентификации в Client API
app = Client('my_account', api_id, api_hash)

app.start()
# Отправляем сообщение
# Первый параметр — это id чата (тип int) или имя получателя (тип str).
# Зарезервированное слово 'me' означает собственный аккаунт отправителя.
app.send_message('me', 'Привет, это я!')
app.stop()
