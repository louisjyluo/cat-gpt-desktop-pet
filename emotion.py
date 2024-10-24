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

# Current Algo idea (ensemble 1 vs All classification)
# Fit
# Take each label put all the words (trigram??? Lemmatized trigram) with that label into a dict
# Which will create 6 separates dictionaries that contains all the training words and how many times they have occurred in all our data
# The more often a word occurs the more likely it is correlated to the label, therefore their weighting will be higher
# Save all 6 dictionary 
# Predict
# Given a new sentence, check what the value of each word gives. Then take the summed value divide it by total amount of words placed into the dictionary to get the portions
# Do it for all 6 dictionaries and see what percentage each model outputs
# Choose the max(probability)

class emotionClassifier():
    
    def __init__(self):
        return NotImplementedError
        
        
    # The goal is to take all the training data and turn it into     
    def fit(self, X, y):
        return NotImplementedError
        
    
    
    def predict(self, X, y):
        return NotImplementedError
    
# Make a plot that can
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
        
        new_X = []
        for sen in X:
            new_sen = []
            for word in sen.split():
                new_word = wnl.lemmatize(word, pos="v")
                new_sen.append(new_word)
            new_X.append(" ".join(new_sen))
        return new_X
        
proc = dataProcessor
proc.processor()