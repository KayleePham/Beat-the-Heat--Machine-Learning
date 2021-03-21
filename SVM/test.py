#Initial testing of kernels on our dataset
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
#from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix
#Replace with your path
data = pd.read_csv(r"C:\Users\strai\Documents\BHeat\CA_WildFires.csv")
X = data.drop('CLASS', axis=1)
#X = X.iloc[:,:-1].values
X = preprocessing.scale(X)
y = data['CLASS']
sum = 0
acc = 0
lim = 100
#If we loop with a differing random we can get a rough average our model. 
#However it is hard to pinpoint what the best random_state is
for i in range(lim):
    #I believe a 70-30 might be a good split
    #random_state = 100 has given me the best results
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30)
    svclassifier = SVC(kernel='rbf',C=100,gamma = 1)
    svclassifier.fit(X_train, y_train)
    y_pred = svclassifier.predict(X_test)
    #print(confusion_matrix(y_test,y_pred))
    #print()
    #print(classification_report(y_test,y_pred))
    sum = sum + f1_score(y_test, y_pred,average="macro")
    acc = acc + precision_score(y_test, y_pred, average="macro")
print('Average f1_score for a rbf is:', sum/lim*100)
print('Average precision_score is: ',acc/lim*100)
sum = 0
for i in range(lim):
    #I belive a 70-30 might be a good split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30,random_state = 100)
    svclassifier = SVC(kernel='poly', degree=4)
    svclassifier.fit(X_train, y_train)
    y_pred = svclassifier.predict(X_test)
    #print(confusion_matrix(y_test,y_pred))
   # print()
   # print(classification_report(y_test,y_pred))
    sum = sum + f1_score(y_test, y_pred,average="macro")
print('Average f1_score for a poly of degree 4:', sum/lim*100)


