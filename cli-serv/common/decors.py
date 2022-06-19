'''...в логе должна быть отражена информация:
"<дата-время> Функция func_z() вызвана из функции main"'''
import sys
import logging

logging.basicConfig(filename = "log/CSApp.log",format = "%(asctime)s %(levelname)-10s %(module)s %(message)s",level = logging.INFO)

print(sys.argv[0].find('client'))
if sys.argv[0].find('client') == -1:
    print('Запущен сервер')
    LOGGER = logging.getLogger('server')
else:
    print('Запущен клиент')
    LOGGER = logging.getLogger('client')

#после того, как определились, кто у нас запущен
#разюерёмся с функционалом

#функция-приёмник(название декоратора)
def log(func_to_log):
    #функция-обёртка(сам декоратор)
    def log_saver(*args,**kwargs):
        print('обернул и вернул')
        LOGGER.info('сообщение')
        dec_func=func_to_log(*args,**kwargs)
        return dec_func
    return log_saver

