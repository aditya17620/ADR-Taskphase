import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

data_path = ['Downloads']
filepath = os.sep.join(data_path + ['heart.csv'])
hd = pd.read_csv(filepath)
#sns.countplot(x="target", data=hd, palette="bwr")
#sns.countplot(x="sex", data=hd, palette="bwr")
#plt.show()

print(hd.groupby('target').mean())
'''
plt.scatter(x=hd.age[hd.target==1], y=hd.thalach[(hd.target==1)], c="red")
plt.scatter(x=hd.age[hd.target==0], y=hd.thalach[(hd.target==0)])
plt.legend(["Disease", "Not Disease"])
plt.xlabel("Age")
plt.ylabel("Maximum Heart Rate")
plt.show()

pd.crosstab(hd.cp, hd.target).plot(kind="bar", figsize=(15,6),color=['#11A5AA','#AA1190'])
plt.title('Pain freq wrt Chest pain')
plt.xlabel('Type of pain')
plt.show()
'''

cpdv = pd.get_dummies(hd['cp'], prefix="cp")
thaldv = pd.get_dummies(hd['thal'], prefix="thal")
slopedv = pd.get_dummies(hd['slope'], prefix="slope")

frames = [hd, cpdv, thaldv, slopedv]
hd = pd.concat(frames,axis=1)
hd = hd.drop(columns = ['cp', 'thal','slope'])
#print(hd.head(5))

y = hd.target.values
x_data = hd.drop(['target'], axis = 1)
x = (x_data - np.min(x_data)) / (np.max(x_data) - np.min(x_data)).values

x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2, random_state=0)
'''
# the score varies from 0.86885 to 0.8852 based on the number of neighbors 
knn = KNeighborsClassifier(8)
knn.fit(x_train, y_train)

y_prediction = knn.predict(x_test)
score = knn.score(x_test, y_test)
print(score)
'''
# SVM gives a score of 0.8852. The better of the two methods.
svm = SVC(random_state=1)
svm.fit(x_train,y_train)
y_prediction = svm.predict(x_test)
score = svm.score(x_test, y_test)
print(score)

'''
plt.plot(y_test, y_prediction, color = 'orange')
plt.ylim(0)
plt.show()
'''
