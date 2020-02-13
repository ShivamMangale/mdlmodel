import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt 



with open('X_train.pkl', 'rb') as file1:
    X_train = np.array(pickle.load(file1))
with open('X_test.pkl', 'rb') as file1:
    X_test = np.array(pickle.load(file1)).reshape(-1,1)
with open('Y_train.pkl', 'rb') as file1:
    y_train = np.array(pickle.load(file1))
with open('Fx_test.pkl', 'rb') as file1:
    y_test = np.array(pickle.load(file1)).reshape(-1,1)




finalVar = []
finalBias = []
for i in range(1, 100):
    pred = []
    poly = PolynomialFeatures(degree=i)
    

    for j in range(0,10):
        X_list = poly.fit_transform(X_train[j].reshape(-1,1))
        X_test_poly = poly.fit_transform(X_test)
        lm = linear_model.LinearRegression()
        lm.fit(X_list, y_train[j].reshape(-1,1))
        pred.append(lm.predict(X_test_poly))
    
    pred = np.array(pred).transpose()[0]
    var_list = []
    bias_list = []
    
    for j in range(len(pred)):
        var_list.append(np.var(pred[j]))
        bias_list.append((np.mean(pred[j])-y_test[j]) ** 2)
    var_list = np.array(var_list)
    bias_list = np.array(bias_list)
    finalVar.append(np.mean(var_list))
    finalBias.append(np.mean(bias_list))

x = list(range(1,100))
plt.plot(y, finalVar, color = 'green')
plt.plot(x, finalBias)
plt.xlabel('Degree')
plt.ylabel('Error')  
plt.show()
    