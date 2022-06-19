'''Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое
программирование», «сокет», «декоратор». Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое.'''

with open('test_file.txt', 'rb') as file:
    text = file.read()
    print(text.decode('utf-8'))