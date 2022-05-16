

word1='class'
word2='function'
word3='method'


byte1=bytes(word1,'utf-8')
byte2=bytes(word2,'utf-8')
byte3=bytes(word3,'utf-8')

print(f'{word1}\t {word2}\t {word3}')
print(f'{type(word1)} {type(word2)} {type(word3)}')
print(f'{byte1}\t {byte2}\t {byte3}')
print(f'{type(byte1)} {type(byte2)} {type(byte3)}')