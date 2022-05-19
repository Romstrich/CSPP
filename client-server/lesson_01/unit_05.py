'''Выполнить пинг веб-ресурсов yandex.ru, youtube.com
и преобразовать результаты из байтовового в строковый тип на кириллице.'''

import subprocess
import chardet

my_ping = subprocess.Popen(["/bin/ping", "-c4", "yandex.ru"], stdout=subprocess.PIPE)

for line in my_ping.stdout:
    result = chardet.detect(line)
    print(result)
    line = line.decode(result['encoding']).encode('utf-8')
    print(line.decode('utf-8'))
