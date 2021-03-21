from sklearn import preprocessing
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC
data = pd.read_csv(r"C:\Users\strai\Documents\BHeat\SVM\CA_WildFires.csv")
X = data.drop('CLASS',axis=1)
X = preprocessing.scale(X)
y = data['CLASS']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30)
#Define parameter range below
#How to define multi-kernel/multi parameter list
param_grid = {'C': [0.1, 1, 10, 100, 1000],  
              'gamma': [1, 0.1, 0.01, 0.001, 0.0001,'scale'],
              'kernel': ['rbf','linear','poly','sigmoid']}  

grid = GridSearchCV(SVC(), param_grid, refit = True, verbose = 3) 
# fitting the model for grid search 
grid.fit(X_train, y_train) 
# print best parameter after tuning 
print(grid.best_params_) 
# print how our model looks after hyper-parameter tuning 
print("The best parameters are: ",grid.best_estimator_) 
grid_predictions = grid.predict(X_test) 
print(classification_report(y_test, grid_predictions)) 
