from itertools import combinations
from time import time as ttime

alfabet='abcdefghijklmnopqrstuvwxyz'

with open('book6.txt', encoding='utf-8') as f:
    book = f.read()

print( len(book) )

book2 = ''.join( [x for x in book if x.isalpha() and x in alfabet ] ).lower()

print( len(book2) )

print(
    len(
        list(
            combinations(list(alfabet), 2)
            )
        )
    )

dct = {}
for bigram in combinations(list(alfabet), 2):
    dct[ ''.join(bigram) ] = 0
    dct[ bigram[1] + bigram[0] ] = 0
for c in alfabet:
    dct[ c+c ] = 0
#[ print( ''.join(k), end=',' ) for k in dct.keys() ]
print( len(dct.keys() ) )


t0 = ttime()
for i in range( len( book2)-2 ):
    bigram = book2[i] + book2[i+1]
    dct[ bigram ] += 1

t1 = ttime()
print( round( t1-t0,3), ' sec')

srt = []
for k in dct.keys():
    srt.append( (dct[k],k) )

srt.sort()
srt.reverse()

#[ print( (''.join(k), dct[k]), end='\t' ) for k in dct.keys() ]

with open('my_english_bigrams.txt', 'w', encoding='utf-8') as f:
    for elem in srt:
        f.write( elem[1] + ' ' + str( elem[0] ) + '\n' )

