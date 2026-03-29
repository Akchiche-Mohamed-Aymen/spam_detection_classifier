import json
import nltk
from nltk.corpus import stopwords
import ssl

# Workaround for SSL certificate issue
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

print(stop_words)
with open('stop_words.json', 'w') as f:
    json.dump(list(stop_words), f)
#py save_stop_wors.py