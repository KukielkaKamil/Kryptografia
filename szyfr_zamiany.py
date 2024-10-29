
import random
from copy import deepcopy
import ngram
from time import time as tm

alf = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

key = ''.join(random.sample(alf,len(alf)))

# print(alf,len(alf))
# print(key)

def encrypt(text, key,alf = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    dictionary = {c: key[i] for i,c in enumerate(alf)}
    encrypted_text = ''

    for c in text:
        encrypted_text += dictionary[c]
    return encrypted_text

en_text = encrypt('TESTSTRING',key,alf)
print(en_text)

def decrypt(text, key, alf = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    dictionary = {c: alf[i] for i,c in enumerate(key)}

    decrypted_text = ''

    for c in text:
        decrypted_text += dictionary[c]
    return decrypted_text

dn_text = decrypt(en_text,key)
print(dn_text)


key1 = ''.join(list(alf[:17]) + random.sample(alf[17:],len(alf[17:])))

# for i in range(5):
#     key1 = ''.join(list(alf[:17]) + random.sample(alf[17:],len(alf[17:])))
#     print(key1)

en_text_1 = encrypt('THISISATESTSTRING',key1)

Scorer = ngram.ngram_score('english_bigrams.txt', sep= ' ')

# Lab version (almost :p)
def attack_auto(crypto_text,stalych_liter = 17):
    best_score = -99999
    result = ''
    tt0 = tm()
    while tm() - tt0 <5:
        rand_key = ''.join(list(alf[:stalych_liter]) + random.sample(alf[stalych_liter:],len(alf[stalych_liter:])))
        decrypted_text = decrypt(crypto_text,rand_key)
        sc = Scorer.score(decrypted_text)
        if sc > best_score:
            best_score, result = sc, decrypted_text
    return best_score, result

# My version
def attack_auto2(crypto_text,stalych_liter = 17, attempts = 1000):
    best_score = -99999
    result = ''
    for i in range(attempts):
        rand_key = ''.join(list(alf[:stalych_liter]) + random.sample(alf[stalych_liter:],len(alf[stalych_liter:])))
        decrypted_text = decrypt(crypto_text,rand_key)
        sc = Scorer.score(decrypted_text)
        if sc > best_score:
            best_score, result = sc, decrypted_text
    return best_score, result

t0 = tm()
print(attack_auto(en_text_1,17))
t1 = tm()

print(f'czas {t1-t0} sekund')