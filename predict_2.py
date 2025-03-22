

import numpy as np
import matplotlib.pyplot as plt  # To visualize
import pandas as pd  # To read data
from sklearn.linear_model import LinearRegression

import pickle

from scipy.optimize import curve_fit
import matplotlib.pyplot as pyplot

data = pd.read_csv('alldata_2019_4.csv')  # load data set

for value, row in data.iterrows():
    review = str(data['Inflation_avg'][value])
    review2 = str(data['GDP_currp'][value])
    review3 = str(data['Inflation_eop'][value])
    #We have to put 0s in front of FIPs values that are less than 10000 bc geojson can not recognize fips values without the leading 0
    if(review.find(',')!=-1):
      data.at[value,'Inflation_avg'] = float(review[:review.find(',')]+review[review.find(',')+1:])
    if(review2.find(',')!=-1):
      data.at[value,'GDP_currp'] = float(review2[:review2.find(',')]+review2[review2.find(',')+1:])
    if(review3.find(',')!=-1):
      data.at[value,'Inflation_eop'] = float(review3[:review3.find(',')]+review3[review3.find(',')+1:])


X = data.iloc[:, 5].values.reshape(-1, 1)  # values converts it into a numpy array
Y = data.iloc[:, 14].values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(X, Y)  # perform linear regression
Y_pred = linear_regressor.predict(X)  # make predictions




print(linear_regressor.predict(.548))
print(linear_regressor.predict(-4.199))
print(linear_regressor.predict(-5.395))
print(linear_regressor.predict(-9.349))
print(linear_regressor.predict(-7.041))
#pickle.dump(linear_regressor, open('model.sav','wb'))

plt.scatter(X, Y)
plt.plot(X, Y_pred, color='red')
plt.show()

