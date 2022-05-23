'''Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с
данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения
каждого параметра поместить в соответствующий список. Должно получиться четыре
списка — например, os_prod_list, os_name_list, os_code_list, os_type_list. В этой же
функции создать главный список для хранения данных отчета — например, main_data
— и поместить в него названия столбцов отчета в виде списка: «Изготовитель
системы», «Название ОС», «Код продукта», «Тип системы». Значения для этих
16столбцов также оформить в виде списка и поместить в файл main_data (также для
каждого файла);'''

import re
import csv
import chardet

def get_data():
    dev_list=[]
    os_list=[]
    code_list=[]
    sys_list=[]
#Считаем содержимое в соответствии с кодировкой
    for i in range(1, 4):
        file = open(f'info_{i}.txt','rb')
        data = file.read()
        result = chardet.detect(data)
        data=data.decode(result['encoding'])
        #print(data)
        # «Изготовитель системы»
        dev_re=re.compile(r'Изготовитель системы:\s*\S*')
        dev_list.append(' '.join(dev_re.findall(data)[0].split()[2:]))
        # dev_info=' '.join(dev_re.findall(data)[0].split()[2:])
        # print(dev_info)
        # «Название ОС»
        os_re =re.compile(r'Название ОС:\s*.*')
        os_list.append(' '.join(os_re.findall(data)[0].split()[2:]))
        # print(os_info)
        #«Кодпродукта»
        code_re = re.compile(r'Код продукта:\s*\S*')
        code_info = ' '.join(code_re.findall(data)[0].split()[2:])
        print(code_info)
        #«Тип системы»
        sys_re = re.compile(r'Тип системы:\s*\S*')
        sys_info = ' '.join(sys_re.findall(data)[0].split()[2:])
        print(sys_info)


#«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».


get_data()
