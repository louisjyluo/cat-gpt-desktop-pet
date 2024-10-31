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
        data.to_csv("data/transformed_text_dict.csv", index=True, index_label="index")
    
    def processorLinear(self, d_points):
        training_data = pd.read_csv("data/transformed_text_dict.csv")
        X = training_data['text'].head(d_points)
        self.y_lin = training_data['label'].head(d_points)
        self.linear_data_dict = {}
        self.linear_data = pd.DataFrame()
        LRfunc = np.vectorize(self.loopRow)
        LRfunc(X, range(len(X)))
        self.linear_data = self.linear_data.from_dict(self.linear_data_dict)
        self.linear_data = self.linear_data.assign(label = self.y_lin)
        self.linear_data.to_csv("data/transformed_text_linear.csv", index=True, index_label="index")
        
    def loopRow(self, sen, i):
        if isinstance(sen, str):
            words = sen.split()
            obs = []
            for j in range(len(words) - 1):
                ngram = words[j] + " " + words[j + 1]
                obs.append(ngram)
            if len(obs) != 0:
                func = np.vectorize(self.newFeature)
                func(obs, i)
            print("row", i , "completed")
    
    def newFeature(self, s, i):
        if s in self.linear_data_dict:
            self.linear_data_dict[s][i] += 1
        else:
            self.linear_data_dict[s] = np.zeros(len(self.y_lin))
            self.linear_data_dict[s][i] += 1
    
    def allZeroOrOne(self, c):
        i0, i1 = 0,0
        for i in c:
            if i == 0:
                i0 += 1
        for i in c:
            if i == 1:
                i1 += 1
        if i0 == 5 or i1 == 5:
            return False
        return True
    
    def lemmatize(self, word):
        if word.lower() not in self.stop_words:
            return self.wnl.lemmatize(word, pos="v")

def processDict():
    proc = dataProcessor()
    proc.processorDict()
    
def processLinear():
    proc = dataProcessor()
    proc.processorLinear(2000)

#processDict()
processLinear()