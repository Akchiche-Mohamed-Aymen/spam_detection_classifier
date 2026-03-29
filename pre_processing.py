import re
from pandas import read_csv
from nltk import PorterStemmer
from json import load

#======================================
def sentence_without_stopwords(sentence):
    sentence = sentence.lower()
    sentence = re.sub(r'[^a-z\s]', '', sentence)  # Keep only lowercase letters and spaces
    words = sentence.split()
    words = [stemmer.stem(word) for word in words if word not in stop_words]
    return ' '.join(words)
#=============================
with open('stop_words.json', 'r') as f:
    stop_words = set(load(f))
stemmer = PorterStemmer()

emails  = read_csv('spam.csv')
emails.Category = emails.Category.map({'ham':0, 'spam':1})
emails = emails.rename(columns={'Message': 'message' , 'Category': 'category'})
emails.message = emails.message.apply(sentence_without_stopwords)
emails.to_csv('preprocessed_emails.csv', index=False)
#py pre_processing.py