import random
import ngram
from time import time as tm
import concurrent.futures

import random

Scorer = ngram.ngram_score('english_bigrams.txt', sep= ' ')


alf = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def format_text(input_string:str):
    formatted_string = input_string.upper()
    formatted_string = ''.join(char for char in formatted_string if char in alf)
    return formatted_string

def extend_string(text:str,n):
    for i in range(n):
        text+= random.choice(alf)
    return text

def encrypt(text: str, key):
    """
    Encrypts a text using a columnar transposition cipher based on a key.
    
    Args:
        text (str): The text to be encrypted.
        key (list of lists): A 2D list defining the columnar transposition order.
    
    Returns:
        str: The encrypted text.
    """
    n = len(key)  # Number of rows based on the key
    # Ensure result list is properly sized
    if len(text) % n != 0:
        residual = n - (len(text) % n)
        text = extend_string(text,residual)

    row_len = len(text) // n  # Length of each row
    # Initialize the result list
    result = [''] * len(text)
    
    # Fill the result list using the key
    for row in range(n):
        for col in range(row_len):
            source_pos = row * row_len + col  # Position in the input text
            char = text[source_pos]          # Character at the source position
            target_col = key[row][col % len(key[row])] - 1  # Adjust for 0-based index
            
            # Compute the target position and place the character
            target_pos = col * n + target_col
            result[target_pos] = char
    
    # Combine the result list into a string and return
    return ''.join(result)


def decrypt(text: str, key):
    """
    Encrypts a text using a columnar transposition cipher based on a key.
    
    Args:
        text (str): The text to be encrypted.
        key (list of lists): A 2D list defining the columnar transposition order.
    
    Returns:
        str: The encrypted text.
    """
    n = len(key)  # Number of rows based on the key
    row_len = len(text) // n  # Length of each row
    
    # Initialize the result list
    result = [''] * len(text)
    
    # Fill the result list using the key
    for row in range(n):
        for col in range(row_len):
            key_shift = key[row][col % len(key[row])] - 1
            target_pos = row*row_len + col
            result[target_pos] = text[col*n + key_shift]
    
    # Combine the result list into a string and return
    return ''.join(result)


def is_valid(grid, row):
    n = len(row)
    for col_idx in range(n):
        # Zbierz wszystkie wartości z kolumny
        column_values = [grid[row_idx][col_idx] for row_idx in range(len(grid))]
        # Dodaj wartość z bieżącego wiersza
        column_values.append(row[col_idx])
        # Sprawdź, czy liczby są unikalne
        if len(set(column_values)) != len(column_values):
            return False
    return True

def get_rand_key(n):
    # Inicjalizuj pustą siatkę
    grid = []
    
    # Wygeneruj listę liczb od 1 do n
    numbers = list(range(1, n + 1))
    
    for _ in range(n):
        # Przetasuj liczby dla wiersza
        row = numbers[:]
        random.shuffle(row)
        
        # Sprawdzaj poprawność i przetasowuj w razie potrzeby
        while not is_valid(grid, row):
            random.shuffle(row)
        
        # Dodaj wiersz do siatki
        grid.append(row)
    
    return grid



def auto_atack(encrypted_text,key_len=8):
    best_score = -99999
    result = ''
    best_key = []
    tt0 = tm()
    while tm() - tt0 <10:
        rand_key_len = random.randint(1,key_len)
        rand_key = get_rand_key(rand_key_len)
        decrypted_text = decrypt(encrypted_text,rand_key)
        sc = Scorer.score(decrypted_text)
        # print( best_score, sc, result)
        if sc > best_score:
            best_score, result,best_key = sc, decrypted_text, rand_key
            print(best_score, result)
    return best_score, result,best_key

def change_of_key(key):
    if random.choice([True, False]):  # Randomly choose to swap rows or columns
        # Swap two rows
        row1, row2 = random.sample(range(len(key)), 2)
        key[row1], key[row2] = key[row2], key[row1]
    else:
        # Swap two columns
        col1, col2 = random.sample(range(len(key[0])), 2)  # Assuming the array has at least one row
        for row in key:
            row[col1], row[col2] = row[col2], row[col1]

    return key


def attackHillClimbing(crypto_text, key_length = 10):
    best_score = -99999
    old_key = get_rand_key(key_length)
    result = ''
    tt0 = tm()
    iters= 0
    while tm() - tt0 < 30:
        iters += 1
        rand_key = change_of_key(old_key)
        decrypted_text = decrypt(crypto_text,rand_key)
        sc = Scorer.score(decrypted_text)
        # print(f'All iterations: {iters} Current score: {sc}, Current key: {rand_key}')
        if sc > best_score:
            best_score, result, old_key = sc, decrypted_text, rand_key
            print(best_score, result[:30], old_key, iters)
    return best_score, result


def helperAttackHillClimbing(crypto_text, key_length = 10,duration=5):
    best_score = -99999
    old_key = get_rand_key(key_length)
    result = ''
    tt0 = tm()
    iters= 0
    while tm() - tt0 < duration:
        iters += 1
        rand_key = change_of_key(old_key)
        decrypted_text = decrypt(crypto_text,rand_key)
        sc = Scorer.score(decrypted_text)
        if sc > best_score:
            best_score, result, old_key = sc, decrypted_text, rand_key
            # print(best_score, result[:30], old_key, iters)
            print(best_score, result[:40])
    return best_score, result, old_key

def shogun_attack(crypto_text, key_length = 5 ,duration=5,key_time=0.7):
    results=[]
    stm= tm()
    while tm() - stm < duration:
        results.append(helperAttackHillClimbing(crypto_text,key_length,key_time))
    results.sort()
    results.reverse()
    return results[0]


def shogun_attack_multithreaded(crypto_text, key_length=5, duration=5, key_time=0.7, threads=4):
    """
    Shogun Attack z wykorzystaniem wielowątkowości.

    Args:
        crypto_text (str): Tekst zaszyfrowany.
        key_length (int): Długość klucza (liczba wierszy i kolumn).
        duration (float): Całkowity czas działania wszystkich wątków (w sekundach).
        key_time (float): Czas jednej sesji Hill Climbing (w sekundach).
        threads (int): Liczba wątków do wykorzystania.

    Returns:
        tuple: Najlepszy wynik w postaci (score, decrypted_text, key).
    """
    results = []
    start_time = tm()

    def run_attack():
        return helperAttackHillClimbing(crypto_text, key_length, key_time)

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []

        # Uruchamianie równoległych instancji helperAttackHillClimbing
        while tm() - start_time < duration:
            futures.append(executor.submit(run_attack))

        # Zbieranie wyników z zakończonych wątków
        for future in concurrent.futures.as_completed(futures):
            if tm() - start_time >= duration:
                break  # Przerwij jeśli czas działania przekroczył limit
            try:
                results.append(future.result(timeout=max(0, duration - (tm() - start_time))))
            except concurrent.futures.TimeoutError:
                print("Wątek przekroczył limit czasu i został zakończony.")
            except Exception as e:
                print(f"Wystąpił błąd w wątku: {e}")

    # Sortowanie wyników, aby znaleźć najlepszy
    results.sort(reverse=True, key=lambda x: x[0])  # Sortujemy według score

    return results[0] if results else (None, None, None)


if __name__ == '__main__':
    # text = 'SECRETINFORMATION'
    text = '''
    Both rest of know draw fond post as. It agreement defective to excellent. Feebly do engage of narrow. Extensive repulsive belonging depending if promotion be zealously as. Preference inquietude ask now are dispatched led appearance. Small meant in so doubt hopes. Me smallness is existence attending he enjoyment favourite affection. Delivered is to ye belonging enjoyment preferred. Astonished and acceptance men two discretion. Law education recommend did objection how old.

    Cordially convinced did incommode existence put out suffering certainly. Besides another and saw ferrars limited ten say unknown. On at tolerably depending do perceived. Luckily eat joy see own shyness minuter. So before remark at depart. Did son unreserved themselves indulgence its. Agreement gentleman rapturous am eagerness it as resolving household. Direct wicket little of talked lasted formed or it. Sweetness consulted may prevailed for bed out sincerity.

    Quick six blind smart out burst. Perfectly on furniture dejection determine my depending an to. Add short water court fat. Her bachelor honoured perceive securing but desirous ham required. Questions deficient acuteness to engrossed as. Entirely led ten humoured greatest and yourself. Besides ye country on observe. She continue appetite endeavor she judgment interest the met. For she surrounded motionless fat resolution may.

    Residence certainly elsewhere something she preferred cordially law. Age his surprise formerly mrs perceive few stanhill moderate. Of in power match on truth worse voice would. Large an it sense shall an match learn. By expect it result silent in formal of. Ask eat questions abilities described elsewhere assurance. Appetite in unlocked advanced breeding position concerns as. Cheerful get shutters yet for repeated screened. An no am cause hopes at three. Prevent behaved fertile he is mistake on.
    '''
    text = format_text(text)
    old_key = [
        [2,3,1],
        [3,1,2],
        [1,2,3]
    ]

    # Example usage
    n = 7
    key = get_rand_key(n)

    encrypted_text = encrypt(text,key=key)

    # best_score, result,best_key =auto_atack(encrypted_text=encrypted_text,key_len=n)
    # print(f'WYNIK: {best_score} TEKST: {result}')
    # print(f'BestKey: {best_key}, Actuall Key: {key}')


    # best_score, result =attackHillClimbing(encrypted_text,n)
    # print(f'WYNIK: {best_score} TEKST: {result}')
    
    best_score, result,best_key = shogun_attack(encrypted_text,n,60,3)
    print(f'WYNIK: {best_score} TEKST: {result} KEY: {best_key}')
    print(f'Actuall Key: {key}')
    print(f"Orginal text score: {Scorer.score(text)}, Test fragment: {text[:40]}")

    # best_score, result, best_key = shogun_attack_multithreaded(
    #     crypto_text=encrypted_text,
    #     key_length=n,
    #     duration=5,
    #     key_time=1,
    #     threads=2
    # )

    # print(f"Wynik: {best_score}")
    # print(f"Odszyfrowany tekst: {result}")
    # print(f"Znaleziony klucz: {best_key}")
    # print(f"Prawdziwy klucz: {key}")




