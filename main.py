
from pandas import read_csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.metrics import recall_score, precision_score, accuracy_score
#======================================
emails = read_csv('preprocessed_emails.csv').dropna()
X , y = emails.drop(columns=['category']), emails.category

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, shuffle=True)

pipeline = ImbPipeline([
    ('vectorizer', TfidfVectorizer()),
    ('smote', SMOTE(random_state=42, k_neighbors=6)),
    ('classifier', MultinomialNB())
])

pipeline.fit(X_train.message, y_train)

# Save the trained model
import pickle
with open('spam_clf.pkl', 'wb') as f:
    pickle.dump(pipeline, f)

y_pred = pipeline.predict(X_test.message)
recall = recall_score(y_test, y_pred)   
precision = precision_score(y_test, y_pred)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.4f}')
print(f'Precision: {precision:.4f}')
print(f'Recall: {recall:.4f}')
import pickle
with open('spam_clf.pkl', 'wb') as f:
    pickle.dump(pipeline, f)
    
