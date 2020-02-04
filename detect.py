#!/usr/bin/env python

from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.model_selection import cross_val_score
from sklearn.neural_network import MLPClassifier
import numpy as np
import pandas as pd

originalTrainingData = pd.read_csv('anaSampledForTraining.csv')
print(originalTrainingData.columns)

forTrainingData = shuffle(originalTrainingData)
X = forTrainingData[['wrdiff', 'trdiff']]
Y = forTrainingData['label']

mlp = MLPClassifier()
mlp.fit(X, Y)

accuracy = cross_val_score(mlp, X, Y, cv=10, scoring='accuracy')
precision = cross_val_score(mlp, X, Y, cv=10, scoring='precision')
recall = cross_val_score(mlp, X, Y, cv=10, scoring='recall')

print('the accuracy is: s%', accuracy)
print('the precision is: s%', precision)
print('the recall is: s%', recall)


test_x = np.array([[-0.025], [5]]).reshape(-1, 1)
# print('the prediction is:', mlp.predict(test_x))

