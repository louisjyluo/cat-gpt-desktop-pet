import random
import pandas as pd
import numpy as np

class emotionClassifier():
    
    def __init__(self):
        # label:
        # 0 = sadness
        # 1 = love
        # 2 = joy
        # 3 = anger
        # 4 = fear
        # 5 = surprise
        
        training_data = pd.read_csv("data/text.csv")
        print(training_data)
        
        
        
    # The goal is to take all the training data and turn it into     
    def fit():
        return NotImplementedError
        
    
    
    def predict():
        return NotImplementedError

emotionClassifier()