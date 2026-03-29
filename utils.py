from json import load
import re
from nltk import PorterStemmer
with open('stop_words.json', 'r') as f:
    stop_words = set(load(f))
def sentence_without_stopwords(sentence):
    stemmer = PorterStemmer()
    sentence = sentence.lower()
    sentence = re.sub(r'[^a-z\s]', '', sentence)  # Keep only lowercase letters and spaces
    words = sentence.split()
    words = [stemmer.stem(word) for word in words if word not in stop_words]
    return ' '.join(words)