import math

class ngram_score(object):
    def __init__(self, ngramfile, sep=' '):
        ''' Load a file containing n-grams and counts, calculate log probabilities '''
        self.ngrams = {}
        key = None  # Initialize key
        with open(ngramfile) as file:
            for line in file:
                parts = line.split(sep)
                if len(parts) == 2:
                    key, count = parts
                    self.ngrams[key] = int(count)
        if key is not None:  # Check if key was assigned
            self.L = len(key)
        else:
            self.L = 0
        self.N = sum(self.ngrams.values())  # Use values() for Python 3
        # Calculate log probabilities
        if self.N > 0:
            for key in self.ngrams.keys():
                self.ngrams[key] = math.log10(float(self.ngrams[key]) / self.N)
            self.floor = math.log10(0.01 / self.N)
        else:
            self.floor = -math.inf  # Log of 0 is undefined, use negative infinity

    def score(self, text):
        ''' Compute the score of text '''
        score = 0
        ngrams = self.ngrams.__getitem__
        for i in range(len(text) - self.L + 1):  # Use range() for Python 3
            if text[i:i + self.L] in self.ngrams:
                score += ngrams(text[i:i + self.L])
            else:
                score += self.floor
        return score
