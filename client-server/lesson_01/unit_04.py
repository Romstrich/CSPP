'''
Преобразовать слова «разработка», «администрирование», «protocol», «standard» из
строкового представления в байтовое и выполнить обратное преобразование (используя методы encode и decode).
'''

words=['разработка', 'администрирование', 'protocol', 'standard']
encode_words=[w.encode('UTF-8') for w in words]
for w in encode_words:
    print(f'{type(w)}\t{w}')
words=[w.decode('UTF-8') for w in encode_words]
for w in words:
    print(f'{type(w)}\t{w}')
