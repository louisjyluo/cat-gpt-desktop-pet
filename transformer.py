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
    
    def processorLinear(self, d_points, write_to_csv):
        training_data = pd.read_csv("data/transformed_text_dict.csv")
        X = training_data['text'].head(d_points)
        self.y_lin = training_data['label'].head(d_points)
        self.len = len(self.y_lin)
        self.linear_data_dict = {}
        self.linear_data = pd.DataFrame()
        LRfunc = np.vectorize(self.loopRow)
        LRfunc(X, range(len(X)))
        if write_to_csv:
            print("rows completed")
            self.linear_data = self.linear_data.from_dict(self.linear_data_dict)
            self.linear_data = self.linear_data.assign(label = self.y_lin)
            self.linear_data.to_csv("data/transformed_text_linear.csv", index=True, index_label="index")
        else:
            print("rows completed for untested")
            return self.linear_data_dict
    
    #data is a list of sentences
    def processTestData(self, data, linear_data_dict):
        self.len = len(data)
        self.data = pd.DataFrame()
        self.linear_data_dict = linear_data_dict
        LRfunc = np.vectorize(self.loopRow)
        LRfunc(data, range(len(data)))
        print("rows completed in test data")
        print(self.linear_data_dict)
        self.data = self.data.from_dict(self.linear_data_dict)
        return self.data.reset_index().tail(self.len)
        
    def loopRow(self, sen, i):
        if isinstance(sen, str):
            words = sen.split()
            obs = []
            for j in range(len(words)):
                ngram = words[j] # + " " + words[j + 1]
                ngram = self.lemmatize(ngram)
                obs.append(ngram)
            if len(obs) != 0:
                func = np.vectorize(self.newFeature)
                func(obs, i)
    
    def newFeature(self, s, i):
        if s in self.linear_data_dict:
            self.linear_data_dict[s][i] += 1
        else:
            self.linear_data_dict[s] = np.zeros(self.len)
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
    
def processLinear(write_to_csv):
    proc = dataProcessor()
    linear_data_dict = proc.processorLinear(20000, write_to_csv)
    return linear_data_dict

#processDict()
#processLinear(True)