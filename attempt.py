import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
from tabulate import tabulate
import math
import pickle
from statistics import variance
import matplotlib.pyplot as plt

file = open('data.pkl', 'rb')

data = pickle.load(file)

file.close()

data = data.transpose()
x = data[0].reshape(-1,1)
y = data[1].reshape(-1,1)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)
x_train = np.array_split(x_train, 10)
y_train = np.array_split(y_train, 10)
finVar = []
finBias = []
finBias2 = []

for i in range(1,10):
    predict = []

    for j in range(10):
        poly = PolynomialFeatures(degree=i)
        lm = linear_model.LinearRegression()
        x_list = poly.fit_transform(x_train[j])
        lm.fit(x_list, y_train[j])
        x_test_poly = poly.fit_transform(x_test)
        predict.append(lm.predict(x_test_poly))
        

    predict = np.array(predict).transpose()[0]
    var_list = []
    bias_list = []
    bias_list1 = []
    for j in range(len(predict)):
        bias_list.append(np.mean(np.mean(predict[j])-y_test[j]) ** 2)
        bias_list1.append(abs(np.mean(np.mean(predict[j])-y_test[j])))
        var_list.append(variance(predict[j]))
    var_list = np.array(var_list)
    finVar.append(np.mean(var_list))
    bias_list = np.array(bias_list)
    finBias2.append(np.mean(bias_list))
    bias_list1 = np.array(bias_list1)    
    finBias.append(np.mean(bias_list1))

table = []
for i in range(1,10):
    table.append([i,finBias2[i-1], finBias[i-1], finVar[i-1]])
columns = ['Degree of Model', 'Bias^2', 'Bias', 'Variance']
print(tabulate(table, headers = columns))