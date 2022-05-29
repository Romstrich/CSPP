'''3. Определить, какие из слов «attribute», «класс», «функция», «type» невоз
можно записать в байтовом типе.'''

words = ['attribute', 'класс', 'функция']

for word in words:
    print(f'{word}\t{type(word)}')
    try:
        print(bytes(word, 'ascii'))
    except BaseException as e:
        print('Ошибка:', e)
        print(f'{"*" * 10}{word} не подходит для прямого перевода в байты')
