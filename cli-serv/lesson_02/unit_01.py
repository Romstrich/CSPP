'''Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с
данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения
каждого параметра поместить в соответствующий список. Должно получиться четыре
списка — например, os_prod_list, os_name_list, os_code_list, os_type_list
. В этой же

функции создать главный список для хранения данных отчета — например, main_data
— и поместить в него названия столбцов отчета в виде списка: «Изготовитель
системы», «Название ОС», «Код продукта», «Тип системы». Значения для этих
16столбцов также оформить в виде списка и

поместить в файл main_data (также для
каждого файла);'''

import re
import csv
import chardet


def get_data():
    dev_list = []
    os_list = []
    code_list = []
    sys_list = []
    main_data = []
    # Считаем содержимое в соответствии с кодировкой
    for i in range(1, 4):
        file = open(f'info_{i}.txt', 'rb')
        data = file.read()
        result = chardet.detect(data)
        data = data.decode(result['encoding'])

        # «Изготовитель системы»
        dev_re = re.compile(r'Изготовитель системы:\s*\S*')
        dev_list.append(' '.join(dev_re.findall(data)[0].split()[2:]))

        # «Название ОС»
        os_re = re.compile(r'Название ОС:\s*.*')
        os_list.append(' '.join(os_re.findall(data)[0].split()[2:]))

        # «Кодпродукта»
        code_re = re.compile(r'Код продукта:\s*\S*')
        code_list.append(' '.join(code_re.findall(data)[0].split()[2:]))

        # «Тип системы»
        sys_re = re.compile(r'Тип системы:\s*\S*')
        sys_list.append(' '.join(sys_re.findall(data)[0].split()[2:]))

    print(f'{dev_list}\n{os_list}\n{code_list}\n{sys_list}')

    # «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
    headers = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    main_data.append(headers)

    j = 1
    for i in range(0, 3):
        row_data = []
        row_data.append(j)
        row_data.append(dev_list[i])
        row_data.append(os_list[i])
        row_data.append(code_list[i])
        row_data.append(sys_list[i])
        main_data.append(row_data)
        j += 1
#    print(main_data)
    return main_data

def write_csv(file='table.csv'):

    main_data=get_data()

    with open(file,'w',encoding='utf-8') as out_file:
        writer = csv.writer(out_file, quoting=csv.QUOTE_NONNUMERIC)
        for row in main_data:
            writer.writerow(row)

#get_data()
write_csv('my_data.csv')
