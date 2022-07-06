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
import logging
import sys
import json
import socket
import time
from errors import IncorrectDataRecivedError, ReqFieldMissingError, ServerError



# модуль с готовыми заголовками протокола
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    MESSAGE, SENDER, DEFAULT_IP_ADDRESS, DEFAULT_PORT, EXIT, MESSAGE_TEXT,\
    DESTINATION, RESPONSE
from common.utils import get_message, send_message
#модуль с декоратором
from common.decors import *


#Создадим лог клиенту
logging.basicConfig(filename = "log/CSApp.log",format = "%(asctime)s %(levelname)-10s %(module)s %(message)s",level = logging.INFO)
LOGGER = logging.getLogger('client_logger')

#сообщение о выходе
@log
def create_exit_message(account_name):
    return {
        ACTION: EXIT,
        TIME: time.time(),
        ACCOUNT_NAME: account_name
    }

def message_from_server(socket, my_username):
    while True:
        try:
            message = get_message(socket)
            if ACTION in message and message[ACTION] == MESSAGE and \
                    SENDER in message and DESTINATION in message \
                    and MESSAGE_TEXT in message and message[DESTINATION] == my_username:
                print(f'\n{message[SENDER]} написал:'
                      f'\n{message[MESSAGE_TEXT]}')
            else:
                print(f'Получено некорректное сообщение с сервера: {message}')
        except IncorrectDataRecivedError:
            print(f'Не удалось декодировать полученное сообщение.')
        except (OSError, ConnectionError, ConnectionAbortedError,
                ConnectionResetError, json.JSONDecodeError):
            print(f'Потеряно соединение с сервером.')
            break

#посылка сообщения
def create_message(sock, account_name='Guest'):
    to_user = input('Введите получателя сообщения: ')
    message = input('Введите сообщение для отправки: ')
    message_dict = {
        ACTION: MESSAGE,
        SENDER: account_name,
        DESTINATION: to_user,
        TIME: time.time(),
        MESSAGE_TEXT: message
    }
    LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
    try:
        send_message(sock, message_dict)
        LOGGER.info(f'Отправлено сообщение для пользователя {to_user}')
    except:
        LOGGER.critical('Потеряно соединение с сервером.')
        sys.exit(1)

def user_interactive(sock, username):
    """Функция взаимодействия с пользователем, запрашивает команды, отправляет сообщения"""
    print_help()
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            create_message(sock, username)
        elif command == 'help':
            print_help()
        elif command == 'exit':
            send_message(sock, create_exit_message(username))
            print('Завершение соединения.')
            LOGGER.info('Завершение работы по команде пользователя.')
            # Задержка неоходима, чтобы успело уйти сообщение о выходе
            time.sleep(0.5)
            break
        else:
            print('Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')

def print_help():
    """Функция выводящяя справку по использованию"""
    print('Поддерживаемые команды:')
    print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
    print('help - вывести подсказки по командам')
    print('exit - выход из программы')


@log
def create_presence(account_name):
    LOGGER.debug('Сообщение серверу')
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out
@log
def process_response_ans(message):
    """
    Функция разбирает ответ сервера на сообщение о присутствии,
    возращает 200 если все ОК или генерирует исключение при ошибке
    :param message:
    :return:
    """
    LOGGER.debug(f'Разбор приветственного сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        elif message[RESPONSE] == 400:
            raise ServerError(f'400 : {message[ERROR]}')
    raise ReqFieldMissingError(RESPONSE)

def process_ans(message):
    return message


# client.py 127.0.0.1  3039
# На какой ip стучимся
# В какой порт ломим
def main():
    # для клиента параметры указаны без управляющих символов(просто по порядку)
    try:
        server_address = sys.argv[2]  # IP
        server_port = int(sys.argv[3])  # port
        if server_port < 1024 or server_port > 65535:
            raise ValueError  # зарубим ошибку значения
    except IndexError:  # Если что-то не так - падаем в дефолт
        # log.error('некорректный адрес сервера - переход к дефолтным значениям')
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        log.error('некорректный порт сервера - завершение работы')
        print('Номер порта от 1024 до 65535. от 1024 до 65535.')
        sys.exit(1)
    pass

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # заводим сокет
    transport.connect((server_address, server_port))  # стучим
    while True:
        message_to_server = create_presence()  # тут надо сконструировать
        print(message_to_server)
        send_message(transport, message_to_server)  # отправить
        try:
            answer = process_ans(get_message(transport))  # принять ответ
            print(answer)
        except (ValueError, json.JSONDecodeError):
            # log.error('некорректная кодировка')
            print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()
