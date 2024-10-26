from string import ascii_uppercase as alf
import ngram

text = '''
After World War II, Lubaczów was one of few locations of the Roman Catholic Archdiocese of Lwów to remain within Poland, when the national boundaries were redrawn in 1945. As a result, former parish church in Lubaczow was named a cathedral, and the part of Lwow Archiodiocese, which remained in Poland, was named the Lubaczow Archdiocese, as Communist government banned all traces of Polish presence of the city of Lwow. In 1984, an inventory of the parish records from the archdiocese of the church archive established there was drawn up. In 1992, the position of the Lubaczów area within the Polish diocesan structure was regularized and it became part of the Diocese of Zamość-Lubaczów. There was still a church archive in Lubaczów. In 1999 Lubaczów became part of the Subcarpathian Voivodeship.
'''

def encrypt_cezar(text:str, shift:int = 3):
    shifted_alf = alf[shift:] + alf[:shift]
    encrypted_text = ''
    for c in text:
        index = alf.index(c)
        encrypted_text += shifted_alf[index]
    return encrypted_text

def decrypt_cezar(text:str, shift:int=3):
    shifted_alf = alf[shift:] + alf[:shift]
    encrypted_text = ''
    for c in text:
        index = shifted_alf.index(c)
        encrypted_text += alf[index]
    return encrypted_text

def format_text(input_string:str):
    formatted_string = input_string.upper()
    formatted_string = ''.join(char for char in formatted_string if char in alf)
    return formatted_string

formated_text = format_text(text)
encrypted_text = encrypt_cezar(formated_text,7)
# print(decrypt_cezar("WHVWWDN",3))

def attack_cezar(crypto_text):
    for shift in range(25):
        print(f'{shift}\t{decrypt_cezar(crypto_text,shift)[:40]}')
    return None
def attack_cezar_auto(crypto_text):
    best_score = -99999
    result = ''
    for shift in range(25, -1, -1):
        decrypted_text = decrypt_cezar(crypto_text,shift)
        sc = Scorer.score(decrypted_text)
        if sc > best_score:
            best_score, result = sc, decrypted_text
    return best_score, result

if __name__ == '__main__':
    Scorer = ngram.ngram_score('english_bigrams.txt', sep= ' ')
    # attack_cezar(encrypted_text)
    print(attack_cezar_auto(encrypted_text))


