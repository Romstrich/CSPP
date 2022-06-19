'''...в логе должна быть отражена информация:
"<дата-время> Функция func_z() вызвана из функции main"'''
import sys
import logging


if sys.argv[0].find('client') == -1:
    print('Запущен клиент')
else:
    print('Запущен сервер')
