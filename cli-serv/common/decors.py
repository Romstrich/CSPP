'''...в логе должна быть отражена информация:
"<дата-время> Функция func_z() вызвана из функции main"'''
import sys
import logging


print(sys.argv[0].find('client'))
if sys.argv[0].find('client') == -1:
    print('Запущен сервер')
else:
    print('Запущен клиент')
