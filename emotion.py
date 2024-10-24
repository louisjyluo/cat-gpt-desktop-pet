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
        training_data = pd.read_csv("data/transformed_text.csv")
        self.X = training_data['text'].head(400000)
        self.y = training_data['label'].head(400000)
        
        
    # The goal is to take all the training data and turn it into     
    def fit(self):
        self.di0, self.di1, self.di2, self.di3, self.di4, self.di5 = [{}, {}, {}, {}, {}, {}]
        self.l0, self.l1, self.l2, self.l3, self.l4, self.l5 = [0,0,0,0,0,0]
        n = len(self.X)
        for i in range(n):
            los = self.X[i].split()
            slen = len(los) - 1
            match self.y[i]:
                case 0:
                    self.l0 += slen
                    self.di0 = self.genDict(self.di0, los)
                    continue
                case 1:
                    self.l1 += slen
                    self.di1 = self.genDict(self.di1, los)
                    continue
                case 2:
                    self.l2 += slen
                    self.di2 = self.genDict(self.di2, los)
                    continue
                case 3:
                    self.l3 += slen
                    self.di3 = self.genDict(self.di3, los)
                    continue
                case 4:
                    self.l4 += slen
                    self.di4 = self.genDict(self.di4, los)
                    continue
                case 5:
                    self.l5 += slen
                    self.di5 = self.genDict(self.di5, los)
                    continue
        #print(self.l0, self.l1, self.l2, self.l3, self.l4, self.l5)
        self.p = np.array([float(self.l0), float(self.l1), float(self.l2), float(self.l3), float(self.l4), float(self.l5)])
            
    def genDict(self, di, sen):
        for j in range(len(sen) - 1):
            ngram = sen[j] + " " + sen[j + 1]
            if ngram in di:
                di[ngram] += 1
            else:
                di[ngram] = 1
        return di
    
    def predict(self, X_pred):
        n = len(X_pred)
        for i in range(n):
            v0,v1,v2,v3,v4,v5 = [0,0,0,0,0,0]
            sen = X_pred[i].split()
            for j in range(len(sen) - 1):
                ngram = sen[j] + " " + sen[j + 1]
                if ngram in self.di0:
                    v0 += self.di0[ngram]
                if ngram in self.di1:
                    v1 += self.di1[ngram]
                if ngram in self.di2:
                    v2 += self.di2[ngram]
                if ngram in self.di3:
                    v3 += self.di3[ngram]
                if ngram in self.di4:
                    v4 += self.di4[ngram]
                if ngram in self.di5:
                    v5 += self.di5[ngram]
            p_pred = np.array([v0, v1, v2, v3, v4, v5])
            prob = p_pred / self.p
            lop = []
            lop.append(np.argmax(p_pred))
        ret = np.zeros(n)
        ret = ret + lop
        return ret
            
    
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
        # prep = pd.read_csv("data/prep.csv")
        # pron = open("data/pronouns.txt", "r")
        # pron = pron.read().split()
        X = training_data['text']
        y = training_data['label']
        # bad_words = []
        # for w in prep["Word"]:
        #     bad_words.append(w)
        # bad_words = np.concat((bad_words, pron))
        
        new_X = []
        for sen in X:
            new_sen = []
            for word in sen.split():
                new_word = wnl.lemmatize(word, pos="v")
                new_sen.append(new_word)
            new_X.append(" ".join(new_sen))
        data = pd.DataFrame({"text" : new_X, "label" : y})
        data.to_csv("data/transformed_text.csv", index=True)

# proc = dataProcessor
# proc.processor()

training_data = pd.read_csv("data/transformed_text.csv")
X_valid = training_data['text'].tail(10000).reset_index(drop=True)
y_valid = training_data['label'].tail(10000).reset_index(drop=True)
proc = emotionClassifier()
proc.fit()
y_hat = proc.predict(X_valid)
total = len(y_valid)
yes = 0
for i in range(total):
    if y_hat[i] == y_valid[i]:
        yes += 1
v_err = float(yes) / total * 100
print("Validation Accuracy: ",v_err, "%")