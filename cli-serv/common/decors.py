'''...в логе должна быть отражена информация:
"<дата-время> Функция func_z() вызвана из функции main"'''
import sys
import logging
import traceback
import inspect

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
        LOGGER.info(f'--- {LOGGER.name} ---' 
                    f'Была вызвана функция {func_to_log.__name__} c параметрами {args}, {kwargs}. '
                    f'Вызов из модуля {func_to_log.__module__}. Вызов из'
                    f' функции {traceback.format_stack()[0].strip().split()[-1]}.'
                    f'Вызов из функции {inspect.stack()[1][3]}')
        dec_func=func_to_log(*args,**kwargs)
        # print(LOGGER.name)
        return dec_func
    return log_saver

