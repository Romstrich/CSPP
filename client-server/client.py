'''
Клиент1.

Реализовать простое клиент-серверное взаимодействие по протоколу JIM (JSON instant messaging):
клиент отправляет запрос серверу;
сервер отвечает соответствующим кодом результата. Клиент и сервер должны быть реализованы в виде
отдельных скриптов, содержащих соответствующие функции. Функции клиента: сформировать presence-сообщение;
отправить сообщение серверу; получить ответ сервера; разобрать сообщение сервера; параметры командной
строки скрипта client.py <addr> [<port>]: addr — ip-адрес сервера; port — tcp-порт на сервере, по
умолчанию 7777. Функции сервера: принимает сообщение клиента; формирует ответ клиенту; отправляет
ответ клиенту; имеет параметры командной строки: -p <port> — TCP-порт для работы (по умолчанию
использует 7777); -a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).


'''

import sys
import json
import socket
import time
#модуль с готовыми заголовками протокола
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT

#server.py 127.0.0.1  3039
#На какой ip стучимся
#В какой порт ломим
def main():
    #для клиента параметры указаны без управляющих символов(просто по порядку)
    try:
        server_address = sys.argv[2]    #IP
        server_port = int(sys.argv[3])  #port
        if server_port < 1024 or server_port > 65535:
            raise ValueError #зарубим ошибку значения
    except IndexError: #Если что-то не так - падаем в дефолт
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        print('Номер порта от 1024 до 65535. от 1024 до 65535.')
        sys.exit(1)
    pass

if __name__=='__main__':
    main()