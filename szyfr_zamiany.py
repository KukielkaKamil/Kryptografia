
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

def get_rand_key(shift, alf = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    key = ''.join(list(alf[:shift]) + random.sample(alf[shift:],len(alf[shift:])))
    return key



Scorer = ngram.ngram_score('english_bigrams.txt', sep= ' ')

# Lab version (almost :p)
def attack_auto(crypto_text,stalych_liter = 17):
    best_score = -99999
    result = ''
    tt0 = tm()
    while tm() - tt0 <20:
        rand_key = get_rand_key(stalych_liter)
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
        rand_key = get_rand_key(stalych_liter)
        decrypted_text = decrypt(crypto_text,rand_key)
        sc = Scorer.score(decrypted_text)
        if sc > best_score:
            best_score, result = sc, decrypted_text
    return best_score, result

def change_of_key(old_key, stalych_liter=17):
    i,j = sorted(random.sample(list(range(stalych_liter,26)),2))
    key_new = old_key[:i] + old_key[j] + old_key[i+1:j] + old_key[i] + old_key[j+1:]
    return key_new

def attackHillClimbing(crypto_text, stalych_liter = 17):
    best_score = -99999
    old_key = get_rand_key(stalych_liter)
    result = ''
    tt0 = tm()
    while tm() - tt0 <5:
        rand_key = change_of_key(old_key,stalych_liter)
        decrypted_text = decrypt(crypto_text,rand_key)
        sc = Scorer.score(decrypted_text)
        if sc > best_score:
            best_score, result, old_key = sc, decrypted_text, rand_key
    return best_score, result

key1 = get_rand_key(20,alf)


en_text_1 = encrypt('THISISATESTSTRINGTHATISREALLYAWESOME',key1)

t0 = tm()
print(attackHillClimbing(en_text_1,20))
t1 = tm()

print(f'czas {t1-t0} sekund')