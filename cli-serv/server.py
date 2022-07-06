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
import logging
import sys
import json
import socket
import select
import time
#модуль с готовыми заголовками протокола
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE,MAX_CONNECTIONS, ERROR,  DEFAULT_PORT,MESSAGE,MESSAGE_TEXT,SENDER,\
    DESTINATION, RESPONSE_200, RESPONSE_400

from common.utils import send_message,get_message
#модуль с декоратором
from common.decors import *

#создадим лог серверу
logging.basicConfig(filename = "log/CSApp.log",format = "%(asctime)s %(levelname)-10s %(module)s %(message)s",level = logging.INFO)
LOGGER = logging.getLogger('server_logger')

@log
def process_client_message(message, messages_list, client, clients, names):
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message:
        #Регистрация
        if message[USER][ACCOUNT_NAME] not in names.keys():
            names[message[USER][ACCOUNT_NAME]] = client
            send_message(client, RESPONSE_200)
        else:
            response = RESPONSE_400 #сообщение об ошибке
            response[ERROR] = 'Имя пользователя уже занято.'
            send_message(client, response)
            clients.remove(client)
            client.close()# закрыл сокет
        return
    elif ACTION in message and message[ACTION] == MESSAGE and \
            TIME in message and MESSAGE_TEXT in message and \
            DESTINATION in message and SENDER in message:
        messages_list.append(message)#в список рассылки
        return
        # Иначе отдаём Bad request
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return

# отправка клиенту
def process_message(message, names, listen_socks):
    #message[DESTINATION] - имя
    #names[message[DESTINATION]] получатель
    if message[DESTINATION] in names and names[message[DESTINATION]] in listen_socks:
        send_message(names[message[DESTINATION]], message)
        print(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                    f'от пользователя {message[SENDER]}.')
    elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
        raise ConnectionError
    else:
        print(f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
            f'отправка сообщения невозможна.')

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
        log.error('некорректный порт в параметре')
        print('Номер порта от 1024 до 65535.')
        sys.exit(1) #выход с ошибкой
    except IndexError:
        log.error('некорректный порт в параметре')
        print('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    #натроим прослушку IP
    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]#как и с портом - отсечка по управляющему знаку
        else:
            listen_address = ''#ну...или просто слушаем
    except IndexError:#ошибка наличия адреса
        log.error('некорректный адрес в параметре')
        print(
            'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)
    #работа с сокетом
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#сокет
    transport.bind((listen_address, listen_port))#включамем серверку
    transport.settimeout(0.5)#Зазор прослушки
    transport.listen(MAX_CONNECTIONS) # Слушаем порт

    # список клиентов , очередь сообщений
    clients = []
    messages = []

    while True:
        # Ждём подключения, если таймаут вышел, ловим исключение.
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            print(f'соединено {client_address}')
            clients.append(client)

        #Списки очередей
        recv_data_lst = []
        send_data_lst = []
        err_lst = []
        #Берём ждунов
        try:
            if clients:
                #работа с select (переключатель)
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        #Разберём очередь сообщений
        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    print(f'Клиент {client_with_message.getpeername()} Подключен')
                    process_client_message(get_message(client_with_message),messages, client_with_message)

                except:
                    print(f'Клиент {client_with_message.getpeername()} отключился от сервера.')
                    clients.remove(client_with_message)

        if messages and send_data_lst:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    print(message)
                    send_message(waiting_client, message)
                except:
                    LOGGER.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    clients.remove(waiting_client)




if __name__ == '__main__':
    main()