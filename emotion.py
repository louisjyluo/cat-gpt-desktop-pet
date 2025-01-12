import random
import pandas as pd
import numpy as np
from numpy.linalg import norm
from numpy.linalg import _umath_linalg
import scipy as scp
from scipy.linalg import solve, inv
from fun_obj import SoftmaxLoss
import linear_models
from optimizers import GradientDescentLineSearch
import time
from sklearn.linear_model import LogisticRegression
import transformer
import json
import nltk
import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
# nltk.download("wordnet")
# nltk.download('punkt_tab')
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

class emotionDictClassifier():    
    
    def __init__(self):
        pass
    # The goal is to take all the training data and turn it into     
    def fit(self, X, y):
        self.di0, self.di1, self.di2, self.di3, self.di4, self.di5 = [{}, {}, {}, {}, {}, {}]
        self.l0, self.l1, self.l2, self.l3, self.l4, self.l5 = [0,0,0,0,0,0]
        n = len(X)
        for i in range(n):
            if isinstance(X[i], str):
                los = X[i].split()
                slen = len(los)
                match y[i]:
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
    
    def predict(self, X_pred, a, b):
        n = len(X_pred)
        for i in range(n):
            if isinstance(X_pred[i], float):
                break
            v0,v1,v2,v3,v4,v5 = [0,0,0,0,0,0]
            sen = X_pred[i].split()
            for j in range(len(sen) - 1):
                ngram = sen[j] + " " + sen[j + 1]
                if self.occurrenceInterval(ngram, self.di0, a, b):
                    v0 += self.di0[ngram]
                if self.occurrenceInterval(ngram, self.di1, a, b):
                    v1 += self.di1[ngram]
                if self.occurrenceInterval(ngram, self.di2, a, b):
                    v2 += self.di2[ngram]
                if self.occurrenceInterval(ngram, self.di3, a, b):
                    v3 += self.di3[ngram]
                if self.occurrenceInterval(ngram, self.di4, a, b):
                    v4 += self.di4[ngram]
                if self.occurrenceInterval(ngram, self.di5, a, b):
                    v5 += self.di5[ngram]
            p_pred = np.array([v0, v1, v2, v3, v4, v5])
            prob = p_pred / self.p
            lop = []
            lop.append(np.argmax(p_pred))
        ret = np.zeros(n)
        ret = ret + lop
        return ret
    
    def occurrenceInterval(self, ngram ,di, a, b):
        return ngram in di and di[ngram] > a and di[ngram] <= b

    def genDict(self, di, sen):
        for j in range(len(sen) - 1):
            ngram = sen[j] + " " + sen[j + 1]
            if ngram in di:
                di[ngram] += 1
            else:
                di[ngram] = 1
        return di

class emotionLinearRegression():
    
    def __init__(self):
        self.verbose = False
        self.max_evals = 50

    def fit(self, X, y):
        n,d = X.shape
        # self.w = self.gradDes(X, y)
        # 0.0001 for linear BoW
        self.w = solve(X.T @ X + 0.001 * np.identity(d), X.T @ y)
        print(self.w)
        
    def predict(self, X_pred):
        y_hat_line = X_pred @ self.w
        # y_hat_norm = (y_hat_line - y_hat_line.mean())/(y_hat_line.std()) * 5
        y_hat = []
        for i in y_hat_line:
            classifier = []
            for j in range(6):
                classifier.append(abs(i - j))
            y_hat.append(np.argmin(classifier))
        return y_hat
    
    def fit_kernel(self, X, y):
        n,d = X.shape
        self.X = X
        K = (1 + X.T @ X) ** 10
        self.U = inv(K + 1 * np.identity(d)) @ y
    
    def predict_kernel(self, X_pred):
        K_test = (1 + X_pred.T @ self.X) ** 10
        y_hat_line = K_test @ self.U
        # y_hat_norm = (y_hat_line - y_hat_line.mean())/(y_hat_line.std()) * 5
        y_hat = []
        for i in y_hat_line:
            classifier = []
            for j in range(6):
                classifier.append(abs(i - j))
            y_hat.append(np.argmin(classifier))
        return y_hat

def dict():
    training_data = pd.read_csv("data/transformed_text_dict.csv")
    X = training_data['text'].head(400000)
    y = training_data['label'].head(400000)
    X_valid = training_data['text'].tail(10000).reset_index(drop=True)
    y_valid = training_data['label'].tail(10000).reset_index(drop=True)
    proc = emotionDictClassifier()
    proc.fit(X, y)

    a = 5
    b = np.inf
    y_hat = proc.predict(X, 0, 10000000)
    total = len(y)
    yes = (y_hat == y).sum()
    t_err = float(yes) / total * 100
    print("set:",a, b,":Training Accuracy: ",t_err, "%")

    mx = 0
    mx_a = 0
    mx_b = 0
    y_hat = proc.predict(X_valid, a, b)
    total = len(y_valid)
    yes = (y_hat == y_valid).sum()
    v_err = float(yes) / total * 100
    if mx < v_err:
        mx = v_err
        mx_a = a
        mx_b = b
    print("set:",a, b,":Validation Accuracy: ",v_err, "%")
    # print("set:",mx_a, mx_b,":Validation Accuracy: ",mx, "%")
    
def linear():
    training_data = pd.read_csv("data/transformed_text_linear.csv")
    X = training_data.drop(['label', 'index'], axis=1).head(200)
    y = training_data['label'].head(2500)
    X_valid = training_data.drop(['label', 'index'], axis=1).tail(500).reset_index(drop=True)
    y_valid = training_data['label'].tail(100).reset_index(drop=True)
    proc = emotionLinearRegression()
    proc.fit(X, y)

    y_hat = proc.predict(X)
    total = len(y)
    yes = (y_hat == y).sum()
    t_err = float(yes) / total * 100
    
    y_hat = proc.predict(X_valid)
    total = len(y_valid)
    yes = (y_hat == y_valid).sum()
    v_err = float(yes) / total * 100
    print("Training Accuracy: ",t_err, "%")
    print("Validation Accuracy: ",v_err, "%")

def softMax():
    training_data = pd.read_csv("data/transformed_text_linear.csv")
    X = training_data.drop(['label', 'index'], axis=1).head(4000).to_numpy()
    y = training_data['label'].head(4000).to_numpy()
    X_valid = training_data.drop(['label', 'index'], axis=1).tail(1000).reset_index(drop=True).to_numpy()
    y_valid = training_data['label'].tail(1000).reset_index(drop=True).to_numpy()
    print("transforming complete")
    start_time = time.time()
    fun_obj = SoftmaxLoss()
    optimizer = GradientDescentLineSearch(max_evals=1000, verbose=True)
    model = linear_models.MulticlassLinearClassifier(fun_obj, optimizer)
    model.fit(X, y)
    
    fitted_weighting = pd.DataFrame(model.W)
    fitted_weighting.to_csv("data/softmax_lib_weightings", index=True, index_label="index")
    print("weightings saved to data")
    
    y_hat = model.predict(X)
    total = len(y)
    yes = (y_hat == y).sum()
    t_err = float(yes) / total * 100
    
    y_hat = model.predict(X_valid)
    total = len(y_valid)
    yes = (y_hat == y_valid).sum()
    v_err = float(yes) / total * 100
    print("Training Accuracy: ",t_err, "%")
    print("Validation Accuracy: ",v_err, "%")
    print("Total Eval Time:", time.time() - start_time)

def softMaxPreMade():
    training_data = pd.read_csv("data/transformed_text_linear.csv")
    X = training_data.drop(['label', 'index'], axis=1).head(8000)
    y = training_data['label'].head(8000)
    X_valid = training_data.drop(['label', 'index'], axis=1).tail(2000).reset_index(drop=True)
    y_valid = training_data['label'].tail(2000).reset_index(drop=True)
    print("transforming complete")
    start_time = time.time()
    softMax = LogisticRegression(multi_class='multinomial', penalty="l2", fit_intercept=False)
    
    softMax.fit(X,y)
    
    SM_y_hat_train = softMax.predict(X)
    SM_y_hat_valid = softMax.predict(X_valid)
    
    SM_t_error = (SM_y_hat_train == y).sum() / len(y)
    SM_v_error = (SM_y_hat_valid == y_valid).sum() / len(y_valid)

    print("SoftMax Training Accuracy:", round(SM_t_error, 4))
    print("SoftMax Validation Accuracy:", round(SM_v_error, 4))
    print("Total Eval Time:", time.time() - start_time)
    
def softMaxFit():
    training_data = pd.read_csv("data/transformed_text_linear.csv")
    X = training_data.drop(['label', 'index'], axis=1).head(5000).to_numpy()
    y = training_data['label'].head(5000).to_numpy()
    bow_columns = {"bow": list(training_data.drop(['label', 'index'], axis=1).columns.values)}
    print("transforming complete")
    fun_obj = SoftmaxLoss()
    optimizer = GradientDescentLineSearch(max_evals=1000, verbose=True)
    model = linear_models.MulticlassLinearClassifier(fun_obj, optimizer)
    model.fit(X, y)
    
    fitted_weighting = pd.DataFrame(model.W)
    fitted_weighting.to_csv("data/softmax_lib_weightings", index=True, index_label="index")
    print("weightings saved to data")
    
    json_object = json.dumps(bow_columns, indent=4)
    
    with open("bow_columns.json", "w") as outfile:
        outfile.write(json_object)
    
def softMaxPrediction(data):
    wnl = WordNetLemmatizer()
    weightings = pd.read_csv("data/softmax_lib_weightings")
    w = np.array(weightings["0"])
    with open('bow_columns.json', 'r') as openfile:
        bow_columns = json.load(openfile)

    sentences = sent_tokenize(data)
    print(sentences)
    dic = {}
    for i in bow_columns["bow"]:
        dic[i] = [0] * len(sentences)
    
    all_zeros = [1] * len(sentences)
    for i, sen in enumerate(sentences):
        sen_p = ""
        for word in sen.split(" "):
            word = wnl.lemmatize(word)
            sen_p = sen_p + " " + word
        for word in sen_p.split(" "):
            if word in dic:
                dic[word][i] += 1
                all_zeros[i] = 0
    X_pred = pd.DataFrame.from_dict(dic).to_numpy()
    y_preds = [0] * len(sentences)
    n, d = X_pred.shape
    W = w.reshape(len(w)//6, 6)
    for i in range(n):
        if all_zeros[i] == 0:
            y_preds[i] = np.argmax(X_pred[i] @ W)
        else:
            y_preds[i] = -1
    return y_preds
    
#dict()    
#linear() 
#softMaxFit()
#softMaxPreMade()
#softMaxPrediction(["meow", "hello", "how are you human", "ready to eat some food", "because I am ready to eat"])