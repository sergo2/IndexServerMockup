Назначение
=============
Имитация веб-сервиса Index Server

Требования к серверу
=============
1. Python 3.6 или выше

Запуск приложения
=============
$PYTHON_PATH/python server.py <composition_receiver_state> <realtime_receiver_state>

Работа приложения
=============
1. Запускается HTTP-сервер на порту из config.py
2. Статус сервисов composition и realtime задается в конфиге или через аргументы командной строки
3. Если в конфиге save_index_error = True, активация новой версии будет вызывать ошибку 