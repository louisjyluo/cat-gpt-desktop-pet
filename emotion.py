import random
import pandas as pd
import numpy as np
from numpy.linalg import norm
from numpy.linalg import _umath_linalg
import scipy as scp
from scipy.linalg import solve

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
            if isinstance(X[i], float):
                break
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
        print(X.T @ X + np.identity(d), X.T @ y)
        self.w = solve(X.T @ X + 0.0001 * np.identity(d), X.T @ y)
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

    def gradDes(self, X, y):
        n, d = X.shape
        n, self.d = X.shape
        learning_rate = 0.008
        threshold = np.ones(d) * 0.01
        curr_w = np.ones(d) * 1
        
        for i in range(self.max_evals):
            g = self.getFAndG(X, y, curr_w)
            curr_w = curr_w - (learning_rate * g)
            if self.break_yes(g, i, threshold):
                break
            print("Currently on iteration:", i)
        return curr_w
            
    
    def getFAndG(self, X, y, w):
        # f = 1/2.0 * (w.T @ X.T @ X @ w - 2*y.T @ X @ w + y.T @ y) + 1/2.0 * (w.T @ w)
        g = X.T @ X @ w - X.T @ y + w
        return g

    def break_yes(self, g, iteration, threshold):
        gradient_norm = norm(g, float("inf"))
        if gradient_norm < threshold:
            if self.verbose:
                print(
                    "Problem solved up to optimality tolerance {:.3f}".format(
                        threshold
                    )
                )
            return True
        elif iteration >= self.max_evals:
            if self.verbose:
                print(
                    "Reached maximum number of function evaluations {:.3f}".format(
                        threshold
                    )
                )
            return True
        else:
            return False

def dict():
    training_data = pd.read_csv("data/transformed_text_dict.csv")
    X = training_data['text'].head(400000)
    y = training_data['label'].head(400000)
    X_valid = training_data['text'].tail(10000).reset_index(drop=True)
    y_valid = training_data['label'].tail(10000).reset_index(drop=True)
    proc = emotionDictClassifier()
    proc.fit(X, y)

    a = 1
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
    X = training_data.drop(['label', 'index'], axis=1).head(1800)
    y = training_data['label'].head(1800)
    X_valid = training_data.drop(['label', 'index'], axis=1).tail(200).reset_index(drop=True)
    y_valid = training_data['label'].tail(200).reset_index(drop=True)
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

#dict()    
linear()
