import logging

logging.basicConfig(filename = "app.log",format = "%(levelname)-10s %(asctime)s %(message)s",level = logging.INFO)
log = logging.getLogger('first_logger')
log.info('Hello, logging!!!')

def first_function():
    print('first function started')
    log.info('first function works stable')
    return 'first function return'

def second_function():
    print('second function started')
    log.info('second function works stable')
    return 'second function return'

def third_function(file_name):
    try:
        with open(file_name,'r',encoding='utf-8') as file:
            print(file.read())
            log.info('file is OK')
    except BaseException as error:
        print('ERROR EXIT')
        log.error('File error, check file')
        exit(1)


if __name__=='__main__':
    print(first_function())
    log.info('first function return OK')
    print(second_function())
    log.info('second function return OK')
    third_function('app.log')