#!/usr/bin/env python
import pandas as pd

# anaGood = pd.read_csv('testAnaGoodDiff.csv')
# anaGoodSampled = anaGood.sample(n=2000, replace=False)
# anaGoodSampled['label'] = '0'

# anaGoodSampled.to_csv('anaGoodSampled.csv')

good_data = pd.read_csv('anaGoodSampled.csv')
bad_data = pd.read_csv('testAnaBadDiff.csv')
bad_data['label'] = '1'

train_data = good_data.append(bad_data, ignore_index=True)

# print(train_data.sample(frac=1).head())

# print(train_data.count(axis=0))
train_data.to_csv('train_data.csv')

train_data = pd.read_csv('train_data.csv')

print(train_data.columns)

train_data.drop(columns=['Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0.1.1'], inplace=True)

train_data = train_data.sample(frac=1).reset_index(drop=True)

train_data.to_csv('new_train_data.csv')



