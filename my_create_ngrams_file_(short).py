from itertools import product
alfabet2='abcdefghijklmnopqrstuvwxyz'
alfabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ';
nlength = 2
with open('book6.txt', encoding='utf-8') as f:
    book = f.read()
book2 = ''.join( [x for x in book if x.isalpha() and x in alfabet ] ).upper() #Change to lower() if you want to use alfabet2
dct, srt = {}, []
for ngram in (''.join(chars) for chars in product(alfabet, repeat=nlength)):
        dct[ngram] = 0
for i in range( len( book2)-nlength ):
    dct[ book2[i:i+nlength] ] += 1
for k in dct.keys():
    srt.append( (dct[k],k) )
srt.sort(reverse=True)
with open('my_english_bigrams.txt', 'w', encoding='utf-8') as f:
    for elem in srt: f.write( elem[1] + ' ' + str( elem[0] ) + '\n' )
