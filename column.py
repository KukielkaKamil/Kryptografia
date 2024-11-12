import random
import ngram
from time import time as tm

alf = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

text = '''
After World War II, Lubaczów was one of few locations of the Roman Catholic Archdiocese of Lwów to remain within Poland, when the national boundaries were redrawn in 1945. As a result, former parish church in Lubaczow was named a cathedral, and the part of Lwow Archiodiocese, which remained in Poland, was named the Lubaczow Archdiocese, as Communist government banned all traces of Polish presence of the city of Lwow. In 1984, an inventory of the parish records from the archdiocese of the church archive established there was drawn up. In 1992, the position of the Lubaczów area within the Polish diocesan structure was regularized and it became part of the Diocese of Zamość-Lubaczów. There was still a church archive in Lubaczów. In 1999 Lubaczów became part of the Subcarpathian Voivodeship.
'''

def format_text(input_string:str):
    formatted_string = input_string.upper()
    formatted_string = ''.join(char for char in formatted_string if char in alf)
    return formatted_string

def column(matrix, i, numLongerColumns):
    lenCol = len(matrix) if i < numLongerColumns else len(matrix) - 1
    return "".join([matrix[j][i] for j in range(lenCol)])

def encrypt(text,key):
    lenk = len(key)
    matrixHeight = len(text)//lenk if len(text)%lenk == 0 else len(text)//lenk+1
    numLongerColumns = lenk if len(text) % lenk == 0 else len(text)%lenk
    matrix = [text[lenk*i:lenk*(i+1)] for i in range(matrixHeight)]
    encrypted_text = ""
    for columnNumber in key:
        encrypted_text += column(matrix,columnNumber,numLongerColumns)
    return encrypted_text

def decrypt(text,key):
    lenk = len(key)
    matrixHeight = len(text)//lenk if len(text)%lenk == 0 else len(text)//lenk+1
    numLongerColumns = lenk if len(text) % lenk == 0 else len(text)%lenk
    lenColumns = {i:matrixHeight if i<numLongerColumns else matrixHeight-1 for i in range(lenk)}
    matrix = [[""]*lenk for i in range(matrixHeight)]
    columns, currPos = {}, 0
    for columnNumber in key:
        columns[columnNumber] = text[currPos: currPos + lenColumns[columnNumber]]
        currPos += lenColumns[columnNumber]
    for columnNumber in range(lenk):
        for il,letter in enumerate(columns[columnNumber]):
            matrix[il][columnNumber] = letter
    decrypted_text = "".join(["".join(matrix[i]) for i in range(len(matrix))])
    return decrypted_text




Scorer = ngram.ngram_score('english_bigrams.txt', sep= ' ')

def get_rand_key(key_length):
    key = random.sample(range(key_length),key_length)
    # print(key)
    return key

def auto_atack(encrypted_text,max_len=8):
    best_score = -99999
    result = ''
    tt0 = tm()
    while tm() - tt0 <7:
        rand_key_len = random.randint(1,max_len)
        rand_key = get_rand_key(rand_key_len)
        decrypted_text = decrypt(encrypted_text,rand_key)
        sc = Scorer.score(decrypted_text)
        if sc > best_score:
            best_score, result = sc, decrypted_text
    return best_score, result

# TO DO
# def change_key_full(key):
#     r = random.random()
#     r_probs=[0.005, 0.035, 0.03, 0.003, 0.1, 0.02, 0.02, 0.02, 0.01, 0.01, 0.72]
#     if r<sum(r_probs[:1]):
#         return inverse_key(key)
#     elif r<sum(r_probs[:2]):
#         return shift_key(key) # swap 2 fragmens od code
#     elif r<sum(r_probs[:3]):
#         return inverse_fragm_key(key)
#     elif r<sum(r_probs[:4]):
#         return shift_fragm_key(key) # add radnom number and limit it to key lenght %
#     elif r<sum(r_probs[:5]):
#         return swap_3(key)
#     elif r<sum(r_probs[:6]):
#         return shift_key_values(key)
#     elif r<sum(r_probs[:7]):
#         return lengthen_key(key)
#     elif r<sum(r_probs[:8]):
#         return shorten_key_2(key)
#     elif r<sum(r_probs[:9]):
#         return lenghten_key(key)
#     elif r<sum(r_probs[:10]):
#         return shorten_key_2(key)
#     else:
#         return swap_2(key)

# Testin encryption
formated_text = format_text(text)
test_key = get_rand_key(5)
encrypted_text = encrypt(formated_text,test_key)
print(encrypted_text[:40])
# decrypted_text = decrypt(encrypted_text,[5,0,3,1,2,4])
# print(decrypted_text[:40])
auto_atack_decrypted_text = auto_atack(encrypted_text,12)
print(auto_atack_decrypted_text[:40])

# def attackHillClimbing(crypto_text, key_length = 17):
#     best_score = -99999
#     old_key = get_rand_key(stalych_liter)
#     result = ''
#     tt0 = tm()
#     iters= 0
#     while tm() - tt0 < 10:
#         iters += 1
#         rand_key = change_of_key(old_key,stalych_liter)
#         decrypted_text = decrypt(crypto_text,rand_key)
#         sc = Scorer.score(decrypted_text)
#         if sc > best_score:
#             best_score, result, old_key = sc, decrypted_text, rand_key
#             print(best_score, result[:30], old_key, iters)
#     return best_score, result


