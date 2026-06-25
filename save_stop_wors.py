import json
import nltk
from nltk.corpus import stopwords


try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

print(stop_words)
with open('stop_words.json', 'w') as f:
    json.dump(list(stop_words), f)
#py save_stop_wors.py
