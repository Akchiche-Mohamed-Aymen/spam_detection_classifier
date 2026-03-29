from utils import sentence_without_stopwords
from pandas import read_csv

#======================================
emails  = read_csv('spam.csv')
emails.Category = emails.Category.map({'ham':0, 'spam':1})
emails = emails.rename(columns={'Message': 'message' , 'Category': 'category'})
emails.message = emails.message.apply(sentence_without_stopwords)
emails.to_csv('preprocessed_emails.csv', index=False)
#py pre_processing.py