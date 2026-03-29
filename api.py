import pickle
from utils import sentence_without_stopwords
with open('spam_clf.pkl', 'rb') as f:
    model = pickle.load(f)
def predict_spam(message):
    message = sentence_without_stopwords(message)
    print(f"Processed message for prediction: '{message}'")
    prediction = model.predict([message])
    return prediction[0]