import re
from collections import defaultdict

# Load the bigram frequencies from a file into a dictionary.
def load_bigram_frequencies(file_path):
    bigram_frequencies = {}
    with open(file_path, 'r') as f:
        for line in f:
            match = re.match(r"(\w{2})\s+(\d+)", line.strip())
            if match:
                bigram = match.group(1).upper()
                frequency = int(match.group(2))
                bigram_frequencies[bigram] = frequency
    return bigram_frequencies

# Normalize the frequencies to probabilities.
def normalize_frequencies(bigram_frequencies):
    total_count = sum(bigram_frequencies.values())
    return {bigram: freq / total_count for bigram, freq in bigram_frequencies.items()}

# Score a given text based on bigram probabilities.
def score_text(text, bigram_probabilities):
    text = re.sub(r"[^A-Z]", "", text.upper())  # Keep only uppercase letters.
    score = 0.0
    for i in range(len(text) - 1):
        bigram = text[i:i+2]
        if bigram in bigram_probabilities:
            score += bigram_probabilities[bigram]
        else:
            score += 0  # Optionally, penalize unseen bigrams (e.g., score += -1)
    return score
