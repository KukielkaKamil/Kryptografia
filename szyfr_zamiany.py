
import random
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
    iters= 0
    while tm() - tt0 < 10:
        iters += 1
        rand_key = change_of_key(old_key,stalych_liter)
        decrypted_text = decrypt(crypto_text,rand_key)
        sc = Scorer.score(decrypted_text)
        if sc > best_score:
            best_score, result, old_key = sc, decrypted_text, rand_key
            print(best_score, result[:30], old_key, iters)
    return best_score, result

def shogun_attack(crypto_text, stalych_liter = 17,duration=5,key_time=0.7):
    results=[]
    stm= tm()
    while tm() - stm < duration:
        results.append(helperAttackHillClimbing(crypto_text,stalych_liter,key_time))
    results.sort()
    results.reverse()
    return results[0]
        
def helperAttackHillClimbing(crypto_text, stalych_liter = 17,duration=5):
    best_score = -99999
    old_key = get_rand_key(stalych_liter)
    result = ''
    tt0 = tm()
    iters= 0
    while tm() - tt0 < duration:
        iters += 1
        rand_key = change_of_key(old_key,stalych_liter)
        decrypted_text = decrypt(crypto_text,rand_key)
        sc = Scorer.score(decrypted_text)
        if sc > best_score:
            best_score, result, old_key = sc, decrypted_text, rand_key
            # print(best_score, result[:30], old_key, iters)
    return best_score, result

key1 = get_rand_key(20,alf)

text = '''
After World War II, Lubaczów was one of few locations of the Roman Catholic Archdiocese of Lwów to remain within Poland, when the national boundaries were redrawn in 1945. As a result, former parish church in Lubaczow was named a cathedral, and the part of Lwow Archiodiocese, which remained in Poland, was named the Lubaczow Archdiocese, as Communist government banned all traces of Polish presence of the city of Lwow. In 1984, an inventory of the parish records from the archdiocese of the church archive established there was drawn up. In 1992, the position of the Lubaczów area within the Polish diocesan structure was regularized and it became part of the Diocese of Zamość-Lubaczów. There was still a church archive in Lubaczów. In 1999 Lubaczów became part of the Subcarpathian Voivodeship.
'''

def format_text(input_string:str):
    formatted_string = input_string.upper()
    formatted_string = ''.join(char for char in formatted_string if char in alf)
    return formatted_string

f_text = format_text(text)
en_text_1 = encrypt(f_text,key1)

t0 = tm()
print(shogun_attack(en_text_1,0,15,0.7))
t1 = tm()

print(f'czas {t1-t0} sekund')