import random
import pandas as pd
import numpy as np
import nltk
import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

from nltk.stem import WordNetLemmatizer
# nltk.download("wordnet")
# nltk.download("omw-1.4")



# Make a plot that can
class dataProcessor():
        # label:
        # 0 = sadness
        # 1 = love
        # 2 = joy
        # 3 = anger
        # 4 = fear
        # 5 = surprise
    def __init__(self):
        self.wnl = WordNetLemmatizer()
        self.training_data = pd.read_csv("data/text.csv")
        self.stop_words = open("data/stopwords.txt", "r", encoding="utf8")
        self.stop_words = self.stop_words.read().split()
        
    def processorDict(self):
        X = self.training_data['text']
        y = self.training_data['label']
        
        new_X = []
        for sen in X:
            new_sen = []
            for word in sen.split():
                if word.lower() not in self.stop_words:
                    new_word = self.wnl.lemmatize(word, pos="v")
                    new_sen.append(new_word)
            new_X.append(" ".join(new_sen))
        data = pd.DataFrame({"text" : new_X, "label" : y})
        data.to_csv("data/transformed_text_dict.csv", index=True)
    
    def processorLinear(self):
        X = self.training_data['text'].head(2000)
        y = self.training_data['label'].head(2000)
        data = pd.DataFrame({"label" : y})
        for i, sen in enumerate(X):
            words = sen.split()
            obs = []              
            mapper = np.vectorize(self.lemmatize)
            new_sen = mapper(words)
            new_sen = np.array(list(filter(None, new_sen)))
            obs = []
            for j in range(len(new_sen) - 1):
                ngram = new_sen[j] + " " + new_sen[j + 1]
                obs.append(ngram)
            for s in obs:
                if s in data.columns:
                    data.iloc[i, data.columns.get_loc(s)] += 1
                else:
                    data = data.assign(**{s:0})
                    data.iloc[i, data.columns.get_loc(s)] += 1
            print("row", i , "completed")
        data.to_csv("data/transformed_text_linear.csv", index=True)
    
    def lemmatize(self, word):
        if word.lower() not in self.stop_words:
            return self.wnl.lemmatize(word, pos="v")

# proc = dataProcessor
# proc.processor()

def processDict():
    proc = dataProcessor()
    proc.processorDict()
    
def processLinear():
    proc = dataProcessor()
    proc.processorLinear()

#processDict()
processLinear()