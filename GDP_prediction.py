import sys
import os
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

data_path = ['Downloads']
filepath = os.sep.join(data_path + ['GDP.csv'])
GDP = pd.read_csv(filepath)
#print(GDP)

var = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code']
data = pd.melt(GDP, var,var_name='year', value_name='GDP')
data['year'] = data['year'].astype(int)

data = data.dropna()
#print(data)

data.drop(['Country Code', 'Indicator Name','Indicator Code'], axis=1, inplace=True)
data.rename(columns={'Country Name':'Country'}, inplace=True)

values = ['Arab World',
         'Caribbean small states',
          'Central Europe and the Baltics',
          'Early-demographic dividend',
          'East Asia & Pacific (excluding high income)',
          'Early-demographic dividend',
          'East Asia & Pacific',
          'East Asia & Pacific (IDA & IBRD countries)',
          'Europe & Central Asia',
          'Europe & Central Asia (IDA & IBRD countries)',
          'Europe & Central Asia (excluding high income)',
          'Euro area',
          'European Union',
          'Fragile and conflict affected situations',
          'Heavily indebted poor countries (HIPC)',
          'High income',
          'IBRD only',
          'IDA & IBRD total',
          'IDA total',
          'IDA blend',
          'IDA only',
          'Late-demographic dividend',
          'Latin America and Caribbean',
          'Latin America & Caribbean',
          'Latin America & Caribbean (excluding high income)',
          'Latin America & the Caribbean (IDA & IBRD countries)',
          'Lower middle income',
          'Low & middle income',
          'Middle income',
          'Middle East & North Africa (IDA & IBRD countries)',
          'Middle East & North Africa',
          'Middle East & North Africa (excluding high income)',
          'North America',
          'OECD members',
          'Pacific island small states',
          'Post-demographic dividend',
          'Pre-demographic dividend',
          'South Asia (IDA & IBRD)',
          'Sub-Saharan Africa (IDA & IBRD countries)',
          'Sub-Saharan Africa (excluding high income)',
          'Sub-Saharan Africa',
          'Small states',
          'Upper middle income',
          'World']

for i in range(0, 60):
    for value in values:
       condition = data[data.Country == value].index
       data.drop(condition, inplace=True)

#print(data['Country'].value_counts())


file = 'GDP_clean.csv'
data.to_csv(file, index=False)
#print("{} saved".format(file))


country = 'United Kingdom'
filter = data['Country'] != country
dataus = data.drop(data[filter].index, inplace=False)


x = dataus[['year']].values
y = dataus['GDP'].values
x_train, x_test, y_train,y_test = train_test_split(x, y, test_size=0.1, random_state=0)

"""
# Linear regression method ----> R2 Score: 0.936
regr = LinearRegression()
model = regr.fit(x_train,y_train)
y_prediction = model.predict(x_test)



------------------------------------------------------------------

Graddient Descent method ----> R2 Score: from 0.9194
based on different conditions of train test split

class Regressor():
    def __init__(self, learning_rate=0.01, tol=0.01, seed=None,normalize=False):
        self.W = None
        self.b = None
        self.__lr = learning_rate
        self.__tol = tol
        self.__length = None
        self.__normalize = normalize
        self.__m = None
        self.__costs = []
        self.__iterations = []
        np.random.seed(seed if seed is not None else np.random.randint(100))
    # random initialization of weights and bias
    def __initialize_weights_and_bias(self):
        self.W = np.random.randn(self.__length) #(n,1)
        self.b = 0
    # compute the error function: sum of squared errors 
    def __computeCost(self,h,Y):
        loss = np.square(h-Y)
        cost = np.sum(loss)/(2*self.__m)
        return cost
    # implement optimization function
    def __optimize(self,X,Y):
        h = np.dot(X,self.W)+self.b
        dW = np.dot( X.T, (h-Y) ) / self.__m
        db = np.sum( h-Y )  / self.__m
        self.W = self.W - self.__lr*dW
        self.b = self.b - self.__lr*db
    # normalize the dataset by subtracting the mean and dividing by std deviation
    def __normalizeX(self,X):return (X-self.__mean) / (self.__std)
    # fit the model to the dataset: training process
    def fit(self, X, y, verbose=False):
        if self.__normalize:
            self.__mean, self.__std = X.mean(axis=0), X.std(axis=0)
            X = self.__normalizeX(X)
        self.__m,self.__length = X.shape
        self.__initialize_weights_and_bias()
        last_cost,i = float('inf'),0
        while True:
            h = np.dot(X,self.W)+self.b
            cost = self.__computeCost(h,y)
            if verbose: print(f"Iteration: {i}, Cost: {cost:.3f}")
            self.__optimize(X,y)
            if last_cost-cost < self.__tol: break
            else: last_cost,i = cost,i+1
            self.__costs.append(cost)
            self.__iterations.append(i)
    # test the model on test data
    def predict(self,X):

        if self.__normalize: X = self.__normalizeX(X)
        return np.dot(X,self.W)+self.b
    # plot the iterations vs cost curves
    def plot(self,figsize=(7,5)):
        plt.figure(figsize=figsize)
        plt.plot(self.__iterations,self.__costs)
        plt.xlabel('Iterations')
        plt.ylabel('Cost')
        plt.title("Iterations vs Cost")
        plt.show()
    # calculates the accuracy
    def score(self,X,y):
        return 1-(np.sum(((y-self.predict(X))**2))/np.sum((y-np.mean(y))**2))


regressor = Regressor(normalize=True)
regressor.fit(x_train,y_train)
train = regressor.score(x_train,y_train)
test = regressor.score(x_test, y_test)
y_prediction = regressor.predict(x_test)
regressor.plot()

-------------------------------------------------------------------

Ridge regression ----> R2 Score from 0.6988 to 0.9198
based on different alpha value


Rreg = Ridge(alpha= 0.3, normalize=True)
model= Rreg.fit(x_train, y_train)
y_prediction = model.predict(x_test)

-----------------------------------------------------------------

Lasso Regression ----> R2 Score 0.9194

lassoreg = Lasso(alpha=0.7, normalize=True)
model = lassoreg.fit(x_train, y_train)
y_prediction = model.predict(x_test)
"""

polyreg = PolynomialFeatures(degree=10)
x_poly = polyreg.fit_transform(x_train)
poly_reg = LinearRegression()
poly_reg.fit(x_poly, y_train)
y_prediction = poly_reg.predict(polyreg.fit_transform(x_test))

plt.scatter(x_train, y_train, color='red')
plt.plot(x_test, y_prediction, color='gray')
plt.show()


print(r2_score(y_test,y_prediction))
print(mean_squared_error(y_test, y_prediction))
# gives an R2 Score of 0.997752
# which is the best score out of all the other methods used.
# so we will opt for a polynomial regression model to predict

'''
plt.scatter(x_train,y_train,color = 'gray')
plt.plot(x_test, y_test, color = 'orange')
plt.ylim(0)
plt.show()
'''
