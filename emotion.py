import random
import pandas as pd
import numpy as np
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

from nltk.stem import WordNetLemmatizer
nltk.download("wordnet")
nltk.download("omw-1.4")

class emotionClassifier():
    
    def __init__(self):
        return NotImplementedError
        
        
    # The goal is to take all the training data and turn it into     
    def fit(self, X, y):
        return NotImplementedError
        
    
    
    def predict(self, X, y):
        return NotImplementedError

class dataProcessor():
    def processor():
        wnl = WordNetLemmatizer()
        # label:
        # 0 = sadness
        # 1 = love
        # 2 = joy
        # 3 = anger
        # 4 = fear
        # 5 = surprise
        training_data = pd.read_csv("data/text.csv")
        X = training_data['text'].head(5000)
        y = training_data['label'].head(5000)
        X_valid = training_data['text'][7000:9000]
        y_valid = training_data['label'][7000:9000]
        # print(X, y, X_valid, y_valid)
        
        for sen in X:
            for word in sen.split():
                print("{0:20}{1:20}".format(word, wnl.lemmatize(word, pos="v")))
        
proc = dataProcessor
proc.processor()