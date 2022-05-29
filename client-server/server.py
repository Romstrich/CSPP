'''
Сервер

1. Реализовать простое клиент-серверное взаимодействие по протоколу JIM (JSON instant messaging):
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
    RESPONSE,MAX_CONNECTIONS, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import send_message,get_message, process_client_message

#server.py -a 127.0.0.1 -p 3039
#Какой ip слушаем -a
#Какой порт занимаем -p
def main():
    #пойдём по примеру с порта
    try:
        if '-p' in sys.argv:
            listen_port=int(sys.argv[sys.argv.index('-p')+1]) # следуюющий по порядку параметр
        else:
            listen_port=DEFAULT_PORT
        if listen_port>65535 or listen_port<1024: #пределы портов
            raise ValueError    #зарубим ошибку значения
    except ValueError:
        print('Номер порта от 1024 до 65535.')
        sys.exit(1) #выход с ошибкой
    except IndexError:
        print('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    #натроим прослушку IP
    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]#как и с портом - отсечка по управляющему знаку
        else:
            listen_address = ''#ну...или просто слушаем
    except IndexError:#ошибка наличия адреса
        print(
            'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)
    #работа с сокетом
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#сокет
    transport.bind((listen_address, listen_port))#включамем серверку
    transport.listen(MAX_CONNECTIONS) # Слушаем порт

    while True:
        client, client_address = transport.accept()
        try:
            message_from_client = get_message(client)
            print(message_from_client)
            # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
            response = process_client_message(message_from_client)
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Принято некорретное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    main()